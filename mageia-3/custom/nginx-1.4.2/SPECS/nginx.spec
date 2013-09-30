%define nginx_user nginx
%define nginx_group %{nginx_user}
%define nginx_home /var/lib/nginx
%define nginx_home_tmp %{nginx_home}/tmp
%define nginx_logdir /var/log/nginx
%define nginx_confdir %{_sysconfdir}/nginx
%define nginx_datadir %{_datadir}/nginx
%define nginx_webroot %{nginx_datadir}/html

Summary:	Robust, small and high performance http and reverse proxy server
Name:		nginx
Version:	1.4.2
Release:	%mkrel 0.2
Group:		System/Servers
# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:	BSD
URL:		http://nginx.net/
Source0:	http://nginx.org/download/nginx-%{version}.tar.gz
Source1:	http://nginx.org/download/nginx-%{version}.tar.gz.asc
Source2:	%{name}-tmpfiles.conf
Source3:	%{name}.logrotate
Source4:	%{name}.sysconfig
Source5:	%{name}.service

Source6:    nginx.conf
Source7:    default.conf
Source8:    ssl.conf
Source9:    virtual.conf
Source100:	index.html
Source102:	nginx-logo.png
Source103:	50x.html
Source104:	404.html

Requires(post):  rpm-helper >= 0.24.8-1
Requires(preun): rpm-helper >= 0.24.8-1
BuildRequires:  GeoIP-devel
BuildRequires:  gd-devel
BuildRequires:  libxslt-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	zlib-devel
BuildRequires:	perl-devel
BuildRequires:	perl(ExtUtils::Embed)
Requires:	pcre
Requires:	openssl
Provides:	webserver

%description
Nginx [engine x] is an HTTP(S) server, HTTP(S) reverse proxy and IMAP/POP3
proxy server written by Igor Sysoev.

%prep
%setup -q

%build
%serverbuild
# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.  The configure script(s) have been patched (Patch1 and
# Patch2) in order to support installing into a build environment.
export DESTDIR=%{buildroot}
./configure \
    --prefix=%{nginx_datadir} \
    --sbin-path=%{_sbindir}/%{name} \
    --conf-path=%{nginx_confdir}/%{name}.conf \
    --error-log-path=%{nginx_logdir}/error.log \
    --http-log-path=%{nginx_logdir}/access.log \
    --http-client-body-temp-path=%{nginx_home_tmp}/client_body \
    --http-proxy-temp-path=%{nginx_home_tmp}/proxy \
    --http-fastcgi-temp-path=%{nginx_home_tmp}/fastcgi \
    --http-uwsgi-temp-path=%{nginx_home_tmp}/uwsgi \
    --http-scgi-temp-path=%{nginx_home_tmp}/scgi \
    --pid-path=/var/run/%{name}/%{name}.pid \
    --lock-path=/run/lock/subsys/%{name} \
    --user=%{nginx_user} \
    --group=%{nginx_group} \
    --with-file-aio \
    --with-ipv6 \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_xslt_module \
    --with-http_image_filter_module \
    --with-http_geoip_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gzip_static_module \
    --with-http_gunzip_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_degradation_module \
    --with-http_stub_status_module \
    --with-http_perl_module \
    --with-http_spdy_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-cc-opt="$CFLAGS $(pcre-config --cflags)" 

%make

%install
rm -rf %{buildroot}

%makeinstall_std INSTALLDIRS=vendor

%{__install} -D -p -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%{__install} -d -m 755 %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE5} %{buildroot}%{_unitdir}

%{__install} -d -m 0755 %{buildroot}%{nginx_confdir}
%{__install} -m 644 %{SOURCE6} %{buildroot}%{nginx_confdir}

%{__install} -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d
%{__install} -m 644 %{SOURCE7} %{SOURCE8} %{SOURCE9} \
    %{buildroot}%{nginx_confdir}/conf.d

%{__install} -d -m 0755 %{buildroot}%{nginx_home_tmp}
%{__install} -d -m 0755 %{buildroot}%{nginx_logdir}
%{__install} -d -m 0755 %{buildroot}%{nginx_webroot}

%{__install} -p -m 0644 %{SOURCE100} %{SOURCE102} %{SOURCE103} %{SOURCE104} \
    %{buildroot}%{nginx_webroot}

# add current version
perl -pi -e "s|_VERSION_|%{version}|g" %{buildroot}%{nginx_webroot}/index.html

# convert to UTF-8 all files that give warnings.
for textfile in CHANGES; do
    mv $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    rm -f $textfile.old
done

install -d %{buildroot}%{_mandir}/man8
install -m0644 man/*.8 %{buildroot}%{_mandir}/man8/

%pre
%_pre_useradd %{nginx_user} %{nginx_home} /bin/false

%post
%_tmpfilescreate %{name}
%_post_service %{nginx_user}

%preun
%_preun_service %{nginx_user}

%postun
%_postun_userdel %{nginx_user}

%files
%doc LICENSE CHANGES README
%{nginx_datadir}
%{_sbindir}/%{name}
%{_mandir}/man3/%{name}.3pm*
%{_mandir}/man8/*
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%dir %{nginx_confdir}
%dir %{nginx_confdir}/conf.d
%config(noreplace) %{nginx_confdir}/conf.d/*.conf
%config(noreplace) %{nginx_confdir}/win-utf
%config(noreplace) %{nginx_confdir}/%{name}.conf.default
%config(noreplace) %{nginx_confdir}/scgi_params
%config(noreplace) %{nginx_confdir}/scgi_params.default
%config(noreplace) %{nginx_confdir}/fastcgi.conf
%config(noreplace) %{nginx_confdir}/fastcgi.conf.default
%config(noreplace) %{nginx_confdir}/mime.types.default
%config(noreplace) %{nginx_confdir}/fastcgi_params
%config(noreplace) %{nginx_confdir}/fastcgi_params.default
%config(noreplace) %{nginx_confdir}/koi-win
%config(noreplace) %{nginx_confdir}/koi-utf
%config(noreplace) %{nginx_confdir}/%{name}.conf
%config(noreplace) %{nginx_confdir}/mime.types
%config(noreplace) %{nginx_confdir}/uwsgi_params
%config(noreplace) %{nginx_confdir}/uwsgi_params.default
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{perl_vendorarch}/auto/%{name}
%{perl_vendorarch}/%{name}.pm
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_home}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_home_tmp}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_logdir}
