%define name	roadmap
%define version	1.0.10
%define	rel	5
%define release	%mkrel %{rel}
%define	Summary	GPS Tracker

Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Sciences/Geosciences
License:	GPL
Source0:	%{name}_1_0_10_src.tar.bz2
Patch0:		roadmap-1.0.10-gcc4-fix.patch.bz2
Patch1:		roadmap-1.0.10-add-missing-files.patch.bz2
Patch2:		roadmap-1.0.10-fix-paths.patch.bz2
URL:		http://roadmap.digitalomaha.net/
Requires:	gpsd
BuildRequires:	shapelib-devel 
BuildRequires:  wget 
BuildRequires:  gtk+2-devel
BuildRequires:  popt-devel
Summary:	%{Summary}

%description 
A navigation system that displays US street maps (from the US Census Bureau)
and tracks a vehicle using GPS. Specific areas can be displayed by selecting
a street address (street number & name, city, and state).
RoadMap can run on iPAQ and Zaurus.

Be sure to consult %{_docdir}/%{name}-%{version}/README
for instructions on using this software!

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .gcc4
%patch1 -p1
%patch2 -p1 -b .paths
wget http://roadmap.digitalomaha.net/maps/usdir.rdm.tgz
tar -zxf usdir.rdm.tgz

%build
cd src
make DESKTOP=GTK2 MODECFLAGS="$RPM_OPT_FLAGS -ffast-math -W -Wall -Wno-unused-parameter -DROADMAP_USE_SHAPEFILES -I%{_includedir}/libshp"

%install
rm -rf %{buildroot}
cd src
%{makeinstall_std} DESKTOP=GTK2 INSTALLDIR=%{_prefix} desktopdir=%{_datadir}/applications
install -m755 gtk2/gtkroadgps -D %{buildroot}%{_bindir}/roadgps
install -m755 gtk2/gtkroadmap -D %{buildroot}%{_bindir}/roadmap
install -m644 ../usdir.rdm -D %{buildroot}%{_datadir}/roadmap/usdir.rdm

install -m644 roadmap-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 roadmap-32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 roadmap-48.png -D %{buildroot}%{_liconsdir}/%{name}.png

install -d %{buildroot}%{_menudir}
cat <<EOF > %{buildroot}%{_menudir}/%{name}
?package(%{name}):command="%{name}" \
                icon=%{name}.png \
                needs="x11" \
                section="More Applications/Sciences/Geosciences" \
                title="Roadmap"\
                longtitle="%{Summary}"
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/roadmap.desktop
%{_mandir}/man1/*.1*
%{_datadir}/pixmaps/*.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_menudir}/%{name}
