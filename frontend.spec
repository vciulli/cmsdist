### RPM cms frontend 4.1
Source: http://www.nikhef.nl/~janjust/proxy-verify/grid-proxy-verify.c
Requires: apache-setup mod_wsgi mod_perl2 p5-apache2-modssl p5-compress-zlib
Requires: p5-digest-hmac p5-apache-dbi p5-dbi oracle p5-dbd-oracle oracle-env
Requires: p5-dbd-sqlite

%prep

%build
case $(uname) in
  Darwin ) STATIC= DYNAMIC= ;;
  *      ) STATIC=-Wl,-Bstatic DYNAMIC=-Wl,-Bdynamic ;;
esac
gcc -o %_builddir/grid-proxy-verify \
  %_sourcedir/grid-proxy-verify.c \
  -I$OPENSSL_ROOT/include -L$OPENSSL_ROOT/lib \
  $STATIC -lssl -lcrypto $DYNAMIC -ldl

%install
mkdir -p %i/{bin,etc/env.d,etc/profile.d}
ln -sf ../profile.d/init.sh %i/etc/env.d/10-frontend.sh
cp -p %_builddir/grid-proxy-verify %i/bin/

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Clean up unnecessary environment before starting the server.
cat > %i/etc/env.d/99-env-cleanup.sh <<- \EOF
        case $(uname) in Darwin ) unset LD_LIBRARY_PATH ;; * ) unset DYLD_FALLBACK_LIBRARY_PATH ;; esac
	for P in $(perl -e 'print map { /^([A-Z0-9_]+)_CATEGORY$/ && "$1\n" } keys %ENV'); do
	  unset ${P}_ROOT ${P}_VERSION ${P}_CATEGORY ${P}_REVISION
	done
EOF

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh