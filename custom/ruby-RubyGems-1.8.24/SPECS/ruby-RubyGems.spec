%define rname	RubyGems
%define	oname	rubygems

Summary:	Ruby package manager
Name:		ruby-%{rname}
Version:	1.8.24
Release:	%mkrel 0.1
License:	GPL
Group:		Development/Ruby
URL:		http://docs.rubygems.org/
Source0:	http://rubyforge.org/frs/download.php/76073/%{oname}-%{version}.tgz
# Sources from the works by Vít Ondruch <vondruch@redhat.com>
# https://github.com/rubygems/rubygems/issues/120
# rubygems-Patches-28631
Patch1:	rubygems-1.8.6-show-extension-build-process-in-sync.patch
# rubygems-Patches-29049
# https://github.com/rubygems/rubygems/issues/118
Patch3:	rubygems-1.8.5-show-rdoc-process-verbosely.patch
# Patches from the works by Vít Ondruch <vondruch@redhat.com>
# Fix the uninstaller, so that it doesn't say that gem doesn't exist
# when it exists outside of the GEM_HOME (already fixed in the upstream)
Patch105:	ruby-1.9.3-rubygems-1.8.11-uninstaller.patch
# Add support for installing binary extensions according to FHS.
# https://github.com/rubygems/rubygems/issues/210
Patch109:	rubygems-1.8.11-binary-extensions.patch
BuildArch:	noarch
BuildRequires:	ruby
Requires:	locales
Requires:	ruby
Requires:	rubygem(rdoc)
Provides:	%{oname} = %{version}
Provides:	ruby(rubygems) = %{version}-%{release}

%description
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%prep
%setup -q -n rubygems-%{version}

%patch1 -p1 -b .insync
%patch3 -p1 -b .rdoc_v
%patch105 -p1 -b .uninst
%patch109 -p1 -b .bindir


# gems are installed in /usr/lib even on x86_64 
%__sed -ie "s,ConfigMap\[:libdir\],\'/usr/lib\'," lib/rubygems/defaults.rb

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{ruby_gemdir}
ruby setup.rb --prefix=%{buildroot}/%{_prefix}
mkdir -p %{buildroot}%{ruby_sitelibdir}
mv %{buildroot}/%{_prefix}/lib/{*.rb,rubygems,rbconfig} %{buildroot}%{ruby_sitelibdir}

for f in `find %{buildroot}%{ruby_sitelibdir} -name \*.rb`
do
	if head -n1 "$f" | grep '^#!' >/dev/null;
	then
		sed -i 's|/usr/local/bin|/usr/bin|' "$f"
		chmod 0755 "$f"
	else
		chmod 0644 "$f"
	fi
done

# use system cert.pem instead of bundled copy
mkdir -p %{buildroot}%{ruby_sitelibdir}/rubygems/ssl_certs
ln -sf %{_sysconfdir}/pki/tls/cert.pem \
       %{buildroot}%{ruby_sitelibdir}/rubygems/ssl_certs/ca-bundle.pem


%clean
rm -rf %{buildroot}

%files
%doc README*
%attr(755,root,root) %{_bindir}/*
%{ruby_sitelibdir}/*
%{ruby_gemdir}
