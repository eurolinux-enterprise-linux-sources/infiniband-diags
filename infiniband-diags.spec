Summary: OpenFabrics Alliance InfiniBand Diagnostic Tools
Name: infiniband-diags 
Version: 2.0.0
Release: 1%{?dist}
# Upstream allows either license to be used
License: GPLv2 or BSD
Url:     https://github.com/linux-rdma/infiniband-diags
Source0: https://github.com/linux-rdma/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
# RHEL-specific patches:
Patch6: 0006-Fix-hostname-usage-in-set_nodedesc.sh.patch
Patch7: 0007-Fix-ibnodes-h-output.patch

BuildRequires: opensm-devel > 3.3.8, libibumad-devel, perl
BuildRequires: glib2-devel
Provides: perl(IBswcountlimits)
Provides: libibmad = %{version}-%{release}
Obsoletes: libibmad < %{version}-%{release}
Obsoletes: openib-diags < 1.3

%description
This package provides IB diagnostic programs and scripts needed to diagnose an
IB subnet.  infiniband-diags now also provides libibmad.  libibmad provides low
layer IB functions for use by the IB diagnostic and management programs. These
include MAD, SA, SMP, and other basic IB functions.

%package devel
Summary: Development files for the infiniband-diags library
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: libibmad-devel = %{version}-%{release}
Obsoletes: libibmad-devel < %{version}-%{release}

%description devel
Headers and shared devel libraries for the infiniband-diags package.

%package devel-static
Summary: Static development files for the infiniband-diags library
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Provides: libibmad-static = %{version}-%{release}
Obsoletes: libibmad-static < %{version}-%{release}

%description devel-static
Static libraries for the infiniband-diags library.

%prep
%setup -q
%patch6 -p1 -b .hostname
%patch7 -p1 -b .help

%build
%configure
make V=1

%install
make DESTDIR=$RPM_BUILD_ROOT install
# remove unpackaged files from the buildroot
find ${RPM_BUILD_ROOT} -type f -name '*.la' -print -delete

%files
# C programs here
%{_sbindir}/ibaddr
%{_mandir}/man8/ibaddr.8.gz
%{_sbindir}/ibnetdiscover
%{_mandir}/man8/ibnetdiscover.8.gz
%{_sbindir}/ibping
%{_mandir}/man8/ibping.8.gz
%{_sbindir}/ibportstate
%{_mandir}/man8/ibportstate.8.gz
%{_sbindir}/ibroute
%{_mandir}/man8/ibroute.8.gz
%{_sbindir}/ibstat
%{_mandir}/man8/ibstat.8.gz
%{_sbindir}/ibsysstat
%{_mandir}/man8/ibsysstat.8.gz
%{_sbindir}/ibtracert
%{_mandir}/man8/ibtracert.8.gz
%{_sbindir}/perfquery
%{_mandir}/man8/perfquery.8.gz
%{_sbindir}/sminfo
%{_mandir}/man8/sminfo.8.gz
%{_sbindir}/smpdump
%{_mandir}/man8/smpdump.8.gz
%{_sbindir}/smpquery
%{_mandir}/man8/smpquery.8.gz
%{_sbindir}/saquery
%{_mandir}/man8/saquery.8.gz
%{_sbindir}/vendstat
%{_mandir}/man8/vendstat.8.gz
%{_sbindir}/iblinkinfo
%{_mandir}/man8/iblinkinfo.8.gz
%{_sbindir}/ibqueryerrors
%{_mandir}/man8/ibqueryerrors.8.gz
%{_sbindir}/ibcacheedit
%{_mandir}/man8/ibcacheedit.8.gz
%{_sbindir}/ibccquery
%{_mandir}/man8/ibccquery.8.gz
%{_sbindir}/ibccconfig
%{_mandir}/man8/ibccconfig.8.gz
%{_sbindir}/dump_fts
%{_mandir}/man8/dump_fts.8.gz

