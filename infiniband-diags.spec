Summary: OpenFabrics Alliance InfiniBand Diagnostic Tools
Name: infiniband-diags 
Version: 1.5.12
Release: 5%{?dist}
License: GPLv2 or BSD
Group: System Environment/Libraries
Url: http://openfabrics.org/
Source0: http://www.openfabrics.org/downloads/management/%{name}-%{version}.tar.gz
Patch0: infiniband-diags-1.5.8-all_hcas.patch
Patch1: infiniband-diags-1.5.12-help.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: opensm-devel >= 3.3.13, libibumad-devel, libibmad-devel, perl
Provides: perl(IBswcountlimits)
Obsoletes: openib-diags < 1.3
ExclusiveArch: %{ix86} x86_64 ia64 ppc ppc64

# Find the correct directory to install the perl module into.
%global _perldir %(perl -e 'use Config; print $Config{installvendorarch};')

%description
This package provides IB diagnostic programs and scripts needed to
diagnose an IB subnet.

%package devel
Summary: Development files for the infiniband-diags library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Headers and shared devel libraries for the infiniband-diags package.

%package devel-static
Summary: Static development files for the infiniband-diags library
Group: System Environment/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description devel-static
Static libraries for the infiniband-diags library.

%prep
%setup -q
%patch0 -p1 -b .hcas
%patch1 -p1 -b .help

%build
%configure --with-perl-installdir=%{_perldir}
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# rm -f $RPM_BUILD_ROOT%{_sbindir}/*.{pl,sh}
# Do not ship man pages for scripts we don't ship.
rm -f $RPM_BUILD_ROOT%{_sbindir}/check_lft_balance.pl
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/check_lft_balance.8*
rm -f $RPM_BUILD_ROOT%{_sbindir}/dump_lfts.sh
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/dump_lfts.8*
rm -f $RPM_BUILD_ROOT%{_sbindir}/dump_mfts.sh
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/dump_mfts.8*
rm -f $RPM_BUILD_ROOT%{_sbindir}/ibdiscover.pl
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/ibdiscover.8*
rm -f $RPM_BUILD_ROOT%{_sbindir}/ibfindnodesusing.pl
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/ibfindnodesusing.8*
rm -f $RPM_BUILD_ROOT%{_sbindir}/ibidsverify.pl
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/ibidsverify.8*
rm -f $RPM_BUILD_ROOT%{_sbindir}/iblinkinfo.pl
rm -f $RPM_BUILD_ROOT%{_sbindir}/ibprintca.pl
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/ibprintca.8*
rm -f $RPM_BUILD_ROOT%{_sbindir}/ibprintrt.pl
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/ibprintrt.8*
rm -f $RPM_BUILD_ROOT%{_sbindir}/ibprintswitch.pl
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/ibprintswitch.8*
rm -f $RPM_BUILD_ROOT%{_sbindir}/ibqueryerrors.pl
rm -f $RPM_BUILD_ROOT%{_sbindir}/set_nodedesc.sh


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_mandir}/man8/infiniband-diags.8*

