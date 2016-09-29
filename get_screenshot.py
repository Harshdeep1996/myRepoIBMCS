import validators
from selenium import webdriver
from pyvirtualdisplay import Display

def main(source,times=None):
	display = Display(visible=0, size=(800, 600))
	display.start()
	driver = webdriver.Chrome() #Using chrome web driver
	if not validators.url(source): 
		driver.get('file://' + source)
	else:
		driver.get(source) #Fill in URL
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
			driver.execute_script("window.scrollBy(0, %d);" % portions)
			driver.save_screenshot('screenshot_full_%d.png' % portions)
			portions += temp

if __name__ == '__main__':
    main('./output.html',times=4)