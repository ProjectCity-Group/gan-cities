from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from random import randint
import time
import os


#Globals
LOAD_WAIT_TIME = 3
SCREENSHOT_TIME = 1
SITE1 = "http://fantasycities.watabou.ru/?size=40&"
SEED = "seed="
SITE2 = "&hub=0&random=1"

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# start driver
driver = webdriver.Chrome(ChromeDriverManager().install())
# set size
driver.set_window_size(512,512)
for i in range(1000):
    # gen rand seed
    randSeed = random_with_N_digits(10)
    driver.get(SITE1 + SEED + str(randSeed) + SITE2)
    time.sleep(LOAD_WAIT_TIME)
    
    # screenshot
    time.sleep(SCREENSHOT_TIME)
    driver.save_screenshot("tmpPage.png")
    # save to file
    im = Image.open('tmpPage.png')
    output = 'out/town' + str(i) + '.png'
    im.save(output)
    # print progress progress
    percentage = "{:.0%}".format(i/1000)
    print(percentage)

driver.quit()