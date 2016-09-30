import os
from os.path import expanduser
import validators
from selenium import webdriver
from pyvirtualdisplay import Display
from fogbugz import FogBugz

fb = FogBugz("https://cloudant.fogbugz.com")
fb.logon("harshdeep.harshdeep@uk.ibm.com","Harsh1996")

def main(source,times=None):
	display = Display(visible=0, size=(800, 600))
	display.start()
	driver = webdriver.Firefox() #Using chrome web driver
	if not validators.url(source): 
		boolexists = os.path.exists('output.html')
		home = expanduser("~")
		driver.get("file://" + home + "/templates/" +source)
	else:
		driver.get(source) #Fill in URL
	how_many_screenshots(driver,times)
	driver.quit()
	display.stop()

	#Does not find file

def how_many_screenshots(driver,times):
	elementHeight = driver.find_element_by_tag_name("body").size['height'] 
	if times is None:
		driver.save_screenshot('screenshot_full.png')
		file = open('screenshot_full.png', 'r')
		fb.edit(ixBug=73752, Files={'screenshot_full.png': file})
	else:
		portions = 0
		temp = elementHeight / times
		while(portions < elementHeight):
			x = driver.execute_script("window.scrollBy(0, %d); return 5;" % portions)
			driver.save_screenshot('screenshot_full_%d.png' % portions) 
			file = open('screenshot_full_%d.png' % portions, 'r')
			#To check even if the height is getting added up
			fb.edit(ixBug=73752, sEvent="The portions is %d and answer %d and height %d and temp %d" %(portions,x,elementHeight,temp),Files={'screenshot_full_%d.png' % portions: file})
			portions += temp

if __name__ == '__main__':
    main('output.html',times=None)



