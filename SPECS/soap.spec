%define node_spec_version 1.0

%define product_version 5.3.1

%define product_name jboss-soap
%define product_home /usr/share/%{product_name}-%{product_version}
%define service_home /usr/share/jboss-soap

%define username jboss
%define user_group jboss
%define group_id 500

Name:	    %{product_name}
Version:	%{product_version}
Release:	4%{?dist}
Summary:    Set up instance of JBoss SOA Platform %{product_version}

Group:      Administration
License:	GPL
URL:        http://access.redhat.com/

Packager:   Romain Pelisse
BuildArch:  x86_64

Source0:    %{product_name}-%{product_version}.tgz

Requires(pre): java-1.7.0-openjdk,java-1.7.0-openjdk-devel

%prep
%setup -q

%pre
mkdir -p %{product_home}
getent group %{user_group} > /dev/null || groupadd -r %{user_group} -g %{group_id}
getent passwd %{username}  > /dev/null || \
    useradd -r -g %{user_group} -d %{product_home} -s /bin/bash \
    -c "JBoss  user account" %{username}

%install
mkdir -p %{buildroot}/%{product_home}
cp -Rp %{_builddir}/%{product_name}-%{version}/* %{buildroot}/%{product_home}

%post

if [ ! -L %{service_home} ]; then
  ln -s %{product_home} %{service_home}
fi

if [ ! -e %{product_home}/etc/init.d/%{product_name} ]; then
  echo 'No such file [%{product_home}/etc/init.d/%{product_name}] - faulty install, aborting...'
  exit 1
fi

%define service_name /etc/init.d/%{product_name}
if [ ! -L %{service_name} ]; then
  ln -s %{product_home}/etc/init.d/%{product_name} %{service_name}
fi

%preun
if [ ! -L %{service_name} ]; then
  service %{service_name} stop
fi

%clean
exit 0

%description

%files
%defattr(-,%{username},%{user_group})
%{product_home}

%doc


%changelog
* Tue Jul 22 2014 Romain Pelisse <belaran@gmail.com> - 5.3.1-4
- Add new init.d script soa-p

* Tue Jul 08 2014 Romain Pelisse <belaran@gmail.com> - 5.3.1-3
- Fix http-uinvoker

* Tue Jul 08 2014 Romain Pelisse <belaran@gmail.com> - 5.3.1-2
- Adding http-invoker to EJB lookup over HTTP
- Fix broken hornet configuration
- Switch user 'jboss' to /bin/bash

* Mon Jul 07 2014 Romain Pelisse <belaran@gmail.com> - 5.3.1-1
- Initial release
