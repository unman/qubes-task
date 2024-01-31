Name:		  3isec-qubes-task-manager
Version:	0.2
Release:	1
Summary:	Qubes task manager

Group:		Qubes
Vendor:		Invisible Things Lab
License:	GPL
URL:		  http://www.qubes-os.org

Source0:  qubes-task

AutoReq:  no

BuildArch: x86_64

Requires:  python3

%description
Qubes task manager

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/lib/python3.11/site-packages/qubesadmin/tools
mkdir -p %{buildroot}/usr/lib/python3.11/site-packages/qubesadmin/tools/__pycache__
cp -rv %{SOURCE0}/qubes-task*  %{buildroot}/usr/bin
cp %{SOURCE0}/qubes_task.py %{buildroot}/usr/lib/python3.11/site-packages/qubesadmin/tools


%post

%pre

%preun

%postun

%files
%defattr(-,root,root,-)
/usr/bin/qubes-task
/usr/bin/qubes-task-gui
/usr/lib/python3.11/site-packages/qubesadmin/tools/qubes_task.py
/usr/lib/python3.11/site-packages/qubesadmin/tools/__pycache__/qubes_task.cpython-311.*
