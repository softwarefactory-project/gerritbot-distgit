%global commit  f32d742effb74d8e5f81673247411189aa7308e2
%global sum     Gerritbot is an IRC bot that will notify IRC channels of Gerrit events.

Name:           gerritbot
Version:        0.4.0
Release:        2%{?dist}
Summary:        %{sum}


License:        ASL 2.0
URL:            http://docs.openstack.org/infra/system-config/
Source0:        https://github.com/openstack-infra/gerritbot/archive/%{commit}.tar.gz
Source1:        gerritbot.service
Source2:        tmpfile.conf
Source10:       logging.conf
Source11:       gerritbot.conf
Source12:       channels.yaml

Patch1:         0001-Add-change-created-event-type.patch
Patch2:         0001-Support-missing-daemon-lib.patch

BuildArch:      noarch

Requires:       python-pbr
Requires:       python2-gerritlib
Requires:       python2-irc
Requires:       PyYAML
Requires:       python-paho-mqtt

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  systemd


%description
%{sum}


%prep
%autosetup -n %{name}-%{commit} -p1
rm requirements.txt test-requirements.txt


%build
PBR_VERSION=%{version} %{__python2} setup.py build


%install
PBR_VERSION=%{version} %{__python2} setup.py install --skip-build --root %{buildroot}

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/gerritbot.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}/lib/tmpfiles.d/gerritbot.conf
install -p -D -m 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/gerritbot/logging.conf
install -p -D -m 0640 %{SOURCE11} %{buildroot}%{_sysconfdir}/gerritbot/gerritbot.conf
install -p -D -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/gerritbot/channels.yaml
install -p -d -m 0700 %{buildroot}%{_sharedstatedir}/gerritbot
install -p -d -m 0755 %{buildroot}%{_var}/run/gerritbot
install -p -d -m 0700 %{buildroot}%{_var}/log/gerritbot


%pre
getent group gerritbot >/dev/null || groupadd -r gerritbot
if ! getent passwd gerritbot >/dev/null; then
  useradd -r -g gerritbot -G gerritbot -d %{_sharedstatedir}/gerritbot -s /sbin/nologin -c "Gerritbot Daemon" gerritbot
fi
exit 0


%post
%systemd_post gerritbot.service


%preun
%systemd_preun gerritbot.service


%postun
%systemd_postun_with_restart gerritbot.service


%files
%{_bindir}/gerritbot
%{_unitdir}/gerritbot.service
%dir %{_sysconfdir}/gerritbot/
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/gerritbot/logging.conf
%config(noreplace) %attr(0640, root, gerritbot) %{_sysconfdir}/gerritbot/gerritbot.conf
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/gerritbot/channels.yaml
%dir %attr(0700, gerritbot, gerritbot) %{_sharedstatedir}/gerritbot
%dir %attr(0750, gerritbot, gerritbot) %{_var}/log/gerritbot
%dir %attr(0755, gerritbot, gerritbot) %{_var}/run/gerritbot
%{python2_sitelib}/gerritbot
%{python2_sitelib}/gerritbot-*.egg-info
/lib/tmpfiles.d/gerritbot.conf


%changelog
* Tue Jun 11 2019 Tristan Cacqueray <tdecacqu@redhat.com> - 0.4.0-2
- Drop python-daemon requirement

* Mon Jun 18 2017 Tristan Cacqueray <tdecacqu@redhat.com> - 0.4.0-1
- Bump version

* Thu Apr 27 2017 Fabien Boucher <fboucher@redhat.com> - 0.3.0-2
- Set the right service identity Gerritbot

* Thu Mar 16 2017 Tristan Cacqueray - 0.3.0-1
- Initial packaging
