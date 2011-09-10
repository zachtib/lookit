#!/usr/bin/env python2

import dbus
import dbus.service
import gobject
import os
import thread
import time

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

    @dbus.service.method(SERVICE_NAME)
    def capture_area(self):
        pass

    @dbus.service.method(SERVICE_NAME)
    def capture_screen(self):
        pass

    @dbus.service.method(SERVICE_NAME)
    def capture_window(self):
        pass

    @dbus.service.method(SERVICE_NAME, in_signature='s')
    def upload_file(self, filename):
        print('Uploading {0}...'.format(filename))

    @dbus.service.method(SERVICE_NAME)
    def show_preferences_dialog(self):
        pass

    @staticmethod
    def get_service_or_start():
        print('Starting...')
        bus = dbus.SessionBus()
        if SERVICE_NAME not in bus.list_names():
            print('Forking the service...')
            pid = os.fork()
            print pid
            if pid == 0:
                LookitService().start()
            else:
                while SERVICE_NAME not in bus.list_names():
                    try:
                        if os.waitpid(pid, os.WNOHANG) != (0, 0):
                            return None
                    except OSError as e:
                        if e.errno == errno.ECHILD:
                            return None
                    time.sleep(0.1)
        print('Now connecting...')
        service = bus.get_object(SERVICE_NAME, SERVICE_PATH)
        return service

if __name__ == '__main__':
    print('Attempting to connect to dbus service...')
    service = LookitService.get_service_or_start()
    service.get_dbus_method('upload_file', SERVICE_NAME)('Banana Phone')
    service.get_dbus_method('stop', SERVICE_NAME)()
