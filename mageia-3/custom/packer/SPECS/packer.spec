Summary:	A tool for building identical machine images for multiple platforms
Name:		packer
Version:	0.3.8
Release:	%mkrel 1
Source0:	https://dl.bintray.com/mitchellh/packer/%{version}_linux_amd64.zip
License:	MPL2
Group:		Development/Other
Url:		http://packer.io/
BuildArch:	x86_64

%description
Packer is a tool for building identical machine images for multiple platforms
from a single source configuration.

Packer is lightweight, runs on every major operating system, and is highly
performant, creating machine images for multiple platforms in parallel. Packer
comes out of the box with support for creating AMIs (EC2), VMware images, and
VirtualBox images. Support for more platforms can be added via plugins.

The images that Packer creates can easily be turned into Vagrant boxes.

%prep
cd %{_builddir}
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}
cd %{name}-%{version}
/usr/bin/unzip %{_sourcedir}/%{version}_linux_amd64.zip

%build

%install
# vim syntax files
mkdir -p %{buildroot}%{_bindir}/
cd %{_builddir}/%{name}-%{version}
cp packer* %{buildroot}%{_bindir}/

%files
%{_bindir}/packer*
