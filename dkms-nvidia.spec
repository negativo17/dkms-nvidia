%global debug_package %{nil}
%global dkms_name nvidia

Name:           dkms-%{dkms_name}
Version:        570.124.04
Release:        1%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
# Package is not noarch as it contains pre-compiled binary code
ExclusiveArch:  x86_64 aarch64

Source0:        %{dkms_name}-kmod-%{version}-x86_64.tar.xz
Source1:        %{dkms_name}-kmod-%{version}-aarch64.tar.xz
Source2:        %{name}.conf

BuildRequires:  sed

Provides:       %{dkms_name}-kmod = %{?epoch:%{epoch}:}%{version}
Requires:       %{dkms_name}-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:       dkms

Conflicts:      akmod-nvidia

%description
This package provides the proprietary Nvidia kernel driver modules.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

%prep
%ifarch x86_64
%autosetup -p1 -n %{dkms_name}-kmod-%{version}-x86_64
%endif

%ifarch aarch64
%autosetup -p1 -T -b 1 -n %{dkms_name}-kmod-%{version}-aarch64
%endif

cp -f %{SOURCE2} dkms.conf

sed -i -e 's/__VERSION_STRING/%{version}/g' dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
rm -f %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/*/dkms.conf

%post
dkms add -m %{dkms_name} -v %{version} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%{_usrsrc}/%{dkms_name}-%{version}

%changelog
* Fri Feb 28 2025 Simone Caronni <negativo17@gmail.com> - 3:570.124.04-1
- Update to 570.124.04.

* Sun Feb 09 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.16-2
- Simplify DKMS configuration.

* Fri Jan 31 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.16-1
- Update to 570.86.16.

* Mon Jan 27 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.15-1
- Update to 570.86.15.

* Thu Dec 05 2024 Simone Caronni <negativo17@gmail.com> - 3:565.77-1
- Update to 565.77.

* Wed Oct 23 2024 Simone Caronni <negativo17@gmail.com> - 3:565.57.01-1
- Update to 565.57.01.

* Wed Oct 16 2024 Simone Caronni <negativo17@gmail.com> - 3:560.35.03-3
- Do not uninstall in preun scriptlet in case of an upgrade.

* Fri Oct 11 2024 Simone Caronni <negativo17@gmail.com> - 3:560.35.03-2
- Fix versioning in the dkms.conf file.
- Add kernel 6.11 patch

* Wed Sep 04 2024 Simone Caronni <negativo17@gmail.com> - 3:560.35.03-1
- Update to 560.35.03.

* Tue Jul 02 2024 Simone Caronni <negativo17@gmail.com> - 3:555.58.02-1
- Update to 555.58.02.

* Fri Jun 28 2024 Simone Caronni <negativo17@gmail.com> - 3:555.58-1
- Update to 555.58.

* Wed Jun 05 2024 Simone Caronni <negativo17@gmail.com> - 3:550.90.07-1
- Update to 550.90.07.

* Fri Apr 26 2024 Simone Caronni <negativo17@gmail.com> - 3:550.78-1
- Update to 550.78.

* Thu Apr 18 2024 Simone Caronni <negativo17@gmail.com> - 3:550.76-1
- Update to 550.76.

* Sun Mar 24 2024 Simone Caronni <negativo17@gmail.com> - 3:550.67-1
- Update to 550.67.

* Sat Mar 09 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-2
- Enable aarch64.

* Sun Mar 03 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-1
- Update to 550.54.14.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 3:550.40.07-1
- Update to 550.40.07.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 3:545.29.06-2
- Add patch to fix build with the latest 6.6/6.7 kernels.

* Fri Dec 01 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.06-1
- Update to 545.29.06.

* Tue Nov 14 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-3
- Update location of configuration file.

* Tue Nov 14 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-2
- Trim changelog.
- Allow building proprietary or open source modules.
- Adjust compile command to match with what Nvidia ships nowadays.

* Tue Oct 31 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-1
- Update to 545.29.02.

* Wed Oct 18 2023 Simone Caronni <negativo17@gmail.com> - 3:545.23.06-1
- Update to 545.23.06.

* Fri Sep 22 2023 Simone Caronni <negativo17@gmail.com> - 3:535.113.01-1
- Update to 535.113.01.

* Thu Aug 24 2023 Simone Caronni <negativo17@gmail.com> - 3:535.104.05-1
- Update to 535.104.05.

* Wed Aug 09 2023 Simone Caronni <negativo17@gmail.com> - 3:535.98-1
- Update to 535.98.

* Wed Jul 19 2023 Simone Caronni <negativo17@gmail.com> - 3:535.86.05-1
- Update to 535.86.05.

* Tue Jun 20 2023 Simone Caronni <negativo17@gmail.com> - 3:535.54.03-1
- Update to 535.54.03.

* Fri May 12 2023 Simone Caronni <negativo17@gmail.com> - 3:525.116.04-1
- Update to 525.116.04.

* Mon May 01 2023 Simone Caronni <negativo17@gmail.com> - 3:525.116.03-1
- Update to 525.116.03.

* Fri Feb 10 2023 Simone Caronni <negativo17@gmail.com> - 3:525.89.02-1
- Update to 525.89.02.

* Fri Jan 20 2023 Simone Caronni <negativo17@gmail.com> - 3:525.85.05-1
- Update to 525.85.05.

* Mon Jan 09 2023 Simone Caronni <negativo17@gmail.com> - 3:525.78.01-1
- Update to 525.78.01.

* Tue Nov 29 2022 Simone Caronni <negativo17@gmail.com> - 3:525.60.11-1
- Update to 525.60.11.

* Thu Oct 13 2022 Simone Caronni <negativo17@gmail.com> - 3:520.56.06-1
- Update to 520.56.06.

* Wed Sep 21 2022 Simone Caronni <negativo17@gmail.com> - 3:515.76-1
- Update to 515.76.

* Mon Aug 08 2022 Simone Caronni <negativo17@gmail.com> - 3:515.65.01-1
- Update to 515.65.01.

* Wed Jun 29 2022 Simone Caronni <negativo17@gmail.com> - 3:515.57-1
- Update to 515.57.

* Thu Jun 09 2022 Simone Caronni <negativo17@gmail.com> - 3:515.48.07-1
- Update to 515.48.07.

* Tue May 31 2022 Simone Caronni <negativo17@gmail.com> - 3:510.73.05-1
- Update to 510.73.05.

* Mon May 02 2022 Simone Caronni <negativo17@gmail.com> - 3:510.68.02-1
- Update to 510.68.02.

* Mon Mar 28 2022 Simone Caronni <negativo17@gmail.com> - 3:510.60.02-1
- Update to 510.60.02.

* Mon Feb 14 2022 Simone Caronni <negativo17@gmail.com> - 3:510.54-1
- Update to 510.54.

* Wed Feb 02 2022 Simone Caronni <negativo17@gmail.com> - 3:510.47.03-1
- Update to 510.47.03.
