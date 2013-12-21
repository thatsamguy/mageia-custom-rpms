%define	fver 1.2.0

%define	major 1
%define libname %mklibname mbfl %{major}
%define develname %mklibname mbfl -d

Summary:	Streamable kanji code filter and converter
Name:		libmbfl
Version:	1.2.0
Release:	%mkrel 7
License:	LGPL
Group:		System/Libraries
URL:		http://sourceforge.jp/projects/php-i18n/
Source0:	http://osdn.dl.sourceforge.jp/php-i18n/18570/%{name}-%{fver}.tar.gz
Source100:	ftp://ftp.unicode.org/Public/UNIDATA/EastAsianWidth.txt
Source101:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-1.TXT
Source102:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-2.TXT
Source103:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-3.TXT
Source104:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-4.TXT
Source105:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-5.TXT
Source106:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-6.TXT
Source107:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-7.TXT
Source108:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-8.TXT
Source109:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-9.TXT
Source110:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-10.TXT
Source111:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-11.TXT
Source113:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-13.TXT
Source114:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-14.TXT
Source115:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-15.TXT
Source116:	ftp://ftp.unicode.org/Public/MAPPINGS/ISO8859/8859-16.TXT
Patch0:		libmbfl-1.2.0-php-5.4.10.diff
Patch1:		automake.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool

%description
This is Libmbfl, a streamable multibyte character code filter and converter
library.

%package -n	%{libname}
Summary:	Streamable kanji code filter and converter library
Group:          System/Libraries

%description -n	%{libname}
This is Libmbfl, a streamable multibyte character code filter and converter
library.

This package provides the shared mbfl library.

%package -n	%{develname}
Summary:	Static library and header files for development with mbfl
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	mbfl-devel = %{version}-%{release}
Obsoletes:	mbfl-devel

%description -n	%{develname}
This is Libmbfl, a streamable multibyte character code filter and converter
library.

This package is only needed if you plan to develop or compile applications
which requires the mbfl library.

%prep
%setup -q -n %{name}-%{fver}
%patch0 -p1
%patch1 -p1 -b .automake
cp %{SOURCE100} mbfl/
cp %{SOURCE101} %{SOURCE102} %{SOURCE103} %{SOURCE104} %{SOURCE105} \
   %{SOURCE106} %{SOURCE107} %{SOURCE108} %{SOURCE109} %{SOURCE110} \
   %{SOURCE111} %{SOURCE113} %{SOURCE114} %{SOURCE115} %{SOURCE116} \
   filters

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

chmod 644 AUTHORS DISCLAIMER LICENSE README

%build
touch NEWS ChangeLog COPYING
autoreconf -fi
%configure2_5x --disable-static
%make

%install
%makeinstall_std
rm -f %{buildroot}%{_libdir}/*.la

%files -n %{libname}
%doc AUTHORS DISCLAIMER LICENSE README
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/mbfl
%{_libdir}/*.so
