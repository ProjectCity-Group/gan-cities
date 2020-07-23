import gi
import numpy as np
import citygan_util
gi.require_version("Gtk", "3.0")
import threading, queue
from gi.repository import Gtk, Gdk, GdkPixbuf
from citygan import CityGan
import pix2pix_citygenerator


class GanCities(Gtk.Window):
    def __init__(self):
        super(GanCities, self).__init__()
        self.generator = CityGan()
        try:
            self.generator.loadModel('models/citygan')
            self.pix2pix = pix2pix_citygenerator.pix2pix_citygen()
        except OSError:
            print("Models should be loaded in ./models/")
            print("Failed to load modules. Exiting gracefully.")
            exit(1)
        # self.countries = self.generator.getValidCountries()
        self.current_model=0
        self.map_data = []
        self.pixbuf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 400, 400)
        self.q = queue.Queue()
        thread = threading.Thread(target=self.get_work)
        thread.daemon = True
        thread.start()
        self.initialize_ui()

    def get_work(self):
        while True:
            self.q.get()


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
        self.gan_generate_button.connect("clicked", self.gan_generate_clicked)
        self.gan_save_button = Gtk.Button(label="Save Map")
        # self.gan_save_button.connect("clicked", self.save_map)
        self.gan_save_button.set_sensitive(False)
        self.pix2pix_save_button = Gtk.Button(label="Save Map")
        # self.pix2pix_save_button.connect("clicked", self.save_map)
        self.pix2pix_save_button.set_sensitive(False)
        ## pix2pix Model
        # Load Image
        self.load_button = Gtk.Button(label="Load PNG")
        # self.load_button.connect("clicked", self.on_load_clicked)
        # Generate Map
        self.pix2pix_generate_button = Gtk.Button(label="Make a Map")
        # self.pix2pix_generate_button.connect("clicked", self.pix2pix_generate)

        # Packing
        self.gan_options_box.pack_start(self.gan_generate_button, False, True, 10)
        self.gan_options_box.pack_end(self.gan_save_button, False, True, 10)
        self.pix2pix_options_box.pack_start(self.load_button, False, True, 10)
        self.pix2pix_options_box.pack_start(self.pix2pix_generate_button, False, True, 10)
        self.pix2pix_options_box.pack_start(self.pix2pix_save_button, False, True, 10)
        self.add(self.horiz_box)
        self.show_all()
    # Resizing Functions
    def on_check_resize(self, window):
        allocation = self.image_area.get_allocation()
        self.image_area.set_allocation(allocation)
        self.q.put(self.resizeImage(allocation.width, allocation.height))

    def resizeImage(self, x, y):
        self.scale_pixbuf = self.pixbuf.scale_simple(x, y, GdkPixbuf.InterpType.BILINEAR)
        self.image_area.set_from_pixbuf(None)
        self.image_area.queue_draw()

    def on_draw(self, win, cr):
        Gdk.cairo_set_source_pixbuf(cr, self.scale_pixbuf, 5, 5)
        cr.paint()

    def gan_generate_clicked(self, widget):
        self.q.put(self.get_map())

    def get_map(self):
        self.map_data = self.generator.generateMap()
        self.map_array = self.map_data.astype(np.uint8)
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_data(self.map_array.tobytes(), GdkPixbuf.Colorspace.RGB, False, 8, self.map_data.shape[1], self.map_data.shape[0], self.map_data.shape[1]*3)
        self.gan_save_button.set_sensitive(True)
        self.pix2pix_generate_button.set_sensitive(False)
        self.pix2pix_save_button.set_sensitive(False)
        self.image_area.set_from_pixbuf(self.scale_pixbuf)


def main():
    application = GanCities()
    Gtk.main()

if __name__ == "__main__":
    main()
