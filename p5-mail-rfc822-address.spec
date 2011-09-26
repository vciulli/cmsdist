### RPM external p5-mail-rfc822-address 0.3
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Mail-RFC822-Address
Source: http://search.cpan.org/CPAN/authors/id/P/PD/PDWARREN/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make

%install
make install
rm -rf %i/man