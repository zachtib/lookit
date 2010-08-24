import gtk

class ScreenCapper:
        def __init__(self):
                self.root = gtk.gdk.get_default_root_window()
                self.mask = gtk.gdk.BUTTON_RELEASE_MASK \
                          | gtk.gdk.POINTER_MOTION_MASK \
                          | gtk.gdk.BUTTON_MOTION_MASK \
                          | gtk.gdk.BUTTON_PRESS_MASK
                self.cursor = gtk.gdk.Cursor(gtk.gdk.CROSS)

                self.pixbuf = None
                
                self.gc = self.root.new_gc(
                                line_width = 1,
                                line_style = gtk.gdk.LINE_SOLID,
                                foreground = gtk.gdk.Color(0, 0, 65535),
                                background = gtk.gdk.Color(0, 0, 0),
                                  function = gtk.gdk.XOR,
                                      fill = gtk.gdk.SOLID,
                                 cap_style = gtk.gdk.CAP_BUTT,
                                join_style = gtk.gdk.JOIN_MITER,
                        graphics_exposures = True,
                            subwindow_mode = gtk.gdk.INCLUDE_INFERIORS
                )
                '''
                self.gc = self.xroot.create_gc(
                        line_width = 1,
                        line_style = X.LineSolid,
                        fill_style = X.FillSolid,
                        fill_rule = X.WindingRule,
                        cap_style = X.CapButt,
                        join_style = X.JoinMiter,
                        foreground = self.xcolor,
                        background = self.display.screen().black_pixel,
                        function = X.GXxor,
                        graphics_exposures = False,
                        subwindow_mode = X.IncludeInferiors,
                        )
                '''

                self.down = False
                self.x = None
                self.y = None
                self.down_x = None
                self.down_y = None
                self.up_x = None
                self.up_y = None
                self.old_x = None
                self.old_y = None

        def handle_event(self, event):
                if event.type == gtk.gdk.BUTTON_PRESS:
                        self.button_press_event(None, event)
                elif event.type == gtk.gdk.BUTTON_RELEASE:
                        self.button_release_event(None, event)
                elif event.type == gtk.gdk.MOTION_NOTIFY:
                        self.motion_notify_event(None, event)
                else:
                        print event


        def key_press_event(self, event):
                self.down = False
                gtk.gdk.pointer_ungrab()
                gtk.main_quit()
        
        def button_press_event(self, widget, event):
                self.x = int(event.x)
                self.y = int(event.y)
                
                self.x_down = self.x
                self.y_down = self.y

                self.down = True
                
                print 'Button Press at ({0},{1})'.format(self.x, self.y)

        def button_release_event(self, widget, event):
                gtk.gdk.pointer_ungrab()
                
                self.x = int(event.x)
                self.y = int(event.y)

                self.draw_rect()
                
                self.x_up = self.x
                self.y_up = self.y

                self.down = False

                print 'Button Release at ({0},{1})'.format(self.x, self.y)

                startx = min(self.x_down, self.x_up)
                starty = min(self.y_down, self.y_up)
                width  = abs(self.x_down - self.x_up)
                height = abs(self.y_down - self.y_up)

                self.pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,
                                             False, 8, width, height)
                self.pixbuf.get_from_drawable(self.root,
                                              self.root.get_colormap(),
                                              startx, starty, 0, 0,
                                              width, height)
                self.result = True
                gtk.main_quit()

        def motion_notify_event(self, widget, event):
                if not self.down:
                        return
                if self.old_x and self.old_y:
                        self.draw_rect()
                
                self.x = int(event.x)
                self.y = int(event.y)
                print event.x, event.y
                
                self.old_x = self.x
                self.old_y = self.y
                
                self.draw_rect()

        def draw_rect(self):
                startx = min(self.x_down, self.old_x)
                starty = min(self.y_down, self.old_y)
                width  = abs(self.x_down - self.old_x)
                height = abs(self.y_down - self.old_y)
                print 'Rect:', startx, starty, width, height
                self.root.draw_rectangle(self.gc, False, startx, starty,
                                         width, height)

        def capture_screen(self):
                self.pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False,
                                             8, self.size[0], self.size[1])
                self.pixbuf.get_from_drawable(self.root,
                                              self.root.get_colormap(),
                                              0, 0, 0, 0, self.size[0],
                                              self.size[1])
                return self.pixbuf

        def capture_area(self):
                self.pixbuf = None
                self.result = False
                self.rect = False
                gtk.gdk.pointer_grab(self.root,
                                     event_mask = self.mask,
                                     cursor = self.cursor)

                gtk.gdk.event_handler_set(self.handle_event)
                
                gtk.main()
                
                return self.pixbuf
