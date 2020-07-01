import gi
import numpy as np
import citygan_util
import time
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
from citygan import CityGan
import pix2pix_citygenerator


class GanCities(Gtk.Window):
    def __init__(self):
        super(GanCities, self).__init__()
        self.generator = CityGan()
        self.generator.loadModel('models/citygan')
        self.pix2pix = pix2pix_citygenerator.pix2pix_citygen()
        # self.countries = self.generator.getValidCountries()
        self.current_model=0
        self.map_data = []
        self.pixbuf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 400, 400)
        self.initialize_ui()

    def initialize_ui(self):
        # Layout
        self.horiz_box = Gtk.Box()
        self.resize(600,400)
        self.options_book = Gtk.Notebook()
        self.model_select_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.gan_options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.pix2pix_options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.options_book.append_page(child=self.gan_options_box, tab_label=Gtk.Label(label="GanCities"))
        self.options_book.append_page(child=self.pix2pix_options_box, tab_label=Gtk.Label(label="pix2pix"))
        self.image_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.horiz_box.pack_start(self.options_book, False, True, 10)
        self.horiz_box.pack_start(self.image_box, True, True, 10)
        self.set_title("GanCities")
        self.connect("check_resize", self.on_check_resize)
        self.connect("delete-event", Gtk.main_quit)
        # Image Display
        self.image_area = Gtk.Image()
        self.image_area.connect("draw", self.on_draw)
        self.image_box.pack_start(self.image_area, True, True, 10)
        # Training Selection
        # self.train_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.train_label = Gtk.Label(label="Training Folder:")
        # self.train_folder_select = Gtk.FileChooserButton(title="Training Folder", action=Gtk.FileChooserAction.SELECT_FOLDER)
        # self.train_button = Gtk.Button(label="Start Training")
        # self.train_button.connect("clicked", self.train_clicked, self.generator, self.train_folder_select)
        # self.train_box.pack_start(self.train_label, False, True, 10)
        # self.train_box.pack_start(self.train_folder_select, False, False, 10)
        # self.train_box.pack_start(self.train_button,True, True, 10)
        # Country Style Combobox
        # self.country_model = Gtk.ListStore(str)
        # for country in self.countries:
        #     self.country_model.append([country])
        # self.country_style = Gtk.ComboBox(model=self.country_model)
        # country_cell = Gtk.CellRendererText()
        # self.country_style.pack_start(country_cell, False)
        # self.country_style.add_attribute(country_cell, "text", 0)
        # self.country_style.set_entry_text_column(0)
        # self.country_style.set_active(0)
        # Population Spin Button
        # pop_adjustment = Gtk.Adjustment(value=1000, lower=1000, upper=10000000, step_increment=1000)
        # self.popspinner = Gtk.SpinButton(numeric=True)
        # self.popspinner.set_adjustment(pop_adjustment)
        # Dimensions
        self.dim_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.dimlabel1 = Gtk.Label(label="Map Dimensions")
        self.dimlabel2 = Gtk.Label(label="x")
        dim_xadjustment = Gtk.Adjustment(value=400, lower=200, upper=3440, step_increment=10)
        dim_yadjustment = Gtk.Adjustment(value=400, lower=200, upper=3440, step_increment=10)
        self.xspinner = Gtk.SpinButton(numeric=True, adjustment=dim_xadjustment)
        self.yspinner = Gtk.SpinButton(numeric=True, adjustment=dim_yadjustment)
        self.dim_box.pack_start(self.dimlabel1, True, True, 0)
        self.dim_box.pack_start(self.xspinner, True, True, 0)
        self.dim_box.pack_start(self.dimlabel2, True, True, 0)
        self.dim_box.pack_start(self.yspinner, True, True, 0)
        # Make Map button
        self.gan_generate_button = Gtk.Button(label="Make a map")
        self.gan_generate_button.connect("clicked", self.gan_generate)
        self.gan_save_button = Gtk.Button(label="Save Map")
        self.gan_save_button.connect("clicked", self.save_map)
        self.gan_save_button.set_sensitive(False)
        self.pix2pix_save_button = Gtk.Button(label="Save Map")
        self.pix2pix_save_button.connect("clicked", self.save_map)
        self.pix2pix_save_button.set_sensitive(False)
        ## pix2pix Model
        # Load Image
        self.load_button = Gtk.Button(label="Load PNG")
        self.load_button.connect("clicked", self.on_load_clicked)
        # Generate Map
        self.pix2pix_generate_button = Gtk.Button(label="Make a Map")
        self.pix2pix_generate_button.connect("clicked", self.pix2pix_generate)

        # Packing
        # self.options_box.pack_start(self.train_box, True, True, 10)
        # self.gan_options_box.pack_start(self.country_style, False, False, 10)
        # self.gan_options_box.pack_start(self.popspinner, False, True, 10)
        # self.gan_options_box.pack_start(self.dim_box, False, True, 10)
        self.gan_options_box.pack_start(self.gan_generate_button, False, True, 10)
        self.gan_options_box.pack_end(self.gan_save_button, False, True, 10)
        self.pix2pix_options_box.pack_start(self.load_button, False, True, 10)
        self.pix2pix_options_box.pack_start(self.pix2pix_generate_button, False, True, 10)
        self.pix2pix_options_box.pack_start(self.pix2pix_save_button, False, True, 10)
        self.add(self.horiz_box)
        self.show_all()

    def on_check_resize(self, window):
        allocation = self.image_area.get_allocation()
        self.image_area.set_allocation(allocation)
        self.resizeImage(allocation.width, allocation.height)

    def resizeImage(self, x, y):
        self.scale_pixbuf = self.pixbuf.scale_simple(x, y, GdkPixbuf.InterpType.BILINEAR)
        self.image_area.set_from_pixbuf(None)
        self.image_area.queue_draw()


    def on_draw(self, win, cr):
        Gdk.cairo_set_source_pixbuf(cr, self.scale_pixbuf, 5, 5)
        cr.paint()

    def gan_generate(self, widget):
        # x_dim = self.xspinner.get_value()
        # y_dim = self.yspinner.get_value()
        # self.generator.setDimensions(x_dim, y_dim)
        # self.generator.setCityPop(self.popspinner.get_value())
        # self.generator.setCountryStyle(self.countries[self.country_style.get_active()])
        self.map_data = self.generator.generateMap()
        self.map_array = self.map_data.astype(np.uint8)
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_data(self.map_array.tobytes(), GdkPixbuf.Colorspace.RGB, False, 8, self.map_data.shape[1], self.map_data.shape[0], self.map_data.shape[1]*3)
        self.gan_save_button.set_sensitive(True)
        self.pix2pix_generate_button.set_sensitive(False)
        self.pix2pix_save_button.set_sensitive(False)
        self.image_area.set_from_pixbuf(self.scale_pixbuf)


    def pix2pix_generate(self, widget):
        self.map_data = self.pix2pix.genImage()
        self.map_array = citygan_util.mapRangeToRange(self.map_data, [0, 1], [0, 255]).astype(np.uint8)
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_data(self.map_array.tobytes(), GdkPixbuf.Colorspace.RGB, False, 8, self.map_data.shape[1], self.map_data.shape[0], self.map_data.shape[1]*3)
        self.scale_pixbuf = self.pixbuf
        self.pix2pix_save_button.set_sensitive(True)
        self.gan_save_button.set_sensitive(False)
        self.image_area.set_from_pixbuf(self.scale_pixbuf)


    def train_clicked(self, widget, generator, chooser):
        if chooser.get_file() is not None:
            generator.train(chooser.get_file().get_uri())

    def save_map(self, widget):
        save_dialog = Gtk.FileChooserDialog(title="Save Map", action=Gtk.FileChooserAction.SAVE)
        save_dialog.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        save_dialog.connect("response", self.save_response)
        save_dialog.run()

    def save_response(self, dialog, response):
        current_page = self.options_book.get_current_page()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            if current_page == 0:
                self.generator.saveGeneratedMap(self.map_data, filename)
            elif current_page == 1:
                self.pix2pix.saveImage(self.map_data, filename)
        dialog.destroy()

    def on_load_clicked(self, widget):
        png_filter = Gtk.FileFilter()
        png_filter.set_name("PNG File")
        png_filter.add_mime_type("image/png")
        load_dialog = Gtk.FileChooserDialog(title="Select a png", action=Gtk.FileChooserAction.OPEN)
        load_dialog.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        load_dialog.add_filter(png_filter)
        load_dialog.connect("response", self.load_response)
        load_dialog.run()

    def load_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.pix2pix_generate_button.set_sensitive(True)
            self.pix2pix_save_button.set_sensitive(True)
            self.pix2pix.loadImage(filename)
        dialog.destroy()

def main():
    application = GanCities()
    Gtk.main()

if __name__ == "__main__":
    main()
