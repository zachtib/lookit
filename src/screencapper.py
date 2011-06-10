import gtk
import time

def capture_screen():
    time.sleep(1)
    root = gtk.gdk.get_default_root_window()
    size = root.get_geometry()
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False,
                     8, size[2], size[3])
    pixbuf.get_from_drawable(root,
                      root.get_colormap(),
                      0, 0, 0, 0, size[2],
                      size[3])
    return pixbuf

def capture_active_window():
    time.sleep(1)
    root = gtk.gdk.get_default_root_window()
    window = gtk.gdk.screen_get_default().get_active_window()
    size = window.get_geometry()
    origin = window.get_root_origin()
    # Calculating window decorations offset
    delta_x = window.get_origin()[0] - window.get_root_origin()[0]
    delta_y = window.get_origin()[1] - window.get_root_origin()[1]
    size_x = size[2] + delta_x
    size_y = size[3] + delta_y
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False,
                     8, size_x, size_y)
    pixbuf.get_from_drawable(root,
                      root.get_colormap(),
                      origin[0], origin[1], 0, 0, size_x, size_y)
    return pixbuf

def capture_selection(rect):
    root = gtk.gdk.get_default_root_window()
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,
                     False, 8, rect[2], rect[3])
    pixbuf.get_from_drawable(root,
                      root.get_colormap(),
                      rect[0], rect[1], 0, 0,
                      rect[2], rect[3])
    return pixbuf
