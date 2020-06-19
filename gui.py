import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
import gancities


class GanCities(Gtk.Window):
    def __init__(self):
        super(GanCities, self).__init__()
        self.generator = gancities.CityGenerator()
        self.countries = self.generator.getValidCountries()
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("gui_placeholder_images/sample.png")
        self.initialize_ui()
        self.load_image()

    def initialize_ui(self):
        self.horiz_box = Gtk.Box()
        self.resize(600,400)
        self.options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.image_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.horiz_box.pack_start(self.options_box, False, True, 10)
        self.horiz_box.pack_start(self.image_box, True, True, 10)
        self.image_area = Gtk.DrawingArea()
        self.image_area.connect("draw", self.on_draw)
        self.image_box.pack_start(self.image_area, True, True, 10)
        self.set_title("GanCities")
        self.connect("check_resize", self.on_check_resize)
        self.connect("delete-event", Gtk.main_quit)
        self.train_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.train_label = Gtk.Label(label="Training Folder:")
        self.train_folder_select = Gtk.FileChooserButton(title="Training Folder", action=Gtk.FileChooserAction.SELECT_FOLDER)
        self.train_button = Gtk.Button(label="Start Training")
        self.train_button.connect("clicked", self.train_clicked, self.generator, self.train_folder_select)
        self.train_box.pack_start(self.train_label, False, True, 10)
        self.train_box.pack_start(self.train_folder_select, False, False, 10)
        self.train_box.pack_start(self.train_button,True, True, 10)
        ### TODO Combobox doesn't work
        self.country_model = Gtk.ListStore(str)
        for country in self.generator.getValidCountries():
            print(country)
            self.country_model.append([country])
        self.country_style=Gtk.ComboBox.new_with_model(self.country_model)
        self.country_style.set_entry_text_column(0)
        ### End of ComboBox Code
        self.options_box.pack_start(self.train_box, True, True, 10)
        self.options_box.pack_start(self.country_style, False, False, 10)
        self.button = Gtk.Button(label="Make a map")
        self.button.connect("clicked", self.on_button_clicked)
        self.options_box.pack_start(self.button, True, True, 10)
        self.add(self.horiz_box)
        self.show_all()

    def on_check_resize(self, window):
        allocation = self.image_area.get_allocation()
        self.image_area.set_allocation(allocation)
        self.resizeImage(allocation.width, allocation.height)

    def load_image(self):
        self.scale_pixbuf = self.pixbuf.scale_simple(400, 400, GdkPixbuf.InterpType.BILINEAR)

    def resizeImage(self, x, y):
        self.scale_pixbuf = self.pixbuf.scale_simple(x, y, GdkPixbuf.InterpType.BILINEAR)

    def on_draw(self, win, cr):
        Gdk.cairo_set_source_pixbuf(cr, self.scale_pixbuf, 5, 5)
        cr.paint()

    def on_button_clicked(self, widget):
        print("Hello world!")

    def train_clicked(self, widget, generator, chooser):
        if chooser.get_file() is not None:
            generator.train(chooser.get_file().get_uri())
def main():
    application = GanCities()
    Gtk.main()


if __name__ == "__main__":
    main()
