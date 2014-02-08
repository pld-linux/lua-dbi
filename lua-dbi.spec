%define luaver 5.1
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}

Summary:	Database interface library for Lua
Name:		lua-dbi
Version:	0.5
Release:	1
License:	MIT
Group:		Development/Libraries
URL:		http://code.google.com/p/luadbi
Source0:	http://luadbi.googlecode.com/files/luadbi.%{version}.tar.gz
Patch1:		%{name}-0.5-pgsql_transaction.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	lua51-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:  postgresql-backend-devel
BuildRequires:	sqlite3-devel

%description
LuaDBI is a database interface library for Lua. It is designed to
provide a RDBMS agnostic API for handling database operations. LuaDBI
also provides support for prepared statement handles, placeholders and
bind parameters for all database operations.

Currently LuaDBI supports DB2, Oracle, MySQL, PostgreSQL and SQLite
databases with native database drivers.

%prep
%setup -q -c
%patch1 -p1
find . -name \*.[ch] -print -exec chmod -x '{}' \;
sed -i -e '1d' DBI.lua

%build
%{__make} LIBDIR="%{_libdir}" CFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/lua51 -I. -I/usr/include/mysql/ -I/usr/include/postgresql/internal/ -I/usr/include/postgresql/server/" COMMON_LDFLAGS="-llua51 -shared"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{luapkgdir}
install -d $RPM_BUILD_ROOT%{lualibdir}

cp -p *.so $RPM_BUILD_ROOT%{lualibdir}
cp -p *.lua $RPM_BUILD_ROOT%{luapkgdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README COPYING
%{lualibdir}/*.so
%{luapkgdir}/*.lua
