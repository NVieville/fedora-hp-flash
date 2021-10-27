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

Name:       hp-flash
Version:    3.01
Release:    1%{?dist}
Summary:    HP FLASH: BIOS utilities for x86_64 UEFI Linux systems

License:    Redistributable, no modification permitted
Group:      System Environment/Kernel
# Retrieve from https://support.hp.com/us-en/drivers
# or from https://ftp.ext.hp.com/pub/caps-softpaq/cmit/HP_LinuxTools.html
URL:        https://ftp.hp.com/pub/softpaq/sp98501-99000/sp98908.html
Source0:    https://ftp.hp.com/pub/softpaq/sp98501-99000/sp98908.tgz

Requires:   hpuefi-kmod >= %{version}

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
%doc non-rpms/%{name}-%{version}_%{_arch}/docs/{hp-flash-README,hp-repsetup-README}
%doc %attr(0644,root,root) docs/HP\ Linux\ Tools\ Readme.{txt,pdf,rtf}
%{_sbindir}/hp-flash
%{_sbindir}/hp-repsetup
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/hp-flash
%{_libexecdir}/%{name}/hp-repsetup


%changelog
* Thu Oct 03 2019 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.01-1
- Initial release
