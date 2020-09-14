#
#
#

ifeq ($(PREFIX),)
	PREFIX := $(HOME)
endif

install:
	echo $(PREFIX)
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m 644 data/investing_com.indexes $(DESTDIR)$(PREFIX)/.investing_com.indexes
	install -m 755 scripts/investing $(DESTDIR)$(PREFIX)/bin/
	install -m 644 scripts/investing-alert-view.py $(DESTDIR)$(PREFIX)/bin/
	install -m 644 scripts/investing-portfolio-view.py $(DESTDIR)$(PREFIX)/bin/
	install -m 644 scripts/investing-portfolio-panel.py $(DESTDIR)$(PREFIX)/bin/

# TODO: add spiders into pip default path installation
