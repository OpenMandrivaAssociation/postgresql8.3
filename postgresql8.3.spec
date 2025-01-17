%if %_lib == lib64
%define _requires_exceptions devel(libtcl8.4(64bit))
%else
%define _requires_exceptions devel(libtcl8.4)
%endif

%define Werror_cflags %nil

%define perl_version %(rpm -q --qf "%{VERSION}" perl)
%define perl_epoch %(rpm -q --qf "%{EPOCH}" perl)

%define pgdata /var/lib/pgsql
%define logrotatedir %{_sysconfdir}/logrotate.d

%define major 5
%define major_ecpg 6

%define bname postgresql
%define current_major_version 8.3
%define current_minor_version 15

# Define if it's a beta
# %%define beta RC2

# define the mdv release
%define rel 1

%define release %mkrel %{?beta:0.rc.%{beta}.}%{rel}

%define libname %mklibname pq%{current_major_version} _%{major}
%define libecpg %mklibname ecpg%{current_major_version} _%{major_ecpg}

Summary: 	PostgreSQL client programs and libraries
Name:		%{bname}%{current_major_version}
Version: 	%{current_major_version}%{?!beta:.%{current_minor_version}}
Release: 	%release
License:	BSD
Group:		Databases
URL:		https://www.postgresql.org/ 
Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}%{?beta}.tar.bz2
Source5:	ftp://ftp.postgresql.orga/pub/source/v%{version}/postgresql-%{version}%{?beta}.tar.bz2.md5
Source10:   postgres.profile
Source11:	postgresql.init
Source13:	postgresql.mdv.releasenote
Requires:	perl
Provides:	postgresql-clients = %{version}-%{release}
BuildRequires:	bison flex
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	tcl-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	zlib-devel
BuildRequires:  ossp_uuid-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:	%{bname}-virtual = %{current_major_version}
Conflicts:	%{bname}-virtual < %{current_major_version}
Requires:	%{libname} = %{version}
Provides:	%{bname} = %{version}-%{release}

%description
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). The
postgresql package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server.  These PostgreSQL
client programs are programs that directly manipulate the internal
structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL
server, or may be on a remote machine which accesses a PostgreSQL
server over a network connection. This package contains the client
libraries for C and C++, as well as command-line utilities for
managing PostgreSQL databases on a PostgreSQL server. 

If you want to manipulate a PostgreSQL database on a remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.

%package -n	%{libname}
Summary:	The shared libraries required for any PostgreSQL clients
Group:		System/Libraries
Provides:	postgresql-libs = %{version}-%{release}
Provides:	libpq = %{version}-%{release}
Provides:	%{mklibname pq}-virtual = %{current_major_version}
Conflicts:	libpq < %{current_major_version}
# Avoid conflicts with lib having bad major
Conflicts:  libpq3 = 8.0.2

%description -n	%{libname}
C and C++ libraries to enable user programs to communicate with the
PostgreSQL database backend. The backend can be on another machine and
accessed through TCP/IP.


%package -n	%{libecpg}
Summary:	Shared library libecpg for PostgreSQL
Group:		System/Libraries
Requires:	postgresql%{current_major_version} = %{version}-%{release}
Provides:	libecpg = %{version}-%{release}
Provides:	%{mklibname ecpg}-virtual = %{current_major_version}
Conflicts:	libecpg < %{current_major_version}

%description -n	%{libecpg}
Libecpg is used by programs built with ecpg (Embedded PostgreSQL for C)
Use postgresql-dev to develop such programs.

%package	server
Summary:	The programs needed to create and run a PostgreSQL server
Group:		Databases
Provides:	sqlserver
Requires(post):   %{libname} >= %{version}-%{release}
Requires(preun):   %{libname} >= %{version}-%{release}
# add/remove services
Requires(post): rpm-helper
Requires(preun): rpm-helper
# add/del user
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	postgresql%{current_major_version} >= %{version}-%{release}
Requires(post):	postgresql%{current_major_version} >= %{version}-%{release}
Conflicts:	postgresql < 7.3
Provides: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-server-virtual = %{current_major_version}
Conflicts: %{bname}-server-virtual < %{current_major_version}
Provides: %{bname}-server = %{version}-%{release}

