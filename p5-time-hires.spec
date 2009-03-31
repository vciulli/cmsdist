### RPM external p5-time-hires 1.9715-CMS24
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
# a comment to build from scratch increase this number 15
%if "%cmsplatf" == "slc4_ia32_gcc345"
Provides: librt.so.1()(64bit)
Provides: librt.so.1(GLIBC_2.2.5)(64bit)
%endif
%define perl /usr/bin/env perl
%if "%(echo %cmsplatf | cut -f1 -d_ | sed -e 's|\([A-Za-z]*\)[0-9]*|\1|')" == "osx"
%define perl /usr/bin/perl
%endif

%define perlversion %(%perl -e 'printf "%%vd", $^V')
%define perlarch %(%perl -MConfig -e 'print $Config{archname}')
%define downloadn Time-HiRes

Source: http://search.cpan.org/CPAN/authors/id/J/JH/JHI/%{downloadn}-%{realversion}.tar.gz
%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
%perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
case %{cmsos} in
    slc4_ia32)
    if ldd /usr/bin/gcc | grep -q /lib64/
    then
        make install
        mv %i/lib/site_perl/%perlversion/x86_64-linux-thread-multi  %i/lib/site_perl/%perlversion/i386-linux-thread-multi
        make clean
        export PATH=/usr/bin/:$PATH
        export GCC_EXEC_PREFIX=/usr/lib/gcc/
        %perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
        make
        make install
     else
        make install
     fi;;
    *)
        make install
    ;;
esac

%install
