# fedora-hp-flash

Repository to build the RPM packages for Fedora of the HP Flash and Replicated Setup Utilities for Linux.
Contains all the files needed to build the RPMS/SRPMS, but not HP sources files.

## General information
The purpose of this repository is to ease the build of the packages for the last Fedora distribution of the different HP Flash and Replicated Setup Utilities for Linux. This should also ease their installation.

This repository contains different branches corresponding to their counterparts versions of the original HP tools available here:

[https://ftp.ext.hp.com/pub/caps-softpaq/cmit/HP_LinuxTools.html](https://ftp.ext.hp.com/pub/caps-softpaq/cmit/HP_LinuxTools.html)

The `main` branch corresponds to the latest version available from the HP WEBsite.

**Caution - Disclaimer**

This repository is not provided by HP and is not an official HP one. It doesn't provide any HP materials. 

Questions about the files provided in this repository should only be request through the tools provided by this repository and not forwarded to any HP WEBsite. All the materials provided in this repository are the exclusive property of their respective owner (see each file internal dedicated section about that).

No support will be provided through this repository and it is only made available as is.

## Usage

In order to build all the RPM packages needed to get the HP Flash and Replicated Setup Utilities for Linux, please follow the below instructions.

- Create a local working directory.
- Choose the correct branch corresponding to the wished version.
- Download each `.spec` file of the chosen branch.
- Download the HP sources archives and copy them in `~/rpmbuild/SOURCE/` directory. Downloading them manually (URLs provided in each `.spec` file) is possible, but it is also possible, when available, to use `spectool` to download the sources files. Using `spectool` allow to download directly the sources files in a destination directory.

  Download sources files and then copy them in `~/rpmbuild/SOURCE/` directory:

  - Downloading:

  `$ spectool -g <package_name.spec>`

  - Copying:

  `$ cp <downloaded_package_source.tar.gz> ~/rpmbuild/SOURCE/`

  Or download directly in the correct directory:

  `$ spectool -g <package_name.spec> -C ~/rpmbuild/SOURCE/`

- Build each package using this command:

  `$ rpmbuild -ba <package_name.spec>`

- Build binaries packages should be found here:

  `~/rpmbuild/RPMS/noarch`

  `~/rpmbuild/RPMS/x86_64`

- Build sources packages should be found here:

  `~/rpmbuild/SRPMS`

- Install the binaries packages file (as a root user):

  `$ sudo dnf install <package_name.rpm>`

- Enjoy!