%description	server
The postgresql-server package includes the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.  PostgreSQL is an advanced
Object-Relational database management system (DBMS) that supports
almost all SQL constructs (including transactions, subselects and
user-defined types and functions). You should install
postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need
to install the postgresql and postgresql-devel packages.

After installing this package, please read postgresql.mdv.releasenote.

%package	docs
Summary:	Extra documentation for PostgreSQL
Group:		Databases
Provides: %{bname}-docs-virtual = %{current_major_version}
Conflicts: %{bname}-docs-virtual < %{current_major_version}

%description	docs
The postgresql-docs package includes the SGML source for the documentation
as well as the documentation in other formats, and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package	contrib
Summary:	Contributed binaries distributed with PostgreSQL
Group:		Databases
Requires:   postgresql%{current_major_version}-server = %{version}-%{release}
Provides: %{bname}-contrib-virtual = %{current_major_version}
Conflicts: %{bname}-contrib-virtual < %{current_major_version}

%description	contrib
The postgresql-contrib package includes the contrib tree distributed with
the PostgreSQL tarball.  Selected contrib modules are prebuilt.

%package	devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Databases
Requires:	postgresql%{current_major_version} = %{version}-%{release}
Provides: %{bname}-devel-virtual = %{current_major_version}
Conflicts: %{bname}-devel-virtual < %{current_major_version}
Requires:	%{libname} = %{version}-%{release}
Provides:	postgresql-libs-devel = %{version}-%{release}
Provides:   libpq-devel = %{version}-%{release}
Provides:       pq-devel = %{version}-%{release}
# Avoid conflicts with lib having bad major
Conflicts:  libpq3-devel = 8.0.2
Provides:   %{_lib}pq-devel = %{current_major_version}
Conflicts:  %{_lib}pq-devel < %{current_major_version}
Requires:	%{libecpg} = %{version}-%{release}
Provides:	libecpg-devel = %{version}-%{release} 
Provides:   %{_lib}ecpg-devel = %{version}-%{release}
Conflicts:  %mklibname -d ecpg 5
Conflicts:  %mklibname -d pq 5
Conflicts:  %mklibname -d pq8.3
Conflicts:  %mklibname -d ecpg8.3
Provides:   %{bname}-devel = %{version}-%{release}

%description	devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. If
you're installing postgresql-server, you need to install this
package.

%package	pl
Summary:	Procedurals languages for PostgreSQL
Group:		Databases
Conflicts:	libpgsql2
Requires:	%{name}-plpython = %{version}-%{release} 
Requires:	%{name}-plperl = %{version}-%{release} 
Requires:	%{name}-pltcl = %{version}-%{release} 
Requires:	%{name}-plpgsql = %{version}-%{release} 
Provides: %{bname}-pl-virtual = %{current_major_version}
Conflicts: %{bname}-pl-virtual < %{current_major_version}
Provides:  %{bname}-pl = %{version}-%{release}

%description	pl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pl will install the the PL/Perl,
PL/Tcl, and PL/Python procedural languages for the backend.
PL/Pgsql is part of the core server package.

%package    plpython
Summary:    The PL/Python procedural language for PostgreSQL
Group:      Databases
Requires:   postgresql%{current_major_version}-server = %{version}
Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-plpython-virtual = %{current_major_version}
Conflicts: %{bname}-plpython-virtual < %{current_major_version}

%description	plpython
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-plpython package contains the the PL/Python
procedural languages for the backend. PL/Python is part of the core 
server package.


%package    plperl
Summary:    The PL/Perl procedural language for PostgreSQL
Group:      Databases
Requires:   postgresql%{current_major_version}-server = %{version}
Requires:   perl-base = %{perl_epoch}:%{perl_version}
Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-plperl-virtual = %{current_major_version}
Conflicts: %{bname}-plperl-virtual < %{current_major_version}
Provides:  %{bname}-plperl = %{version}-%{release}

%description	plperl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-plperl package contains the the PL/Perl
procedural languages for the backend. PL/Perl is part of the core 
server package.

