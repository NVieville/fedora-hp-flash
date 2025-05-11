# HP .spec for HP uefi flash utility kernel module rpm

##
# Hewlett-Packard Company Confidential
# (C) Copyright 2020 Hewlett-Packard Development Company, L.P.
# All rights reserved.
#
# Disclaimer of Warranty: This software is experimental and
# provided "as-is" by Hewlett-Packard Development Company,
# LP. ("HP")  HP shall have no obligation to maintain or
# support this software.  HP makes no express or implied
# warranty of any kind regarding this software including any
# warranties of merchantability, fitness for a particular
# purpose, title or non-infringement.  HP shall not be liable
# for any direct, indirect, special, incidental, or consequential
# damages, whether based on contract, tort or any other legal
# theory, in connection with or arising out of the furnishing,
# performance or use of this software.
##

%global debug_package %{nil}
%define hp_flash_global_ver 3.25
%define hp_flash_global_package_prefix_name sp157762
# Build download URL directory from prefix_name
%define hp_flash_global_package_interval %(c=%{hp_flash_global_package_prefix_name} ; t=${c//[!0-9]/} ; if [ ${t: -3} -le 500 ] ; then echo "${c//[!a-z;A-Z]/}${t::${#t}-3}001-$(( ${t::${#t}-3}001+499 ))" ; else echo "${c//[!a-z;A-Z]/}${t::${#t}-3}501-$(( ${t::${#t}-3}501+499 ))" ; fi)

Name:       hp-flash
Version:    3.25
Release:    1%{?dist}
Summary:    HP FLASH: BIOS utilities for x86_64 UEFI Linux systems

License:    Redistributable, no modification permitted
Group:      System Environment/Kernel
# Retrieve from https://support.hp.com/us-en/drivers
# or from https://ftp.ext.hp.com/pub/caps-softpaq/cmit/linuxtools/HP_LinuxTools.html
URL:        https://ftp.hp.com/pub/softpaq/%{hp_flash_global_package_interval}/%{hp_flash_global_package_prefix_name}.html
Source0:    https://ftp.hp.com/pub/softpaq/%{hp_flash_global_package_interval}/%{hp_flash_global_package_prefix_name}.tgz

Requires:   hpuefi-kmod >= 3.06

# HP UEFI flashing tool only plays on x86_64 bits machines
ExclusiveArch:  x86_64


%description
The hp flash %{version} BIOS flash utilities programs for x86_64 UEFI systems
running Linux. It offers both flash and replicated setup support (see
/usr/share/doc/hp-flash directory for details). This is intended ONLY
for HP products.


%prep
%setup -q -c
pushd non-rpms
 tar xzf %{name}-%{version}_%{_arch}.tgz
 # Adapt paths and names to Fedora locations and naming scheme
 sed -i -e 's@/opt/hp/hp-flash/bin@%{_libexecdir}/%{name}@g' %{name}-%{version}_%{_arch}/{hp-flash,hp-repsetup}
 sed -i -e 's@/lib/modules/`uname -r`/kernel/drivers/hpuefi@%{_libexecdir}/%{name}@g' %{name}-%{version}_%{_arch}/{hp-flash,hp-repsetup}
 sed -i -e 's@hpuefi-mod@hpuefi-kmod@g' %{name}-%{version}_%{_arch}/{hp-flash,hp-repsetup}
%if 0%{?rhel} == 6
cp %{name}-%{version}_%{_arch}/builds/hp-flash.rh610 %{name}-%{version}_%{_arch}/bin/hp-flash
cp %{name}-%{version}_%{_arch}/builds/hp-repsetup.rh610 %{name}-%{version}_%{_arch}/bin/hp-repsetup
%endif
%if 0%{?rhel} == 7
cp %{name}-%{version}_%{_arch}/builds/hp-flash.rh70 %{name}-%{version}_%{_arch}/bin/hp-flash
cp %{name}-%{version}_%{_arch}/builds/hp-repsetup.rh70 %{name}-%{version}_%{_arch}/bin/hp-repsetup
%endif
%if 0%{?rhel} == 8
cp %{name}-%{version}_%{_arch}/builds/hp-flash.rh80 %{name}-%{version}_%{_arch}/bin/hp-flash
cp %{name}-%{version}_%{_arch}/builds/hp-repsetup.rh80 %{name}-%{version}_%{_arch}/bin/hp-repsetup
%endif
%if 0%{?rhel} == 9
cp %{name}-%{version}_%{_arch}/builds/hp-flash.rh90 %{name}-%{version}_%{_arch}/bin/hp-flash
cp %{name}-%{version}_%{_arch}/builds/hp-repsetup.rh90 %{name}-%{version}_%{_arch}/bin/hp-repsetup
%endif
%if 0%{?fedora} || 0%{?rhel} > 9
cp %{name}-%{version}_%{_arch}/builds/hp-flash.rh90 %{name}-%{version}_%{_arch}/bin/hp-flash
cp %{name}-%{version}_%{_arch}/builds/hp-repsetup.rh90 %{name}-%{version}_%{_arch}/bin/hp-repsetup
%endif
popd


%build
echo "Nothing to build."


%install
install -m 0755 -d                                                   %{buildroot}%{_sbindir}
install -m 0755 non-rpms/%{name}-%{version}_%{_arch}/hp-flash        %{buildroot}%{_sbindir}/
install -m 0755 non-rpms/%{name}-%{version}_%{_arch}/hp-repsetup     %{buildroot}%{_sbindir}/
install -m 0755 -d                                                   %{buildroot}%{_libexecdir}/%{name}
install -m 0755 non-rpms/%{name}-%{version}_%{_arch}/bin/hp-flash    %{buildroot}%{_libexecdir}/%{name}/
install -m 0755 non-rpms/%{name}-%{version}_%{_arch}/bin/hp-repsetup %{buildroot}%{_libexecdir}/%{name}/


%files
%doc docs/* non-rpms/%{name}-%{version}_%{_arch}/docs/{hp-flash-README,hp-repsetup-README}
%{_sbindir}/hp-flash
%{_sbindir}/hp-repsetup
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/hp-flash
%{_libexecdir}/%{name}/hp-repsetup


%changelog
* Fri Apr 25 2025 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.25-1
- Upgrade to 3.25

* Mon Mar 25 2024 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.24-1
- Upgrade to 3.24

* Wed Jun 07 2023 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.22-2
- Update sources files to sp143035.tgz
- Added documentation files
- Adapt SPEC file

* Tue Sep 13 2022 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.22-1
- Upgrade to 3.22

* Mon Oct 25 2021 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.21-1
- Upgrade to 3.21

* Thu Oct 03 2019 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.01-1
- Initial release
