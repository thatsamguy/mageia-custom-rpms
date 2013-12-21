%define modname timezonedb
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A60_%{modname}.ini

# (tpg) define release here
%define release %mkrel 1

Summary:	Timezone Database to be used with PHP's date and time functions
Name:		php-%{modname}
Version:	2013.8
Release:	%{release}
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/timezonedb/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.4.3
BuildRequires:	file
Epoch:		3


%description
This extension is a drop-in replacement for the builtin timezone database that
comes with PHP. You should only install this extension in case you need to get
a later version of the timezone database than the one that ships with PHP.

The data that this extension uses comes from the "Olson" database, which is
located at ftp://elsie.nci.nih.gov/pub/.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

mv modules/*.so .

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


