import cairo
import gtk
import gtk.gdk

class Selector:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0

        self.mouse_down = False

        self.overlay = gtk.Window(gtk.WINDOW_POPUP)

        self.overlay.set_app_paintable(True)
        self.overlay.set_decorated(False)

        self.overlay.add_events(gtk.gdk.POINTER_MOTION_MASK |
                                gtk.gdk.BUTTON_PRESS_MASK |
                                gtk.gdk.BUTTON_RELEASE_MASK |
                                gtk.gdk.KEY_PRESS_MASK)

        self.overlay.connect('expose-event',            self.expose)
        self.overlay.connect('screen-changed',          self.screen_changed)
        self.overlay.connect('realize',                 self.realize)
        self.overlay.connect('show',                    self.on_show)
        self.overlay.connect('button-press-event',      self.button_pressed)
        self.overlay.connect('button-release-event',    self.button_released)
        self.overlay.connect('motion-notify-event',     self.motion_notify)
        self.overlay.connect('key-press-event',         self.key_pressed)

    def expose(self, widget, event=None):
        cr = widget.window.cairo_create()

        cr.set_source_rgba(0.125, 0.125, 0.125, 0.75)

        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        if self.mouse_down:
            cr.set_source_rgba(0, 0, 0, 0)
            cr.rectangle(self.x, self.y, self.dx, self.dy)
            cr.fill()
            cr.stroke()

        return False

    def screen_changed(self, widget, old_screen=None):
        screen = widget.get_screen()
        widget.move(0, 0)
        widget.resize(screen.get_width(), screen.get_height())

        colormap = screen.get_rgba_colormap()
        widget.set_colormap(colormap)

        return True

    def realize(self, widget):
        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSS))
        gtk.gdk.keyboard_grab(widget.window)

    def on_show(self, widget):
        gtk.gdk.keyboard_grab(widget.window)

    def button_pressed(self, widget, event):
        self.mouse_down = True
        self.x = event.x
        self.y = event.y

    def button_released(self, widget, event):
        self.mouse_down = False
        gtk.main_quit()

    def motion_notify(self, widget, event):
        self.dx = event.x - self.x
        self.dy = event.y - self.y

        self.expose(self.overlay)

    def key_pressed(self, widget, event):
        if event.keyval == gtk.gdk.keyval_from_name('Escape'):
            gtk.main_quit()
        else:
            return False

    def get_selection(self):
        self.screen_changed(self.overlay)
        self.overlay.show_all()
        gtk.main()
        return self.x, self.y, self.dx, self.dy

if __name__ == '__main__':
    # For testing purposes only
    print Selector().get_selection()