%{_sbindir}/ibaddr
%{_mandir}/man8/ibaddr.8*
%{_sbindir}/ibcacheedit
%{_mandir}/man8/ibcacheedit.8*
%{_sbindir}/ibcheckerrors
%{_mandir}/man8/ibcheckerrors.8*
%{_sbindir}/ibcheckerrs
%{_mandir}/man8/ibcheckerrs.8*
%{_sbindir}/ibchecknet
%{_mandir}/man8/ibchecknet.8*
%{_sbindir}/ibchecknode
%{_mandir}/man8/ibchecknode.8*
%{_sbindir}/ibcheckport
%{_mandir}/man8/ibcheckport.8*
%{_sbindir}/ibcheckportstate
%{_mandir}/man8/ibcheckportstate.8*
%{_sbindir}/ibcheckportwidth
%{_mandir}/man8/ibcheckportwidth.8*
%{_sbindir}/ibcheckstate
%{_mandir}/man8/ibcheckstate.8*
%{_sbindir}/ibcheckwidth
%{_mandir}/man8/ibcheckwidth.8*
%{_sbindir}/ibclearcounters
%{_mandir}/man8/ibclearcounters.8*
%{_sbindir}/ibclearerrors
%{_mandir}/man8/ibclearerrors.8*
%{_sbindir}/ibdatacounters
%{_mandir}/man8/ibdatacounters.8*
%{_sbindir}/ibdatacounts
%{_mandir}/man8/ibdatacounts.8*
%{_sbindir}/ibhosts
%{_mandir}/man8/ibhosts.8*
%{_sbindir}/iblinkinfo
%{_mandir}/man8/iblinkinfo.8*
%{_sbindir}/ibnetdiscover
%{_mandir}/man8/ibnetdiscover.8*
%{_sbindir}/ibnodes
%{_mandir}/man8/ibnodes.8*
%{_sbindir}/ibping
%{_mandir}/man8/ibping.8*
%{_sbindir}/ibportstate
%{_mandir}/man8/ibportstate.8*
%{_sbindir}/ibqueryerrors
%{_mandir}/man8/ibqueryerrors.8*
%{_sbindir}/ibroute
%{_mandir}/man8/ibroute.8*
%{_sbindir}/ibrouters
%{_mandir}/man8/ibrouters.8*
%{_sbindir}/ibstat
%{_mandir}/man8/ibstat.8*
%{_sbindir}/ibstatus
%{_mandir}/man8/ibstatus.8*
%{_sbindir}/ibswitches
%{_mandir}/man8/ibswitches.8*
%{_sbindir}/ibswportwatch.pl
%{_mandir}/man8/ibswportwatch.8*
%{_sbindir}/ibsysstat
%{_mandir}/man8/ibsysstat.8*
%{_sbindir}/ibtracert
%{_mandir}/man8/ibtracert.8*
%{_sbindir}/perfquery
%{_mandir}/man8/perfquery.8*
%{_sbindir}/saquery
%{_mandir}/man8/saquery.8*
%{_sbindir}/sminfo
%{_mandir}/man8/sminfo.8*
%{_sbindir}/smpdump
%{_mandir}/man8/smpdump.8*
%{_sbindir}/smpquery
%{_mandir}/man8/smpquery.8*
%{_sbindir}/vendstat
%{_mandir}/man8/vendstat.8*

%{_libdir}/libibnetdisc.so.5
%{_libdir}/libibnetdisc.so.5.2.0
%dir %{_sysconfdir}/infiniband-diags
%config(noreplace) %{_sysconfdir}/infiniband-diags/error_thresholds
%doc COPYING README ChangeLog
%{_perldir}/IBswcountlimits.pm

%files devel
%defattr(-,root,root)
%dir %{_includedir}/infiniband
%{_includedir}/infiniband/ibnetdisc.h
%{_includedir}/infiniband/ibnetdisc_osd.h
%{_libdir}/libibnetdisc.so
%{_mandir}/man3/ibnd_debug.*
%{_mandir}/man3/ibnd_destroy_fabric.*
%{_mandir}/man3/ibnd_discover_fabric.*
%{_mandir}/man3/ibnd_find_node_dr.*
%{_mandir}/man3/ibnd_find_node_guid.*
%{_mandir}/man3/ibnd_iter_nodes.*
%{_mandir}/man3/ibnd_iter_nodes_type.*
%{_mandir}/man3/ibnd_show_progress.*

%files devel-static
%defattr(-,root,root)
%{_libdir}/*.a

%changelog
* Mon Oct 15 2012 Doug Ledford <dledford@redhat.com> - 1.5.12-5
- Bump and rebuild against latest opensm
- Pick up fixes done for rhel5.9
- Related: bz756396

* Thu Aug 23 2012 Doug Ledford <dledford@redhat.com> - 1.5.12-4
- Update the all_hcas patch to resolve several problems
- Give a simple help message to the ibnodes script
- Resolves: bz818606, bz847129

* Thu Apr 26 2012 Jay Fenlason <fenlason@redhat.com> - 1.5.12-3
- Reorganize this spec file to include /usr/sbin/ibswportwatch.pl
  and remove man pages for programs that aren't included.
  Resolves: bz814518

* Wed Feb 29 2012 Doug Ledford <dledford@redhat.com> - 1.5.12-2
- Bump and rebuild against new opensm
- Related: bz754196

* Fri Jan 06 2012 Doug Ledford <dledford@redhat.com> - 1.5.12-1
- Update to latest upstream release
- Initial Fedora import
- Add devel and devel static packages (review item)
- Make etc file config(noreplace) (review item)
- Remove no longer support scripts (review item)
- Related: bz750609

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

* Thu Feb 14 2007 Hal Rosenstock <halr@voltaire.com> - 1.2.1
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

* Sun Jun 10 2006 Hal Rosenstock <halr@voltaire.com> - 1.0-1
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
