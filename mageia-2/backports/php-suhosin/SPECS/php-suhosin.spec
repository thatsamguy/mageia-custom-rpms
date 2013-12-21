%define modname suhosin
%define soname %{modname}.so
%define inifile Z98_%{modname}.ini

Summary:	Suhosin extension module for PHP
Name:		php-%{modname}
Version:	0.9.34
Release:	%mkrel 0.0.git1fba865.4
Group:		Development/PHP
License:	PHP License
URL:		http://www.hardened-php.net/suhosin/
#Source0:	http://download.suhosin.org/%{modname}-%{version}.tgz
#Source1:	http://download.suhosin.org/%{modname}-%{version}.tgz.sig
Source0:        stefanesser-suhosin-1fba865.tar.gz
# https://github.com/stefanesser/suhosin/pull/26
Patch0:		0001-Fix-saving-sessions-in-PHP-5.4-with-user-session-han.patch
BuildRequires:	php-devel >= 3:5.4.0

%description
Suhosin is an advanced protection system for PHP installations. It was designed
to protect servers and users from known and unknown flaws in PHP applications
and the PHP core. Suhosin is binary compatible to normal PHP installation,
which means it is compatible to 3rd party binary extension like ZendOptimizer.

%prep

# %setup -q -n %{modname}-%{version}
%setup -q -n stefanesser-suhosin-1fba865
%apply_patches

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so %{modname}.so

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 suhosin.ini %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%clean
rm -rf %{buildroot}

%files 
%doc CREDITS tests Changelog
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


