#%define node_id 1
%define node_spec_version 1.0

%define product_version 5.3.1

%define product_name jboss-soap
%define product_home /usr/local/java/%{product_name}-%{product_version}

%define username jboss
%define user_group jboss
%define group_id 500

Name:	    %{product_name}
Version:	%{product_version}
Release:	1%{?dist}
Summary:    Set up instance of JBoss SOA Platform %{product_version}

Group:      Administration
License:	GPL
URL:        http://access.redhat.com/

Packager:   Romain Pelisse
BuildArch:  noarch

Source0:    %{product_name}-%{product_version}.tgz
#Source1:    postgres.tgz
#Source2:    jboss-patches.tgz

#Patch0:     jboss-as-standalone.sh.patch
#Patch1:     add-node-default-jvm-settings.patch
#Patch2:	    set-default-jsf-to-1.2.patch

Requires(pre): java-1.7.0-openjdk,java-1.7.0-openjdk-devel

%prep
%setup -q
#%setup -q -D -T -b 1
#%setup -q -D -T -b 2
#%global _default_patch_fuzz 2
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1

%pre
mkdir -p %{product_home}
getent group %{user_group} > /dev/null || groupadd -r %{user_group} -g %{group_id}
getent passwd %{username}  > /dev/null || \
    useradd -r -g %{group} -d %{product_home} -s /sbin/nologin \
    -c "JBoss  user account" %{username}

%install
mkdir -p %{buildroot}/%{product_home}

%post
%define service_name /etc/init.d/%{product_name}
if [ ! -L %{service_name} ]; then
  ln -s %{product_home}/etc/init.d/%{product_name} %{service_name}
fi

%clean
exit 0

%description

%files
%defattr(-,%{username},%{group})
%{product_home}

%doc


%changelog

