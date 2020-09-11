#
#
#

ifeq ($(PREFIX),)
	PREFIX := $(HOME)
endif

install:
	echo $(PREFIX)
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m 755 scripts/investing-alert $(DESTDIR)$(PREFIX)/bin/
	install -m 755 scripts/investing-portfolio $(DESTDIR)$(PREFIX)/bin/
	install -m 755 scripts/investing-alert-view $(DESTDIR)$(PREFIX)/bin/
	install -m 755 scripts/investing-portfolio-view $(DESTDIR)$(PREFIX)/bin/
	install -m 755 scripts/investing-portfolio-panel $(DESTDIR)$(PREFIX)/bin/

# TODO: add spiders into pip default path installation