# scripts here
%{_sbindir}/ibhosts
%{_mandir}/man8/ibhosts.8.gz
%{_sbindir}/ibswitches
%{_mandir}/man8/ibswitches.8.gz
%{_sbindir}/ibnodes
%{_mandir}/man8/ibnodes.8.gz
%{_sbindir}/ibrouters
%{_mandir}/man8/ibrouters.8.gz
%{_sbindir}/ibfindnodesusing.pl
%{_mandir}/man8/ibfindnodesusing.8.gz
%{_sbindir}/ibidsverify.pl
%{_mandir}/man8/ibidsverify.8.gz
%{_sbindir}/check_lft_balance.pl
%{_mandir}/man8/check_lft_balance.8.gz
%{_sbindir}/dump_lfts.sh
%{_mandir}/man8/dump_lfts.8.gz
%{_sbindir}/dump_mfts.sh
%{_mandir}/man8/dump_mfts.8.gz
%{_sbindir}/ibstatus
%{_mandir}/man8/ibstatus.8.gz

# and the rest
%{_mandir}/man8/infiniband-diags.8.gz
%{_libdir}/*.so.*
%global _perldir %(perl -e 'use Config; $T=$Config{installvendorlib}; print $T;')
%{_perldir}/IBswcountlimits.pm
%dir %{_sysconfdir}/infiniband-diags
%config(noreplace) %{_sysconfdir}/infiniband-diags/error_thresholds
%config(noreplace) %{_sysconfdir}/infiniband-diags/ibdiag.conf
%doc README COPYING ChangeLog
%license COPYING

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*

%files devel-static
%{_libdir}/*.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Mon Oct 16 2017 Honggang Li <honli@redhat.com> 2.0.0-1
- Rebase to latest upstream release v2.0.0
- Resolves: bz1456944

* Mon Mar  6 2017 Honggang Li <honli@redhat.com> - 1.6.7-1
- Rebase to latest upstream release 1.6.7.
- Remove patches merged into upstream release.
- Remove sub-package rdma-ndd as it merged into rdma-core.
- Resolves: bz1382809

* Mon Jun 22 2015 Michal Schmidt <mschmidt@redhat.com> - 1.6.5-3
- systemd Requires for scriptlets belong to rdma-ndd too.
- Related: bz1169968

* Mon Jun 22 2015 Michal Schmidt <mschmidt@redhat.com> - 1.6.5-2
- Move the Conflicts to the rdma-ndd subpackage.
- Related: bz1169968

* Mon Jun 22 2015 Michal Schmidt <mschmidt@redhat.com> - 1.6.5-1
- Update to latest upstream release. Adds rdma-ndd daemon.
- Rebase patches, cherry-pick fixes from upstream git.
- Enable build on s390(x).
- Fixed bogus changelog dates.
- Add Conflicts with old rdma. It needs to be aware of rdma-ndd.
- Resolves: bz1169968

* Fri Oct 31 2014 Doug Ledford <dledford@redhat.com> - 1.6.4-1
- Update to latest upstream release
- Resolves: bz1061586

* Thu Jan 23 2014 Doug Ledford <dledford@redhat.com> - 1.6.2-1
- Update to latest upstream release (resolves bz998816)
- Revive all_hcas patch (otherwise would be a regression)
- Fix ibnodes -h output (another regression, bz1054545)
- Resolves: bz998816, bz1054545

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.6.1-5
- Mass rebuild 2013-12-27

* Sun Mar 10 2013 Doug Ledford <dledford@redhat.com> - 1.6.1-4
- Fix hostname usage in set_nodedesc.sh

* Sat Mar  2 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.6.1-3
- Build on ARM
- Cleanup and modernise spec

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Jon Stanley <jonstanley@gmail.com>
- Update to 1.6.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 06 2012 Doug Ledford <dledford@redhat.com> - 1.5.12-1
- Update to latest upstream release
- Initial Fedora import
- Add devel and devel static packages (review item)
- Make etc file config(noreplace) (review item)
- Remove no longer support scripts (review item)

* Wed Jul 27 2011 Doug Ledford <dledford@redhat.com> - 1.5.8-1.el6
- Update to latest upstream version
- Make build work on i686 arch
- Modify perfquery to be able to loop through all HCAs in a single host
- Resolves: bz593767
- Related: bz725016

* Fri Mar 12 2010 Doug Ledford <dledford@redhat.com> - 1.5.5-1.el6
- Update and rebuild against latest opensm (which was needed for latest
  ibutils, which was needed for licensing issues resolved in new upstream
  tarball, which was needed for pkgwrangler review)
- Related: bz555835

* Fri Feb 26 2010 Doug Ledford <dledford@redhat.com> - 1.5.3-4.el6
- Tidy ups for pkgwrangler review
- Related: bz555835

* Tue Feb 9 2010 Jay Fenlason <fenlason@redhat.com> 1.5.3-3.el6
- Correct the perldir macro for rhel-6's perl.
- Remove the unrecognized --with-node-name-map configure option.
- reorganize the files section to use fewer globs, so that it's less likely
  to pick up files inappropriately.

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.5.3-2.el6
- Update license tag for pkgwrangler import
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 1.5.3-1.el5
- Update to latest upstream version
- Don't include the newly added devel stuff as it's likely only needed
  internally (and certainly not needed by anything we've supported before
  since we've never shipped it)
- Related: bz518218

* Fri Apr 17 2009 Doug Ledford <dledford@redhat.com> - 1.4.4-1.el5
- Update to ofed 1.4.1-rc3 version
- Remove dead patch
- Related: bz459652

* Fri Oct 17 2008 Doug Ledford <dledford@redhat.com> - 1.4.1-2
- Fix up a few trivial issues
- Resolves: bz216014

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 1.4.1-1
- Update to latest upstream version (required to work with latest opensm libs)
- Resolves: bz451465

* Tue Apr 01 2008 Doug Ledford <dledford@redhat.com> - 1.3.6-1
- Update to latest upstream version to match OFED 1.3
- Related: bz428197

* Sun Jan 27 2008 Doug Ledford <dledford@redhat.com> - 1.3.5-2
- Obsolete the openib-diags that this package replaces

* Fri Jan 25 2008 Doug Ledford <dledford@redhat.com> - 1.3.5-1
- Import into Red Hat CVS
- Related: bz428197

* Wed Oct 31 2007 Ira Weiny <weiny2@llnl.gov> - 1.3.2
- Change switch-map option to node-name-map

* Thu Aug 9 2007 Ira Weiny <weiny2@llnl.gov> - 1.3.1
- Change set_mthca_nodedesc.sh to set_nodedesc.sh

* Tue Jul 10 2007 Hal Rosenstock <halr@voltaire.com> - 1.3.1
- Add link width and speed to topology file output in ibnetdiscover
- Add support for -R(outer_list) in ibnetdiscover
- Add script and man page for ibidsverify
- Moved diags from bin to sbin
- Add scripts and man pages for display on IB routers
- Add GUID to output line for ports in ibqueryerrors.pl
- Add ibdatacounts and ibdatacounters scripts and man pages
- Add peer port link width and speed validation in iblinkinfo.pl
- Display remote LID with peer port info in IBswcountlimits.pm
- Handle peer ports at 1x that should be wider and 2.5 Gbps
  links that should be faster in ibportstate
- Add LinkSpeed/Width components to output of ibportstate
- Add support for IB routers 
- Add grouping support for ISR2012 and ISR2004 in ibnetdiscover
- Remove all uses of "/tmp" from perl scripts
- Add switch map support for saquery -O and -U options
- Add support for saquery -s (isSMdisabled)
- Add name input checks to saquery (-O and -U) 

* Thu Mar 29 2007 Hal Rosenstock <halr@voltaire.com> - 1.3.0
- Add some extra debug information to IBswcountlimits.pm
- Send normal output to stdout in ibtracert
- Don't truncate NodeDescriptions containing ctl characters in ibdiag_common
- Fix ibnetdiscover grouping for Cisco SFS7000
- Add support to query the GUIDInfo table in smpquery
- Allow user to specify a default switch map file

* Fri Mar 9 2007 Hal Rosenstock <halr@voltaire.com> - 1.2.5 
- Find perl modules in perl sitearch directory
- Fix non standard prefix install for diag scripts
- Clean gcc-4.1 warnings in saquery and ibdiag_common

* Fri Mar 2 2007 Hal Rosenstock <halr@voltaire.com> - 1.2.4
- OpenFabrics 1.2.4 release
- Fix diag rpmbuild from make dist
- Include set_mthca_nodedesc.sh and dump_lfts.sh in the rpm

* Thu Mar 1 2007 Hal Rosenstock <halr@voltaire.com> - 1.2.3
- OpenFabrics 1.2.3 release
- Fixed saquery timeout handling

* Tue Feb 27 2007 Hal Rosenstock <halr@voltaire.com> - 1.2.2
- OpenFabrics 1.2.2 release
- Minor changes to ibswitches and ibhosts output

* Wed Feb 14 2007 Hal Rosenstock <halr@voltaire.com> - 1.2.1
- OpenFabrics 1.2.1 release
- Initial release of vendstat tool

* Fri Feb 2 2007 Hal Rosenstock <halr@voltaire.com> - 1.2.0
- OpenFabrics 1.2.0 release
- Added brief option to ibcheckerrors and ibcheckerrs
- Updated man pages
- Added build version to saquery and updated build version tags of other tools
- Added -N | nocolor to usage display of scripts
- Fixed -nocolor and -G options on scripts 
- Fixed error return status in ibchecknet
- Added exit code to ibcheckerrors
- Added nodename to output of ibcheckerrs
- ibqueryerrors.pl fixes and improvements
- Removed use of tmpfile for ibroute data in ibfindnodeusing.pl
- Fixed undefined subroutine error in iblinkinfo.pl
- Added switch-map option to ibtracert and ibnetdiscover
- Cleaned up node descriptions before printing in saquery
- Clarified --src-to-dst option in saquery
- Added peer NodeDescription and LID to output of inbetdiscover
- For grouping, ordered Spine and Line Nodes (for Voltaire chassis) in ibnetdiscover
- Cleaned up node descriptions before printing in ibtracert and ibroute
- Added additional sematics to -m option of saquery
- Added dump_mfts.sh similar to dump_lfts.sh
- ibnetdiscover improvements (memory leaks, ports moving, etc.)
- Converted iblinkspeed.pl into iblinkinfo.pl and added additional capabilities
- Added 0x in front of GUID printing of ibtracert
- Fixed loopback handling in ibnetdiscover
- Added support for querying Service Records to saquery
- Added support for PerfMgt IsExtendedWidthSupported IBA 1.2 erratum in perfquery
- For query operations, added peer port checking of linkwidth and speed
  active in ibportstate
- Added support for DrSLID in smpquery
- Added IB router support to ibnetdiscover and ibtracert
- Added additional options to saquery
- Added support to change LinkSpeedEnabled in ibportstate

* Fri Sep 22 2006 Hal Rosenstock <halr@voltaire.com> - 1.1.0
- OpenFabrics 1.1 release
 
* Wed Sep 13 2006 Hal Rosenstock <halr@voltaire.com> - 1.1.0-rc5
- OpenFabrics 1.1-rc5 release

* Wed Sep 6 2006 Hal Rosenstock <halr@voltaire.com> - 1.1.0-rc4
- OpenFabrics 1.1-rc4 release

* Wed Aug 23 2006 Hal Rosenstock <halr@voltaire.com> - 1.1.0-rc3
- OpenFabrics 1.1-rc3 release

* Mon Aug 14 2006 Hal Rosenstock <halr@voltaire.com> - 1.1.0-rc2
- OpenFabrics 1.1-rc2 release
- Added ibsysstat man page

* Wed Jul 26 2006 Hal Rosenstock <halr@voltaire.com> - 1.1.0-rc1
- OpenFabrics 1.1-rc1 release
- Added man pages
- Made diag command/script options more consistent
- saquery tool added
- dump_lft.sh script added
- Renamed discover.pl to ibdiscover.pl

* Sat Jun 10 2006 Hal Rosenstock <halr@voltaire.com> - 1.0-1
- OpenFabrics 1.0 release

* Tue May 30 2006 Hal Rosenstock <halr@voltaire.com> - 1.0.0-rc6
- Maintenance release

* Fri May 12 2006 Hal Rosenstock <halr@voltaire.com> - 1.0.0-rc5
- Maintenance release

* Thu Apr 27 2006 Hal Rosenstock <halr@voltaire.com> - 1.0.0-rc4
- Maintenance release
- Note rc3 skipped to sync with OFED

* Mon Apr 10 2006 Hal Rosenstock <halr@voltaire.com> - 1.0.0-rc2
- Maintenance release

* Mon Feb 27 2006 Hal Rosenstock <halr@voltaire.com> - 1.0.0-rc1
- Initial spec file and release
