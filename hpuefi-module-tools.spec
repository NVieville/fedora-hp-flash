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
%define hp_flash_name hp-flash
%define hp_flash_global_ver 3.25
%define hp_flash_global_package_prefix_name sp157762
# Build download URL directory from prefix_name
%define hp_flash_global_package_interval %(c=%{hp_flash_global_package_prefix_name} ; t=${c//[!0-9]/} ; if [ ${t: -3} -le 500 ] ; then echo "${c//[!a-z;A-Z]/}${t::${#t}-3}001-$(( ${t::${#t}-3}001+499 ))" ; else echo "${c//[!a-z;A-Z]/}${t::${#t}-3}501-$(( ${t::${#t}-3}501+499 ))" ; fi)

Name:       hpuefi-module-tools
Version:    3.06
Release:    1%{?dist}
Summary:    HP FLASH: Common files for utility kernel module for UEFI Linux HP systems

License:    GPLv2
Group:      System Environment/Kernel
# Retrieve from https://support.hp.com/us-en/drivers
# or from https://ftp.ext.hp.com/pub/caps-softpaq/cmit/linuxtools/HP_LinuxTools.html
URL:        https://ftp.hp.com/pub/softpaq/%{hp_flash_global_package_interval}/%{hp_flash_global_package_prefix_name}.html
Source0:    https://ftp.hp.com/pub/softpaq/%{hp_flash_global_package_interval}/%{hp_flash_global_package_prefix_name}.tgz

BuildArch:  noarch
Provides:   hpuefi-kmod-common = %{version}
Requires:   hpuefi-kmod >= %{version}

# HP UEFI flashing tool only plays on x86_64 bits machines
ExclusiveArch:  x86_64


%description
The hp flash %{version} BIOS flash utility kernel module for UEFI
systems. This is intended ONLY for HP products.

This Package provides common files for the hpuefi-kmod package.


%prep
%setup -q -c
pushd non-rpms
 tar xzf hpuefi-mod-%{version}.tgz
 # Add shell script standard shebang
 sed -i -e '1 i #!/bin/sh' hpuefi-mod-%{version}/mkdevhpuefi
popd


%build
echo "Nothing to build."


%install
install -m 0755 -d                                         %{buildroot}%{_libexecdir}/%{hp_flash_name}
install -m 0755 non-rpms/hpuefi-mod-%{version}/mkdevhpuefi %{buildroot}%{_libexecdir}/%{hp_flash_name}/


%postun
modprobe -r hpuefi
depmod
if [ -c /dev/hpuefi ] ; then
 /bin/rm -f /dev/hpuefi
fi


%files
%doc non-rpms/hpuefi-mod-%{version}/README
%license non-rpms/hpuefi-mod-%{version}/COPYING
%dir %{_libexecdir}/%{hp_flash_name}
%{_libexecdir}/%{hp_flash_name}/mkdevhpuefi


%changelog
* Fri Apr 25 2025 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.06-1
- Upgrade to 3.06

* Mon Mar 25 2024 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.05-1
- Upgrade to 3.05

* Wed Jun 07 2023 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.04-2
- Update sources files to sp143035.tgz
- Adapt SPEC file

* Tue Sep 13 2022 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.04-1
- Upgrade to 3.04

* Mon Oct 25 2021 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.03-1
- Upgrade to 3.03

* Thu Oct 03 2019 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.01-1
- Initial release
