# HP .spec for HP uefi flash utility kernel module rpm

##
# Hewlett-Packard Company Confidential
# (C) Copyright 2019 Hewlett-Packard Development Company, L.P.
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

Name:       hpuefi-module-tools
Version:    3.01
Release:    1%{?dist}
Summary:    HP FLASH: Common files for utility kernel module for UEFI Linux HP systems

License:    GPLv2
Group:      System Environment/Kernel
# Retrieve from https://support.hp.com/us-en/drivers
# or from https://ftp.ext.hp.com/pub/caps-softpaq/cmit/HP_LinuxTools.html
URL:        https://ftp.hp.com/pub/softpaq/sp98501-99000/sp98908.html
Source0:    https://ftp.hp.com/pub/softpaq/sp98501-99000/sp98908.tgz

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
* Thu Oct 03 2019 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.01-1
- Initial release