%package    pltcl
Summary:    The PL/Tcl procedural language for PostgreSQL
Group:      Databases
Requires:   postgresql%{current_major_version}-server = %{version}
Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-pltcl-virtual = %{current_major_version}
Conflicts: %{bname}-pltcl-virtual < %{current_major_version}
Provides:  %{bname}-pltcl = %{version}-%{release}

%description	pltcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pltcl package contains the the PL/Tcl
procedural languages for the backend. PL/Tcl is part of the core 
server package.


%package    plpgsql
Summary:    The PL/PgSQL procedural language for PostgreSQL
Group:      Databases
Requires:   postgresql%{current_major_version}-server = %{version}
Conflicts:  postgresql-pl < %version-%release
Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-plpgsql-virtual = %{current_major_version}
Conflicts: %{bname}-plpgsql-virtual < %{current_major_version}
Provides:  %{bname}-plpgsql = %{version}-%{release}

%description	plpgsql
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-plpgsql package contains the the PL/PgSQL
procedural languages for the backend. PL/PgSQL is part of the core 
server package.

%prep
%setup -q -n %{bname}-%{version}%{?beta}

%build
%serverbuild
%configure2_5x \
        --disable-rpath \
        --enable-hba \
	    --enable-locale \
	    --enable-multibyte \
	    --enable-syslog\
	    --with-CXX \
	    --enable-odbc \
	    --with-perl \
	    --with-python \
        --with-tcl --with-tclconfig=%{_libdir} \
        --without-tk \
        --with-openssl \
        --with-pam \
        --with-libxml \
        --with-libxslt \
        --libdir=%{_libdir} \
        --with-docdir=%{_docdir} \
        --mandir=%{_mandir} \
        --prefix=%_prefix \
        --sysconfdir=%{_sysconfdir}/pgsql \
        --enable-nls \
        --with-ossp-uuid

# $(rpathdir) come from Makefile
perl -pi -e 's|^all:|LINK.shared=\$(COMPILER) -shared -Wl,-rpath,\$(rpathdir),-soname,\$(soname)\nall:|' src/pl/plperl/GNUmakefile


%make all
%make -C contrib all

pushd src/test
make all
popd

%check
make check

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install 
make -C contrib DESTDIR=$RPM_BUILD_ROOT install

# install odbcinst.ini
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pgsql

# copy over Makefile.global to the include dir....
#install -m755 src/Makefile.global $RPM_BUILD_ROOT%{_includedir}/pgsql/

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/backups

# Create the multiple postmaster startup directory
install -d -m 700 $RPM_BUILD_ROOT/etc/sysconfig/pgsql

%if 0
# tests. There are many files included here that are unnecessary, but include
# them anyway for completeness.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pgsql/test
cp -a src/test/regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test
install -m 0755 contrib/spi/refint.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
install -m 0755 contrib/spi/autoinc.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
pushd  $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/
strip *.so
popd
%endif

mkdir -p %buildroot/var/log/postgres

mkdir -p %buildroot%logrotatedir
cat > %buildroot%logrotatedir/%{bname} <<EOF
/var/log/postgres/postgresql {
    notifempty
    missingok
    copytruncate
}
EOF

install -D -m755 %{SOURCE11} $RPM_BUILD_ROOT%{_initrddir}/postgresql

mv $RPM_BUILD_ROOT%{_docdir}/%{bname}/html $RPM_BUILD_ROOT%{_docdir}/%{name}-docs-%{version}

%find_lang libpq
%find_lang libecpg
%find_lang pg_dump
%find_lang postgres
%find_lang psql
%find_lang pg_resetxlog
%find_lang pg_controldata
%find_lang pgscripts
%find_lang initdb
%find_lang pg_config
%find_lang pg_ctl

cat pg_ctl.lang initdb.lang pg_config.lang psql.lang pg_dump.lang pgscripts.lang > main.lst
cat postgres.lang pg_resetxlog.lang pg_controldata.lang > server.lst
# 20021226 warly waiting to be able to add a major in po name
cat libpq.lang libecpg.lang >> main.lst

# taken directly in build dir.
rm -fr $RPM_BUILD_ROOT%{_datadir}/doc/postgresql/contrib/

