import time
from selenium import webdriver
from pyvirtualdisplay import Display


def main(source, times=None):
    display = Display(visible=0, size=(800, 600))
    display.start()
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/chromium-browser'
    options.add_argument(
        "--no-sandbox", "--no-default-browser-check",
        "--no-first-run", "--disable-default-apps")
    driver = webdriver.Chrome(
        '/home/travis/virtualenv/python2.7.9/chromedriver',
        chrome_options=options)
    driver.get(source)
    how_many_screenshots(driver, times)
    driver.quit()
    display.stop()


def how_many_screenshots(driver, times):
    elementHeight = driver.find_element_by_tag_name("body").size['height']
    if times is None:
        driver.save_screenshot('screenshot_full.png')
    else:
        portions = 0
        temp = elementHeight / times
        while(portions < elementHeight):
            driver.execute_script("window.scrollTo(0, %d);" % portions)
            time.sleep(2)
            driver.save_screenshot('screenshot_full_%d.png' % portions)
            portions += temp

if __name__ == '__main__':
    main(source, times=None)
