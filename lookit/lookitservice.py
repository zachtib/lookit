#!/usr/bin/env python2

import dbus
import dbus.service
import gobject

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

SERVICE_NAME = 'org.gnome.lookitservice'
SERVICE_PATH = '/org/gnome/lookitservice'

class LookitService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName(SERVICE_NAME, bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, SERVICE_PATH)
        self.loop = gobject.MainLoop()

    def start(self):
        print('Starting Lookit Service...')
        self.loop.run()

    @dbus.service.method(SERVICE_NAME)
    def stop(self):
        print('Stopping Lookit Service')
        self.loop.quit()

if __name__ == '__main__':
    service = LookitService()
    service.start()

