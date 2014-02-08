# TODO
# - subpackage for each driver
%define		luaver 5.1
%define		lualibdir %{_libdir}/lua/%{luaver}
%define		luapkgdir %{_datadir}/lua/%{luaver}
Summary:	Database interface library for Lua
Name:		lua-dbi
Version:	0.5
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	http://luadbi.googlecode.com/files/luadbi.%{version}.tar.gz
# Source0-md5:	ede2b003aadddc151aac87050c3d926e
URL:		http://code.google.com/p/luadbi
Patch1:		%{name}-0.5-pgsql_transaction.patch
BuildRequires:	lua51-devel
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
%setup -qc
%patch1 -p1
find . -name \*.[ch] -print -exec chmod -x '{}' \;
sed -i -e '1d' DBI.lua

%{__sed} -i -e 's,-O2,$(EXTRA_CFLAGS),' Makefile

%build
%{__make} \
	LIBDIR="%{_libdir}" \
	CC="%{__cc}" \
	EXTRA_CFLAGS="%{rpmcflags} %{rpmcppflags} -I/usr/include/lua51 -I/usr/include/postgresql/internal -I/usr/include/postgresql/server"
	COMMON_LDFLAGS="%{rpmldflags} -llua51 -shared"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{luapkgdir},%{lualibdir}}
install -p *.so $RPM_BUILD_ROOT%{lualibdir}
cp -p *.lua $RPM_BUILD_ROOT%{luapkgdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README COPYING
%{lualibdir}/dbdmysql.so
%{lualibdir}/dbdpostgresql.so
%{lualibdir}/dbdsqlite3.so
%{luapkgdir}/DBI.lua
