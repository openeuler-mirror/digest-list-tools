name:           digest-list-tools
Version:        0.3.90
Release:        1%{?dist}
Summary:        Digest list tools

Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:        GPL-2.0
Url:            https://github.com/euleros/digest-list-tools
BuildRequires:  autoconf automake libcurl-devel libtool rpm-devel dracut gzip
BuildRequires:  libcap-devel
BuildRequires:  txt2man

%if 0%{?suse_version}
BuildRequires:  libopenssl-devel
BuildRequires:  linux-glibc-devel keyutils-devel
%endif

%if 0%{?fedora}
BuildRequires:  openssl-devel kernel-headers
BuildRequires:  keyutils-libs-devel
%endif

%description
This package includes the tools for configure the IMA Digest Lists extension.

%prep
%setup -q

%build
autoreconf -iv
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/ima/digest_lists
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
cd %_builddir/%{name}-%{version}
txt2man -t %{name} README | gzip > ${RPM_BUILD_ROOT}%{_mandir}/man1/%{name}.1.gz
cd docs
for doc in $(ls *.txt); do txt2man -t ${doc%.txt} $doc |
    gzip > ${RPM_BUILD_ROOT}%{_mandir}/man1/${doc%.txt}.1.gz; done

%post
ldconfig

%postun
ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/dracut.conf.d
%{_sysconfdir}/dracut.conf.d/digestlist.conf
%dir %{_sysconfdir}/ima
%dir %{_sysconfdir}/ima/digest_lists
%{_bindir}/gen_digest_lists
%{_bindir}/setup_ima_digest_lists
%{_bindir}/setup_ima_digest_lists_demo
%{_bindir}/upload_digest_lists
%{_bindir}/verify_digest_lists
%{_libdir}/libdigestlist-base.so
%dir %{_libdir}/digestlist
%{_libdir}/digestlist/libgenerator-compact.so
%{_libdir}/digestlist/libgenerator-copy.so
%{_libdir}/digestlist/libgenerator-rpm.so
%{_libdir}/digestlist/libgenerator-unknown.so
%{_libdir}/digestlist/libparser-compact_tlv.so
%{_libdir}/digestlist/libparser-rpm.so
%{_unitdir}/setup-ima-digest-lists.service
%dir /usr/lib/dracut/modules.d/98digestlist
%{_prefix}/lib/dracut/modules.d/98digestlist/module-setup.sh
%{_prefix}/lib/dracut/modules.d/98digestlist/upload_meta_digest_lists.sh
%exclude /usr/lib64/digestlist/*.a
%exclude /usr/lib64/digestlist/*.la
%exclude /usr/lib64/libdigestlist-base.a
%exclude /usr/lib64/libdigestlist-base.la

%doc
%dir /usr/share/digest-list-tools
%{_datarootdir}/digest-list-tools/README
%{_datarootdir}/digest-list-tools/gen_digest_lists.txt
%{_datarootdir}/digest-list-tools/setup_ima_digest_lists.txt
%{_datarootdir}/digest-list-tools/setup_ima_digest_lists_demo.txt
%{_datarootdir}/digest-list-tools/upload_digest_lists.txt
%{_datarootdir}/digest-list-tools/verify_digest_lists.txt
%{_mandir}/man1/gen_digest_lists.1.gz
%{_mandir}/man1/setup_ima_digest_lists.1.gz
%{_mandir}/man1/setup_ima_digest_lists_demo.1.gz
%{_mandir}/man1/verify_digest_lists.1.gz
%{_mandir}/man1/upload_digest_lists.1.gz
%{_mandir}/man1/%{name}.1.gz

%changelog
* Fri Apr 17 2020 Roberto Sassu <roberto.sassu@huawei.com> - 0.3.90
- TLV compact list
- unknown generator
- digest list of metadata

* Tue Mar 19 2019 Roberto Sassu <roberto.sassu@huawei.com> - 0.3
- refactored code
- tests

* Thu Apr 05 2018 Roberto Sassu <roberto.sassu@huawei.com> - 0.2
- PGP signatures
- Multiple digest algorithms
- User space digest list parser
- DEB package format

* Wed Nov 15 2017 Roberto Sassu <roberto.sassu@huawei.com> - 0.1
- Initial version
