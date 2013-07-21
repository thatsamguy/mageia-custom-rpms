%define oname   puppet-lint

Name:       %{oname}
Version:    0.3.2
Release:    %mkrel 0.1
Summary:    Ensure your Puppet manifests conform with the Puppetlabs style guide
License:    Apache License 
Group:      Development/Ruby
URL:        https://github.com/rodjek/puppet-lint/
Source0:    http://rubygems.org/gems/%{oname}-%{version}.gem
BuildRequires: rubygems
BuildArch:  noarch

%description
Checks your Puppet manifests against the Puppetlabs
style guide and alerts you to any discrepancies.

%package        doc
Summary:    Documentation for %{name}
Group:      Development/Ruby

%description    doc
Documents, Rdoc & RI documentation for %{name}.

%prep
%setup -q
tar xmf data.tar.gz

%build
%gem_build

%install
%gem_install

%files
%{_bindir}/puppet-lint
%{ruby_gemdir}/gems/%{oname}-%{version}
%{ruby_gemdir}/specifications/%{oname}-%{version}.gemspec

%files          doc
%doc %{ruby_gemdir}/doc/%{oname}-%{version}
