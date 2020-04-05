# TODO
# - subpackage for each driver
%define		luaver 5.3
%define		real_name luadbi

%define		luasuffix %(echo %{luaver} | tr -d .)
%if "%{luaver}" == "5.1"
%define		luaincludedir %{_includedir}/lua51
%else
%define		luaincludedir %{_includedir}/lua%{luaver}
%endif
%define		lualibdir %{_libdir}/lua/%{luaver}
%define		luapkgdir %{_datadir}/lua/%{luaver}

Summary:	Database interface library for Lua
Name:		lua%{luasuffix}-dbi
Version:	0.7.2
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	https://github.com/mwild1/luadbi/archive/v%{version}/%{real_name}-%{version}.tar.gz
# Source0-md5:	8e80fdc9ea25845c17e9268b75980b85
URL:		https://github.com/mwild1/luadbi
Patch0:		makefile.patch
BuildRequires:	lua%{luasuffix}-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LuaDBI is a database interface library for Lua. It is designed to
provide a RDBMS agnostic API for handling database operations. LuaDBI
also provides support for prepared statement handles, placeholders and
bind parameters for all database operations.

Currently LuaDBI supports DB2, Oracle, MySQL, PostgreSQL and SQLite
databases with native database drivers.

%prep
%setup -q -n %{real_name}-%{version}
%patch0 -p1
find . -name \*.[ch] -print -exec chmod -x '{}' \;
sed -i -e '1d' DBI.lua

%build
%{__make} free \
	LIBDIR="%{_libdir}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	LUA_V="%{luaver}" \
	LUA_INC="-I%{luaincludedir}" \
	LUA_LDIR="%{luapkgdir}" \
	LUA_CDIR="%{lualibdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{luapkgdir},%{lualibdir}}

%{__make} install_free \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR="%{_libdir}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	LUA_V="%{luaver}" \
	LUA_INC="-I%{luaincludedir}" \
	LUA_LDIR="%{luapkgdir}" \
	LUA_CDIR="%{lualibdir}"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md COPYING
%dir %{lualibdir}/dbd
%{lualibdir}/dbd/mysql.so
%{lualibdir}/dbd/postgresql.so
%{lualibdir}/dbd/sqlite3.so
%{luapkgdir}/DBI.lua
