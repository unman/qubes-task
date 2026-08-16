Name:     3isec-qubes-task-manager
Version:  2.0
Release:  1
Summary:  Qubes task manager

Group:    Qubes
Vendor:   Invisible Things Lab
License:  GPL
URL:      http://www.qubes-os.org

Source0:  qubes-task

AutoReq:  no

BuildArch: x86_64

Requires:  python3

%description
Qubes task manager

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
mkdir -p $%{buildroot}/usr/share/qubes-task
cp %{SOURCE0}/qubes-task*  %{buildroot}/usr/bin
cp %{SOURCE0}/desc/* $%{buildroot}/usr/share/qubes-task

%post

%pre

%preun

%postun

%files
%defattr(-,root,root,-)
/usr/bin/qubes-task
/usr/bin/qubes-task-gui
/usr/share/qubes-task/3isec-qubes-admin.txt
/usr/share/qubes-task/3isec-qubes-builder.txt
/usr/share/qubes-task/3isec-qubes-cacher.txt
/usr/share/qubes-task/3isec-qubes-dnscrypt.txt
/usr/share/qubes-task/3isec-qubes-git.txt
/usr/share/qubes-task/3isec-qubes-gpg.txt
/usr/share/qubes-task/3isec-qubes-mirage-firewall.txt
-usr/share/qubes-task/3isec-qubes-monitor.txt
/usr/share/qubes-task/3isec-qubes-mullvad-vpn.txt
/usr/share/qubes-task/3isec-qubes-sys-multimedia.txt
/usr/share/qubes-task/3isec-qubes-mutt.txt
/usr/share/qubes-task/3isec-qubes-pihole.txt
/usr/share/qubes-task/3isec-qubes-qubes-doc.txt
/usr/share/qubes-task/3isec-qubes-qubes-ssh-agent.txt
/usr/share/qubes-task/3isec-qubes-reader.txt
/usr/share/qubes-task/3isec-qubes-store.txt
/usr/share/qubes-task/3isec-qubes-syncthing.txt
