from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from PIL import Image

from webdriver_manager.chrome import ChromeDriverManager

# Global Constants
# On average, three seconds seems to be a good buffer for loading the page/elements
LOAD_WAIT_TIME = 3
# We need at least one second to get a good screenshot
SCREENSHOT_TIME = 1

f = open('addresses.txt',"r", encoding="utf8")
# Using Chrome to access web
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
# Open the website
driver.get('https://snazzymaps.com/style/127403/no-label-bright-colors')
print(driver.title)


time.sleep(LOAD_WAIT_TIME)
# Closes out the ad on the map
driver.find_element_by_xpath("/html/body/main/div[1]/button").click()
# Closes the side menu
driver.find_element_by_xpath("/html/body/main/div[2]/button[2]").click()

# The default_path_location variable holds the directory where the photos will be stored.
# I highly recommend saving it to one of your spare hard drives with lots of space.

# CDW_file_location = "E:/Map Photos/Attempt2/"
default_path_location = "C:/Users/Public/Pictures/"

default_filename = default_path_location

for line in f:

    # Initializer for the names of the original screenshot and all crops.
    split_line = line.split(",")
    filename = default_filename + split_line[1] + "-" + split_line[0] + ".png"
    filename_mod_1= default_filename + split_line[1] + "-" + split_line[0] + "-1" + ".png"
    filename_mod_2= default_filename + split_line[1] + "-" + split_line[0] + "-2" + ".png"
    filename_mod_3= default_filename + split_line[1] + "-" + split_line[0] + "-3" + ".png"
    filename_mod_4 = default_filename + split_line[1] + "-" + split_line[0] + "-4" + ".png"
    filename_mod_5 = default_filename + split_line[1] + "-" + split_line[0] + "-5" + ".png"
    filename_mod_6 = default_filename + split_line[1] + "-" + split_line[0] + "-6" + ".png"

    # File location debug info
    print(filename)

    # Access the map search bar and enter the next location
    search = driver.find_element_by_id("map-location-search")
    search.send_keys(line)

    # Wait for options to load and then enter on the first related entry in the map search bar
    time.sleep(LOAD_WAIT_TIME)
    search.send_keys(Keys.ARROW_DOWN)
    search.send_keys(Keys.RETURN)

    # Wait for the location to load and then click the zoom buttons for the map twice
    time.sleep(LOAD_WAIT_TIME)
    driver.find_element_by_xpath(
        "/html/body/main/div[3]/div[1]/div[1]/div/div/div/div/div/div[8]/div/div/button[1]").click()
    driver.find_element_by_xpath(
        "/html/body/main/div[3]/div[1]/div[1]/div/div/div/div/div/div[8]/div/div/button[1]").click()

    # Wait for zoom, then screenshot
    time.sleep(SCREENSHOT_TIME)
    driver.save_screenshot(filename)
    im = Image.open(filename)

    # Crops of the full dimension screenshot, 6 in total
    im.crop((40,54,640,654 )).save(filename_mod_1)
    im.crop((640,54,1240,654 )).save(filename_mod_2)
    im.crop((940,54,1540,654 )).save(filename_mod_3)
    im.crop((40,200,640,800 )).save(filename_mod_4)
    im.crop((640,200,1240,800 )).save(filename_mod_5)
    im.crop((940,200,1540,800 )).save(filename_mod_6)
    search.clear()

