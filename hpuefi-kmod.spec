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

# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%if 0%{?fedora}
 #global buildforkernels current
 %global buildforkernels akmod
 %global debug_package %{nil}
%endif
%define hp_flash_global_ver 3.22

Name:       hpuefi-kmod
Version:    3.04
Release:    1%{?dist}
Summary:    hpuefi kernel module

License:    GPLv2
Group:      System Environment/Kernel
# Retrieve from https://support.hp.com/us-en/drivers
# or from https://ftp.ext.hp.com/pub/caps-softpaq/cmit/HP_LinuxTools.html
URL:        https://ftp.ext.hp.com/pub/softpaq/sp141001-141500/sp141048.html
Source0:    https://ftp.ext.hp.com/pub/softpaq/sp141001-141500/sp141048.tgz
Source11:   hpuefi-kmod-kmodtool-excludekernel-filterfile

# HP UEFI flashing tool only plays on x86_64 bits machines
ExclusiveArch:  x86_64

# Get the needed BuildRequires (in parts depending on what we build for)
%global AkmodsBuildRequires %{_bindir}/kmodtool, elfutils-libelf-devel
BuildRequires:  %{AkmodsBuildRequires}

%{!?kernels:BuildRequires: gcc, elfutils-libelf-devel, buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
The hp flash %{version} BIOS flash utility kernel module for UEFI
systems running kernel ${kernel_version}. This is intended ONLY for
HP products.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null


%setup -q -c -T -a 0
tar xvf sp141048.tar
if [ $? -ne 0 ]; then
  exit $?
fi
mkdir %{name}-%{version}-src
pushd %{name}-%{version}-src
 tar xzf ../hpflash-%{hp_flash_global_ver}/non-rpms/hpuefi-mod-%{version}.tgz
popd

for kernel_version in %{?kernel_versions} ; do
 cp -a %{name}-%{version}-src/hpuefi-mod-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
 make %{?_smp_mflags} -C "${kernel_version##*___}" M="${PWD}/_kmod_build_${kernel_version%%___*}" KVERS="${kernel_version%%___*}" KSRC="${kernel_version##*___}" KDIR="%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}" modules
done


%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}
  install -m 0755 -d    ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
  install -m 0755 *.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 popd
done

chmod 0755 $RPM_BUILD_ROOT%{kmodinstdir_prefix}*%{kmodinstdir_postfix}/* || :
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Tue Sep 13 2022 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.04-1
- Upgrade to 3.04

* Mon Oct 25 2021 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.03-1
- Upgrade to 3.03

* Thu Oct 03 2019 Nicolas Viéville <nicolas.vieville@uphf.fr> - 3.01-1
- Initial release
- Fixed the akmods build on kernel 5.4