mkdir -p %buildroot/%_sys_macros_dir
cat > %buildroot/%_sys_macros_dir/%{name}.macros <<EOF
%%postgresql_version %{version}
%%postgresql_major   %{current_major_version}
%%postgresql_minor   %{current_minor_version}
%%pgmodules_req Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
EOF

cat %{SOURCE13} > postgresql.mdv.releasenote
cat > README.urpmi <<EOF
You just installed or update %{bname} server.
You can found important informations about mandriva %{bname} rpms and database
management in:

%{_defaultdocdir}/%{name}-server/postgresql.mdv.releasenote

Please, read it.
EOF

# postgres' .profile and .bashrc
install -D -m 700 %SOURCE10 $RPM_BUILD_ROOT/var/lib/pgsql/.profile
(
cd $RPM_BUILD_ROOT/var/lib/pgsql/
ln -s .profile .bashrc
)

cat > %buildroot%_sysconfdir/sysconfig/postgresql <<EOF
# Olivier Thauvin <nanardon@mandriva.org>

# The database location:
# You probably won't change this
# PGDATA=/var/lib/pgsql/data

# What is the based locales for postgresql
# Setting locales to C allow to use any encoding
# ISO or UTF, any other choice will restrict you
# either ISO or UTF.
LC_ALL=C

EOF

%pre server
%_pre_useradd postgres /var/lib/pgsql /bin/bash

[ ! -f %pgdata/data/PG_VERSION ] && exit 0
[ `cat %pgdata/data/PG_VERSION` = %{current_major_version} ] && exit 0

%if %mdkversion < 200900
%post server -p /sbin/ldconfig
%endif

%posttrans server

%_post_service %{bname}

%preun server
%_preun_service %{bname}

%postun server
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%_postun_userdel postgres

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libecpg} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libecpg} -p /sbin/ldconfig
%endif

%clean
[ $RPM_BUILD_ROOT != '/' ] && rm -rf $RPM_BUILD_ROOT

