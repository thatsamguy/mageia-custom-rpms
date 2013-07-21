Name:		nodejs
Version:	0.8.9
Release:	%mkrel 0.1
Summary:	Evented Server-Side Javascript
Group:		System/Servers
License:	BSD
URL:		http://nodejs.org
Source0:	http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz
BuildRequires:	v8-devel
BuildRequires:	libev-devel
BuildRequires:	c-ares-devel
BuildRequires:	scons
BuildRequires:	openssl-devel
Provides:	npm = %{version}-%{release}

%description
Node's goal is to provide an easy way to build scalable network programs.

%prep
%setup -q -n node-v%{version}

%build
#FIXME: some CFLAGS do not seem to be recognized :/
#FIXME: does not build with --shared-libev
./configure	--prefix=%{_prefix} \
		--shared-v8 \
		--openssl-use-sys \
		--shared-zlib

%make

%install
%makeinstall_std

%files
%{_bindir}/node*
%{_bindir}/npm
%{_prefix}/lib/node_modules
%{_prefix}/lib/node
%{_prefix}/lib/dtrace
%{_includedir}/node
%{_mandir}/man1/node.1.*
