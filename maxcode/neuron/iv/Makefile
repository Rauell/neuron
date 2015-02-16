# Makefile.in generated automatically by automake 1.4a from Makefile.am

# Copyright (C) 1994, 1995-8, 1999 Free Software Foundation, Inc.
# This Makefile.in is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, to the extent permitted by law; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.

SHELL = /bin/bash

srcdir = .
top_srcdir = .

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

top_builddir = .

AUTOCONF = autoconf



SUBDIRS = src
subdir = .

ACLOCAL_M4 = $(top_srcdir)/aclocal.m4

mkinstalldirs = $(SHELL) $(top_srcdir)/mkinstalldirs
CONFIG_CLEAN_FILES = 
DIST_SOURCES = 
DIST_COMMON =  README INSTALL Makefile.in aclocal.m4 \
config.guess config.sub configure configure.in install-sh \
ltconfig ltmain.sh mkinstalldirs


DISTFILES = $(DIST_COMMON) $(DIST_SOURCES) $(TEXINFOS) $(EXTRA_DIST)

# This directory's subdirectories are mostly independent; you can cd
# into them and run `make' without going through this Makefile.
# To change the values of `make' variables: instead of editing Makefiles,
# (1) if the variable is set in `config.status', edit `config.status'
#     (which will cause the Makefiles to be regenerated when you run `make');
# (2) otherwise, pass the desired values on the `make' command line.

all install clean mostlyclean uninstall:
	@topdir=`pwd`; \
	for dir in $(SUBDIRS); do \
	  echo "Making $@ in $$dir"; \
	  cd $$dir; \
	  $(MAKE) $@; \
	  cd $$topdir; \
	done

distclean:
	@topdir=`pwd`; \
	for dir in $(SUBDIRS); do \
	  echo "Making $@ in $$dir"; \
	  cd $$dir; \
	  $(MAKE) $@; \
	  cd $$topdir; \
	done
	$(RM) config.cache config.status config.log

Makefile: $(srcdir)/Makefile.in  $(top_builddir)/config.status
	cd $(top_builddir) \
	  && CONFIG_FILES=$@ CONFIG_HEADERS= $(SHELL) ./config.status

config.status: $(srcdir)/configure $(CONFIG_STATUS_DEPENDENCIES)
	$(SHELL) ./config.status --recheck
$(srcdir)/configure: $(srcdir)/configure.in $(ACLOCAL_M4) $(CONFIGURE_DEPENDENCIES)
	cd $(srcdir) && $(AUTOCONF)

.PHONY: all install clean mostlyclean distclean uninstall dist zip-dist

# Tell versions [3.59,3.63) of GNU make to not export all variables.
# Otherwise a system limit (for SysV at least) may be exceeded.
.NOEXPORT:
