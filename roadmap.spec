%define name	roadmap
%define version	1.2.1
%define release	%mkrel 3
%define	Summary	GPS Tracker

Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Sciences/Geosciences
License:	GPL
Summary:	%{Summary}
URL:		http://roadmap.sourceforge.net/download.html
Source0:	http://downloads.sourceforge.net/roadmap/%{name}-%{version}-src.tar.gz
Source1:	http://downloads.sourceforge.net/roadmap/roadmap-1.2.0-wince-arm.cab
Patch2:		roadmap-1.2.1-fix-paths.patch
Requires:	gpsd
BuildRequires:	shapelib-devel 
BuildRequires:	expat-devel
BuildRequires:  gtk+2-devel
BuildRequires:  popt-devel
Buildroot:	%{_tmppath}/%{name}-%{version}

%description 
A navigation system that displays US street maps (from the US Census Bureau)
and tracks a vehicle using GPS. Specific areas can be displayed by selecting
a street address (street number & name, city, and state).
RoadMap can run on iPAQ and Zaurus.

%prep
%setup -q -n %{name}-%{version}
%patch2 -p1 -b .paths

%build
cd src
make DESKTOP=GTK2 MODECFLAGS="$RPM_OPT_FLAGS -ffast-math -W -Wall -Wno-unused-parameter -DROADMAP_USE_SHAPEFILES -I%{_includedir}/libshp"

%install
rm -rf %{buildroot}
cd src
%{makeinstall_std} \
    DESKTOP=GTK2 \
    INSTALLDIR=%{_prefix} \
    desktopdir=%{buildroot}%{_datadir}/applications

install -m755 gtk2/gtkroadgps -D %{buildroot}%{_bindir}/roadgps
install -m755 gtk2/gtkroadmap -D %{buildroot}%{_bindir}/roadmap
#install -m644 ../usdir.rdm -D %{buildroot}%{_datadir}/roadmap/usdir.rdm

install -m644 icons/roadmap-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 icons/roadmap-32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 icons/roadmap-48.png -D %{buildroot}%{_liconsdir}/%{name}.png

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/roadmap.desktop
%{_mandir}/man1/*.1*
%{_datadir}/pixmaps/*.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop
