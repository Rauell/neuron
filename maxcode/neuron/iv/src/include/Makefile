SHELL = /bin/bash

srcdir = .
top_srcdir = ../..

prefix = /home/hendemd/neuron/iv
exec_prefix = /home/hendemd/neuron/iv/i686

bindir = ${exec_prefix}/bin
sbindir = ${exec_prefix}/sbin
libexecdir = ${exec_prefix}/libexec
datadir = ${prefix}/share
sysconfdir = ${prefix}/etc
sharedstatedir = ${prefix}/com
localstatedir = ${prefix}/var
libdir = ${exec_prefix}/lib
infodir = ${prefix}/info
mandir = ${prefix}/man
includedir = ${prefix}/include
oldincludedir = /usr/include

DESTDIR =

pkgdatadir = $(datadir)/iv
pkglibdir = $(libdir)/iv
pkgincludedir = $(includedir)/iv

top_builddir = ../..

INSTALL = /usr/bin/install -c
INSTALL_PROGRAM = ${INSTALL}
INSTALL_DATA = ${INSTALL} -m 644
INSTALL_SCRIPT = ${INSTALL}

DIRS = Dispatch IV-2_6 IV-2_6/InterViews IV-X11 IV-look InterViews OS TIFF

#DIRS = Dispatch IV-Win IV-look InterViews OS TIFF

#DIRS = Dispatch IV-Mac IV-look InterViews OS TIFF



subdir = src/include

ACLOCAL_M4 = $(top_srcdir)/aclocal.m4

mkinstalldirs = $(SHELL) $(top_srcdir)/mkinstalldirs

all:

clean:

mostlyclean:

Makefile: $(srcdir)/Makefile.in  $(top_builddir)/config.status
	cd $(top_builddir) \
	  && CONFIG_FILES=$@ CONFIG_HEADERS= $(SHELL) ./config.status

install:
	for dir in $(DIRS); do \
	  $(mkinstalldirs) $(DESTDIR)$(includedir)/$$dir; \
	  for file in $$dir/*.h; do \
	    $(INSTALL_DATA) $$file $(DESTDIR)$(includedir)/$$file; \
	  done; \
	done
	$(mkinstalldirs) $(DESTDIR)$(includedir)/InterViews/Bitmaps
	for file in InterViews/Bitmaps/*.bm; do \
	  $(INSTALL_DATA) $$file $(DESTDIR)$(includedir)/$$file; \
	done
	$(INSTALL_DATA) ivstream.h $(DESTDIR)$(includedir)/ivstream.h
	$(INSTALL_DATA) ivstrm.h $(DESTDIR)$(includedir)/ivstrm.h
	$(INSTALL_DATA) ivversion.h $(DESTDIR)$(includedir)/ivversion.h

uninstall:
	for dir in $(DIRS); do \
	  cd $$dir; \
	  for file in *.h; do \
	    rm -f $(DESTDIR)$(includedir)/$$dir/$$file; \
	  done; \
	  cd ..; \
	done
	for file in ivstream.h ivstrm.h ivversion.h do \
	  rm -f $(DESTDIR}$(includedir)/$$file; \
	done
.PHONY: all install clean mostlyclean distclean uninstall

# Tell versions [3.59,3.63) of GNU make to not export all variables.
# Otherwise a system limit (for SysV at least) may be exceeded.
.NOEXPORT:
