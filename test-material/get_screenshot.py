import os
import time
from selenium import webdriver
from pyvirtualdisplay import Display
from fogbugz import FogBugz

fb = FogBugz("https://cloudant.fogbugz.com")
fb.logon("harshdeep.harshdeep@uk.ibm.com","Harsh1996")

def main(source,times=None):
	display = Display(visible=0, size=(1024, 768))
	display.start()
	options = webdriver.ChromeOptions()
	options.binary_location = '/usr/bin/chromium-browser'
	#All the arguments added for chromium to work on selenium
	options.add_argument("--no-sandbox")
	options.add_argument("--no-default-browser-check")
	options.add_argument("--no-first-run")
	options.add_argument("--disable-default-apps")
	driver = webdriver.Chrome('/home/travis/virtualenv/python2.7.9/chromedriver',chrome_options=options)
	driver.get(source)
	how_many_screenshots(driver,times)
	driver.quit()
	display.stop()

def how_many_screenshots(driver,times):
	elementHeight = driver.find_element_by_tag_name("body").size['height'] 
	if times is None:
		driver.save_screenshot('screenshot_full.png')
	else:
		portions = 0
		temp = elementHeight / times
		while(portions < elementHeight):
			driver.execute_script("window.scrollTo(0, %d);" %portions)
			time.sleep(2)
			driver.save_screenshot('screenshot_full_%d.png' % portions) 
			portions += temp

if __name__ == '__main__':
	source = "http://localhost:8000/templates/output.html"
	main(source,times=4)



