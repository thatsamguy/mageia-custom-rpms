%define name rust
%define version 0.8
%define release %mkrel 0.1

Summary:	A safe, concurrent, practical programming language
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://static.rust-lang.org/dist/%{name}-%{version}.tar.gz
License:	MIT
Group:		Development
Url:		http://www.rust-lang.org/

BuildRequires:  python < 3.0

%description
Rust is a curly-brace, block-structured expression language. It
visually resembles the C language family, but differs significantly
in syntactic and semantic details. Its design is oriented toward
concerns of "programming in the large", that is, of creating and
maintaining boundaries - both abstract and operational - that
preserve large-system integrity, availability and concurrency.

It supports a mixture of imperative procedural, concurrent actor,
object-oriented and pure functional styles. Rust also supports
generic programming and metaprogramming, in both static and dynamic
styles. 

%package -n vim-rust
Group:          Editors
Summary:        Syntax highlighting for rust in vim

%description -n vim-rust
The vim-rust package provides filetype detection and syntax highlighting for
the rust programming language.

%package -n kate-rust
Group:          Editors
Summary:        Syntax highlighting for rust in kate

%description -n kate-rust
The kate-rust package provides filetype detection and syntax highlighting for
the rust programming language.

%prep
%setup -q

%build
#export RUST_LOG=rustc=1;
./configure \
	--prefix=%{_prefix}
%make

%install
%makeinstall_std

# vim syntax files
vimdir=%{buildroot}%{_datadir}/vim
mkdir -vp %{buildroot}%{_datadir}/vim
cp -vr src/etc/vim/* $vimdir/

# kate syntax files
mkdir -vp %{buildroot}%{_datadir}/apps/katepart/syntax/
cp -v src/etc/kate/rust.xml %{buildroot}%{_datadir}/apps/katepart/syntax/

%files
%{_bindir}/rust
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_bindir}/rusti
%{_bindir}/rustpkg
%{_prefix}/lib/rustc
%{_prefix}/lib/l*
%{_mandir}/man*/*

%files -n vim-rust
%{_datadir}/vim/*

%files -n kate-rust
%{_datadir}/apps/katepart/syntax/rust.xml
