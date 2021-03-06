%define  debug_package %{nil}
%global __os_install_post %{nil}

%define service_user harbor
%define service_group harbor
%define service_homedir /opt/harbor
%define service_logdir /var/log/harbor
%define service_configdir /etc/harbor
%define service_datadir /var/lib/harbor

Summary: Harbor Core Service
Name: harbor-core
Version: 1.10.1_rc1
Release: 1%{dist}
Source0: harbor_core-v1.10.1-rc1
Source1: harbor-core.service
Source2: app.conf
Source3: env
Source4: db-v1.10.1-rc1.tar.gz
Source5: reset-password-mail.tpl
Source6: 404.tpl
Source7: prepareapp-v1.10.1-rc1.tar.gz
Source8: harbor.yml
License: GPLv3
Group: System Tools
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}.buildroot
AutoReqProv: false

%description
%{summary}

%prep
tar zxf %{SOURCE4}

%install
mkdir -p $RPM_BUILD_ROOT%{service_homedir}/core/views
mkdir -p $RPM_BUILD_ROOT%{service_homedir}/setup
mkdir -p $RPM_BUILD_ROOT%{service_configdir}/db
mkdir -p $RPM_BUILD_ROOT%{service_datadir}/data
mkdir -p $RPM_BUILD_ROOT%{service_configdir}/core
mkdir -p $RPM_BUILD_ROOT%{service_configdir}/core/token
mkdir -p $RPM_BUILD_ROOT%{service_configdir}/core/certificates
mkdir -p $RPM_BUILD_ROOT%{service_configdir}/secret/core
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{service_logdir}

mv db-v1.10.1-rc1/db/ $RPM_BUILD_ROOT%{service_configdir}/db/initial
mv db-v1.10.1-rc1/migrations/postgresql $RPM_BUILD_ROOT%{service_configdir}/db/migrations
cd %{buildroot}/%{service_homedir}/setup/ && tar zxf %{SOURCE7}
echo "1.10.1_rc1" > $RPM_BUILD_ROOT%{service_homedir}/core/UIVERSION

install -m 755 %{SOURCE0} %{buildroot}/%{service_homedir}/core/harbor_core
install -m 755 %{SOURCE1} %{buildroot}/%{_unitdir}/harbor-core.service
install -m 755 %{SOURCE2} %{buildroot}/%{service_configdir}/core/app.conf
install -m 755 %{SOURCE3} %{buildroot}/%{service_configdir}/core/env
install -m 755 %{SOURCE5} %{buildroot}/%{service_homedir}/core/views/reset-password-mail.tpl
install -m 755 %{SOURCE6} %{buildroot}/%{service_homedir}/core/views/404.tpl
install -m 755 %{SOURCE8} %{buildroot}/%{service_homedir}/setup/harbor.yml

%pre
/usr/bin/getent group %{service_group} >/dev/null || /usr/sbin/groupadd --system %{service_group}
/usr/bin/getent passwd %{service_user} >/dev/null || /usr/sbin/useradd --no-create-home --system -g %{service_group} --home-dir %{service_homedir} -s /bin/bash %{service_user}
/usr/sbin/usermod -s /bin/bash %{service_user}

%post
%systemd_post harbor-core

%preun
%systemd_preun harbor-core

%postun
%systemd_postun harbor-core

%clean

%files
%defattr(0644, harbor, harbor, 0755)
%config %{service_configdir}/core
%config %{service_configdir}/db
%{service_homedir}/core
%{service_homedir}/setup
%dir %{service_datadir}/data
%dir %{service_configdir}/secret/core
%attr(0755, harbor, harbor) %{service_homedir}/core/harbor_core
%attr(0755, harbor, harbor) %{service_homedir}/setup
%attr(0644, root, root) %{_unitdir}/harbor-core.service

%changelog
* Tue Feb 11 2020 07:09:14 +0000 Martin Juhl <m@rtinjuhl.dk> 1.10.1_rc1
- New version build: 1.10.1_rc1
* Fri Dec 06 2019 11:09:41 +0000 Martin Juhl <m@rtinjuhl.dk> 1.10.0_rc2
- New version build: 1.10.0_rc2
* Fri Nov 22 2019 11:08:55 +0000 Martin Juhl <mj@casalogic.dk> 1.10.0_rc1
- New version build: 1.10.0_rc1
* Wed Nov 20 2019 19:01:50 +0000 Martin Juhl <mj@casalogic.dk> 1.9.3_rc1
* Wed Nov 20 2019 16:47:17 +0000 Martin Juhl <mj@casalogic.dk> 1.9.3_rc1
* Thu Nov 14 2019 19:12:31 +0000 Martin Juhl <mj@casalogic.dk> 1.9.3_rc1
- New version build: 1.9.3_rc1
* Sun Nov 03 2019 15:08:58 +0000 Martin Juhl <mj@casalogic.dk> 1.9.2_rc1
- New version build: 1.9.2_rc1
* Fri Sep 27 2019 14:15:32 +0000 Martin Juhl <mj@casalogic.dk> 1.9.1_rc1
- New version build: 1.9.1_rc1
* Wed Sep 11 2019 18:15:49 +0000 Martin Juhl <mj@casalogic.dk> 1.9.0_rc2
- New version build: 1.9.0_rc2
* Wed Sep 04 2019 06:14:54 +0000 Martin Juhl <mj@casalogic.dk> 1.9.0_rc1
- New version build: 1.9.0_rc1
* Wed Aug 14 2019 12:08:23 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2
* Wed Aug 14 2019 10:41:29 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2
- New version build: 1.8.2
* Tue Aug 13 2019 13:18:23 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2_rc2
* Tue Aug 13 2019 12:17:17 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2_rc2
* Tue Aug 13 2019 11:41:14 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2_rc2
* Tue Aug 13 2019 11:25:34 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2_rc2
* Tue Aug 13 2019 10:15:29 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2_rc2
- New version build: 1.8.2_rc2
* Fri Aug 02 2019 16:58:07 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2_rc1
* Fri Aug 02 2019 16:55:21 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2_rc1
* Fri Aug 02 2019 16:53:58 +0000 Martin Juhl <mj@casalogic.dk> 1.8.2_rc1
- New version build: 1.8.2_rc1
