#! /usr/bin/python2
# -*- coding: utf-8 -*-

import os
import gettext
import dbus

from gi.repository import Gtk
from gi.repository import Gio

gettext.install("gnome-shell-theme-selector")

SHELL_THEME = u"Adwaita"
THEME_SETTINGS_SCHEMA = 'org.gnome.shell'
THEME_SETTINGS_KEY = 'theme-name'
Settings =  Gio.Settings.new(THEME_SETTINGS_SCHEMA)

#-----------------------------------------------
def mainwin_close(event):
	Gtk.main_quit()
	if SETUP :
		try :
			StopDaemon()
		except dbus.exceptions.DBusException :
			print ""


def load_theme_list():

	lst_shell_themes = os.listdir('/usr/share/themes')
	ComboBox_shell.append_text("Adwaita")

	for i in range(len(lst_shell_themes)):
		if os.path.isdir('/usr/share/themes/'+lst_shell_themes[i]+'/gnome-shell') :
			ComboBox_shell.append_text(lst_shell_themes[i])

def unquote(value):
	if value[0:1] == "'"  and value[len(value)-1:len(value)] == "'" :
		value = value[1:len(value)-1]
	return value

def get_iter(model,target):
	target_iter = None
	iter_test = model.get_iter_first()
	while iter_test!=None:
		name = model.get_value(iter_test,0)
		if name == target:
			target_iter = iter_test
			break 
		iter_test = model.iter_next(iter_test)
	return target_iter


def get_theme():
	global SHELL_THEME
	SHELL_THEME = Settings.get_string(THEME_SETTINGS_KEY)
	ComboBox_shell.set_active_iter(get_iter(ComboBox_shell.get_model(),SHELL_THEME))

def CheckGdmCompatibility() :
	state = Gio.file_new_for_path('/usr/share/themes/'+SHELL_THEME+'/gnome-shell/gdm.css').query_exists(None)
	if state or SHELL_THEME=="Adwaita" :
		Button_GDM.set_sensitive(True)
	else:
		Button_GDM.set_sensitive(False)

def shell_theme_changed(e):
	global SHELL_THEME
	SHELL_THEME = unquote(ComboBox_shell.get_active_text())
	Settings.set_string(THEME_SETTINGS_KEY,SHELL_THEME)
	CheckGdmCompatibility()

def gdm_button_clicked(e):
	SetUI('SHELL_THEME',SHELL_THEME)


#-----------------------------------------------
mainwin = Gtk.Window()
mainwin.connect("destroy",mainwin_close)
mainwin.set_border_width(4)
mainwin.set_position(Gtk.WindowPosition.CENTER)
mainwin.set_resizable(False)
mainwin.set_title(_("GnomeShell Theme Selector"))
mainwin.set_icon_name("preferences-desktop-theme")

VBox_Main = Gtk.VBox.new(False, 4)
mainwin.add(VBox_Main)

HBox_1 = Gtk.HBox.new(True, 4)
VBox_Main.pack_start(HBox_1, False, False, 4)

Label_shell = Gtk.Label(_("Shell theme"))
Label_shell.set_alignment(0,0.5)
HBox_1.pack_start(Label_shell, True, True, 4)

ComboBox_shell =  Gtk.ComboBoxText.new()
HBox_1.pack_start(ComboBox_shell, True, True, 4)

HBox_2 = Gtk.HBox.new(True, 4)
VBox_Main.pack_end(HBox_2, True, True, 0)

Button_GDM = Gtk.Button(_("Set this theme for GDM"))
HBox_2.pack_end(Button_GDM, False, False, 0)

#-------
mainwin.show_all()
load_theme_list()
get_theme()
CheckGdmCompatibility()

SETUP = Gio.file_new_for_path('/usr/bin/gdm3setup-daemon.py').query_exists(None) or \
Gio.file_new_for_path('/usr/bin/gdm3setup-daemon').query_exists(None)
if SETUP :
	bus = dbus.SystemBus()
	gdm3setup = bus.get_object('apps.nano77.gdm3setup','/apps/nano77/gdm3setup')
	SetUI = gdm3setup.get_dbus_method('SetUI','apps.nano77.gdm3setup')
	StopDaemon = gdm3setup.get_dbus_method('StopDaemon', 'apps.nano77.gdm3setup')
	Button_GDM.show()
else :
	Button_GDM.hide()


ComboBox_shell.connect("changed",shell_theme_changed)
Button_GDM.connect("clicked",gdm_button_clicked)


Gtk.main()
