import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class DrawingAreaWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Sketchpad")
        self.set_default_size(800, 600)
        
        # Creating a scrolled window for drawing area
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        # Drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(842, 595)  # A4 format (poziomo)
        self.drawing_area.connect('draw', self.on_draw)
        self.drawing_area.connect('motion-notify-event', self.on_motion)
        self.drawing_area.connect('button-press-event', self.on_button_press)
        self.drawing_area.connect('button-release-event', self.on_button_release)
        self.drawing_area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.POINTER_MOTION_MASK)
        scrolled_window.add(self.drawing_area)
        
        # Toolbar
        toolbar = Gtk.Toolbar()
        undo_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_UNDO)
        redo_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REDO)
        clear_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_CLEAR)
        
        # Create a ToolItem for the color button
        self.color_button = Gtk.ColorButton.new_with_rgba(Gdk.RGBA(0, 0, 0, 1))
        self.color_button.connect('color-set', self.on_color_button_clicked)
        color_tool_item = Gtk.ToolItem()
        color_tool_item.add(self.color_button)
        
        undo_button.connect("clicked", self.on_undo_clicked)
        redo_button.connect("clicked", self.on_redo_clicked)
        clear_button.connect("clicked", self.on_clear_clicked)
        toolbar.insert(undo_button, 0)
        toolbar.insert(redo_button, 1)
        toolbar.insert(clear_button, 2)
        toolbar.insert(color_tool_item, 3)  # Insert the color button as a ToolItem
        
        # Layout
        vbox = Gtk.VBox()
        vbox.pack_start(toolbar, False, False, 0)
        vbox.pack_start(scrolled_window, True, True, 0)
        self.add(vbox)
        
        self.is_drawing = False
        self.connect('scroll-event', self.on_scroll)
        
        self.elements = []
        self.current_element_id = 0
        self.brush_size = 10
        self.color = Gdk.RGBA(0, 0, 0, 1)  # Domyślny kolor pędzla/olówka

    def on_draw(self, widget, cr):
        cr.set_source_rgb(1, 1, 1)
        cr.paint()

        for element in self.elements:
            cr.set_source_rgba(element['color'].red, element['color'].green, element['color'].blue, 1.0)
            cr.set_line_width(element['brush_size'])
            cr.move_to(element['points'][0][0], element['points'][0][1])
            for point in element['points'][1:]:
                cr.line_to(point[0], point[1])
            cr.stroke()

    def on_motion(self, widget, event):
        if self.is_drawing:
            self.current_element['points'].append((event.x, event.y))
            widget.queue_draw()

    def on_button_press(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY or event.keyval == Gdk.KEY_space:
            self.is_drawing = True
            self.current_element = {
                'id': self.current_element_id,
                'points': [(event.x, event.y)],
                'brush_size': self.brush_size,
                'color': Gdk.RGBA(self.color.red, self.color.green, self.color.blue, 1.0)
            }
            self.elements.append(self.current_element)
            self.current_element_id += 1

    def on_button_release(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY or event.keyval == Gdk.KEY_space:
            self.is_drawing = False

    def on_scroll(self, widget, event):
        if event.direction == Gdk.ScrollDirection.UP:
            self.brush_size += 1
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.brush_size -= 1 if self.brush_size > 1 else 0
        return True

    def on_undo_clicked(self, button):
        if self.elements:
            del self.elements[-1]
            self.drawing_area.queue_draw()

    def on_redo_clicked(self, button):
        # Implement redo logic if necessary
        pass

    def on_clear_clicked(self, button):
        self.elements.clear()
        self.drawing_area.queue_draw()

    def on_color_button_clicked(self, widget):
        self.color = widget.get_rgba()

    def color_to_rgb(self, color):
        return color.red, color.green, color.blue

win = DrawingAreaWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

