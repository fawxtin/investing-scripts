#
#
#

ifeq ($(PREFIX),)
	PREFIX := $(HOME)
endif

install:
	echo $(PREFIX)
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -d $(DESTDIR)$(PREFIX)/.local/share/investing.com/logs/
	install -d $(DESTDIR)$(PREFIX)/.local/share/investing.com/spiders/
	install -m 644 --compare --backup=numbered data/investing_com.indexes $(DESTDIR)$(PREFIX)/.investing_com.indexes
	install -m 755 scripts/investing $(DESTDIR)$(PREFIX)/bin/
	install -m 644 scripts/investing-alert-view.py $(DESTDIR)$(PREFIX)/bin/
	install -m 644 scripts/investing-portfolio-view.py $(DESTDIR)$(PREFIX)/bin/
	install -m 644 scripts/investing-portfolio-panel.py $(DESTDIR)$(PREFIX)/bin/
	install -m 644 spiders/investing-spider-alert-list.py $(DESTDIR)$(PREFIX)/.local/share/investing.com/spiders/
	install -m 644 spiders/investing-spider-portfolio-list.py $(DESTDIR)$(PREFIX)/.local/share/investing.com/spiders/