%files -f main.lst 
%defattr(-,root,root)
%doc doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createlang.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/droplang.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man1/reindexdb.*
%{_mandir}/man7/*
%_sys_macros_dir/%{name}.macros

%files -n %{libname} 
%defattr(-,root,root)
%{_libdir}/libpq.so.%{major}*

%files -n %{libecpg}
%defattr(-,root,root)
%{_libdir}/libecpg.so.%{major_ecpg}*
%{_libdir}/libecpg_compat.so.*
%{_libdir}/libpgtypes.so.*

%files docs
%defattr(-,root,root)
%doc %{_docdir}/%{name}-docs-%{version}

%files contrib
%defattr(-,root,root)
%doc contrib/*/README.* contrib/spi/*.example
%{_libdir}/postgresql/_int.so
%{_libdir}/postgresql/btree_gist.so
%{_libdir}/postgresql/chkpass.so
%{_libdir}/postgresql/cube.so
%{_libdir}/postgresql/dblink.so
%{_libdir}/postgresql/earthdistance.so
%{_libdir}/postgresql/fuzzystrmatch.so
%{_libdir}/postgresql/insert_username.so
%{_libdir}/postgresql/int_aggregate.so
%{_libdir}/postgresql/lo.so
%{_libdir}/postgresql/ltree.so
%{_libdir}/postgresql/moddatetime.so
%{_libdir}/postgresql/pgcrypto.so
%{_libdir}/postgresql/pgstattuple.so
%{_libdir}/postgresql/refint.so
%{_libdir}/postgresql/seg.so
%{_libdir}/postgresql/tablefunc.so
%{_libdir}/postgresql/timetravel.so
%{_libdir}/postgresql/pg_trgm.so
%{_libdir}/postgresql/autoinc.so
%{_libdir}/postgresql/pg_buffercache.so
%{_libdir}/postgresql/adminpack.so
%{_libdir}/postgresql/hstore.so
%{_libdir}/postgresql/isn.so
%{_libdir}/postgresql/pg_freespacemap.so
%{_libdir}/postgresql/pgrowlocks.so
%{_libdir}/postgresql/sslinfo.so
%{_libdir}/postgresql/pageinspect.so

%{_datadir}/postgresql/contrib/
%{_bindir}/oid2name
%{_bindir}/pgbench
%{_bindir}/vacuumlo

%files server -f server.lst
%defattr(-,root,root)
%config(noreplace) %{_initrddir}/postgresql
%config(noreplace) %{_sysconfdir}/sysconfig/postgresql
%doc README.urpmi postgresql.mdv.releasenote
%{_bindir}/initdb
%{_bindir}/ipcclean
%{_bindir}/pg_controldata 
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/pg_standby
%{_mandir}/man1/initdb.1*
%{_mandir}/man1/ipcclean.1*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.1*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.1*
%{_mandir}/man1/postmaster.1*
%dir %{_libdir}/postgresql
%dir %{_datadir}/postgresql
%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bashrc
%attr(-,postgres,postgres) /var/lib/pgsql/.profile
%attr(700,postgres,postgres) %dir %{pgdata}
%attr(-,postgres,postgres) %{pgdata}/data
%attr(700,postgres,postgres) %dir %{pgdata}/backups
%{_libdir}/postgresql/*_and_*.so
%{_libdir}/postgresql/pgxml.so
%{_libdir}/postgresql/dict_int.so
%{_libdir}/postgresql/dict_xsyn.so
%{_libdir}/postgresql/test_parser.so
%{_libdir}/postgresql/tsearch2.so
%{_libdir}/postgresql/dict_snowball.so
%{_libdir}/postgresql/uuid-ossp.so
%{_datadir}/postgresql/postgres.bki
%{_datadir}/postgresql/postgres.description
%{_datadir}/postgresql/*.sample
%{_datadir}/postgresql/timezone
%{_datadir}/postgresql/system_views.sql
%{_datadir}/postgresql/conversion_create.sql
%{_datadir}/postgresql/information_schema.sql
%{_datadir}/postgresql/snowball_create.sql
%{_datadir}/postgresql/sql_features.txt

%{_datadir}/postgresql/postgres.shdescription
%dir %{_datadir}/postgresql/timezonesets
%{_datadir}/postgresql/timezonesets/Africa.txt
%{_datadir}/postgresql/timezonesets/America.txt
%{_datadir}/postgresql/timezonesets/Antarctica.txt
%{_datadir}/postgresql/timezonesets/Asia.txt
%{_datadir}/postgresql/timezonesets/Atlantic.txt
%{_datadir}/postgresql/timezonesets/Australia
%{_datadir}/postgresql/timezonesets/Australia.txt
%{_datadir}/postgresql/timezonesets/Default
%{_datadir}/postgresql/timezonesets/Etc.txt
%{_datadir}/postgresql/timezonesets/Europe.txt
%{_datadir}/postgresql/timezonesets/India
%{_datadir}/postgresql/timezonesets/Indian.txt
%{_datadir}/postgresql/timezonesets/Pacific.txt
%{_datadir}/postgresql/tsearch_data

%attr(700,postgres,postgres) %dir /var/log/postgres
%logrotatedir/%{bname}

%files devel
%defattr(-,root,root)
%doc doc/TODO doc/TODO.detail
%{_includedir}/*
%{_bindir}/ecpg
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/postgresql/pgxs/
%{_mandir}/man1/ecpg.1*
%{_bindir}/pg_config
%{_mandir}/man1/pg_config.1*
#From %files -n %{libnamedevel}
%{_libdir}/libpq.so
#From %files -n %{libecpgdevel}
%{_libdir}/libecpg.so

%files pl 
%defattr(-,root,root) 

%files plpython
%defattr(-,root,root) 
%{_libdir}/postgresql/plpython.so 

%files plperl
%defattr(-,root,root) 
%{_libdir}/postgresql/plperl.so 

%files pltcl
%defattr(-,root,root) 
%{_libdir}/postgresql/pltcl.so 
%{_bindir}/pltcl_delmod 
%{_bindir}/pltcl_listmod 
%{_bindir}/pltcl_loadmod 
%{_datadir}/postgresql/unknown.pltcl 

%files plpgsql
%defattr(-,root,root) 
%{_libdir}/postgresql/plpgsql.so

