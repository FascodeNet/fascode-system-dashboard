APPNAME=fascode-system-dashboard
PREFIX=usr
LANGUAGE_FILES=$(patsubst po/%.po, locale/%/LC_MESSAGES/$(APPNAME).mo, $(wildcard po/*.po))
DESTDIR=

locale/%/LC_MESSAGES/$(APPNAME).mo: po/%.po
	mkdir -p $(dir $@)
	msgfmt $< -o $@

install: $(LANGUAGE_FILES)
	install -d $(DESTDIR)/$(PREFIX)/bin
	install -m 755 bin/$(APPNAME) $(DESTDIR)/$(PREFIX)/bin

	install -d $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	install -m 644 $(APPNAME)/application.py $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	install -m 644 $(APPNAME)/cairo_util.py $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	install -m 644 $(APPNAME)/circle.py $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	install -m 644 $(APPNAME)/fascode-system-dashboard.py  $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	install -m 644 $(APPNAME)/graph.py $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	install -m 644 $(APPNAME)/label.py $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	install -m 644 $(APPNAME)/process.py $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	install -m 644 $(APPNAME)/speed.py $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	install -m 644 $(APPNAME)/util.py $(DESTDIR)/$(PREFIX)/share/$(APPNAME)

	install -d $(DESTDIR)/$(PREFIX)/share/applications
	install -m 644 fascode-system-dashboard.desktop $(DESTDIR)/$(PREFIX)/share/applications

	cp -rf locale $(DESTDIR)/$(PREFIX)/share

uninstall:
	rm -rf $(DESTDIR)/$(PREFIX)/share/$(APPNAME)
	rm -f $(DESTDIR)/$(PREFIX)/bin/$(APPNAME)
	rm -f $(DESTDIR)/$(PREFIX)/share/locale/*/LC_MESSAGES/$(APPNAME).mo

clean:
	rm -rf locale