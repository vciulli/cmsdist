### RPM external openldap-toolfile 1.0
Requires: openldap
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/openldap.xml
<tool name="openldap" version="@TOOL_VERSION@">
  <client>
    <environment name="OPENLDAP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$OPENLDAP_BASE/lib"/>
  </client>
  <use name="openssl"/>
  <use name="db4"/>
  <architecture name="slc6_*">
    <use name="cyrus-sasl"/>
  </architecture>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
