### RPM external tbb 40_20120613oss
Source: http://threadingbuildingblocks.org/uploads/77/187/4.0%20update%205/tbb%{realversion}_src.tgz

%prep
%setup -n tbb%{realversion}

%build
make %compilingprocesses

%install
install -d %i/lib
cp -r include %i/include
find build -name "*.$SONAME" -exec cp {} %i/lib \; 