%define  debug_package %{nil}
%global __os_install_post %{nil}

%define service_user harbor
%define service_group harbor
%define service_homedir /opt/harbor
%define service_logdir /var/log/harbor
%define service_configdir /etc/harbor
%define service_datadir /var/lib/harbor

Summary: Harbor Chart Server
Name: harbor-chartserver
Version: ¤CLEANVERSION¤
Release: ¤BUILDRELEASE¤%{dist}
Source0: chartm-¤VERSION¤
Source1: harbor-chartserver.service
Source2: env 
License: GPLv3
Group: System Tools
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}.buildroot
AutoReqProv: false

%description
%{summary}

%prep

%install
mkdir -p $RPM_BUILD_ROOT%{service_homedir}/chartserver
mkdir -p $RPM_BUILD_ROOT%{service_configdir}/chartserver
mkdir -p $RPM_BUILD_ROOT%{service_datadir}/chart
mkdir -p $RPM_BUILD_ROOT%{_unitdir}

install -m 755 %{SOURCE0} %{buildroot}/%{service_homedir}/chartserver/chartm
install -m 755 %{SOURCE1} %{buildroot}/%{_unitdir}/harbor-chartserver.service
install -m 755 %{SOURCE2} %{buildroot}/%{service_configdir}/chartserver/env

%pre
/usr/bin/getent group %{service_group} >/dev/null || /usr/sbin/groupadd --system %{service_group}
/usr/bin/getent passwd %{service_user} >/dev/null || /usr/sbin/useradd --no-create-home --system -g %{service_group} --home-dir %{service_homedir} -s /bin/bash %{service_user}
/usr/sbin/usermod -s /bin/bash %{service_user}

%post

%preun

%postun

%clean

%files
%defattr(0644, harbor, harbor, 0755)
%config %{service_configdir}/chartserver
%{service_homedir}/chartserver
%dir %{service_datadir}/chart
%attr(0755, harbor, harbor) %{service_homedir}/chartserver/chartm
%attr(0644, root, root) %{_unitdir}/harbor-chartserver.service

%changelog