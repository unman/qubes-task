Name:     3isec-qubes-task-manager
Version:  1.0
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
cp -rv %{SOURCE0}/qubes-task*  %{buildroot}/usr/bin

%post

%pre

%preun

%postun

%files
%defattr(-,root,root,-)
/usr/bin/qubes-task
/usr/bin/qubes-task-gui
