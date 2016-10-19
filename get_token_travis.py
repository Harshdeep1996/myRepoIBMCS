import os
import sys
import git
from datetime import datetime as dt
from datetime import timedelta

g = git.Git()
time_now = dt.now()
#print g.log()
print g.log("-1")
print "-------------------------------------------------------------------------------------------"
print g.log("-1","test.xml")
print "-------------------------------------------------------------------------------------------"
print g.log("-1","--pretty='%ci'","test.xml")
print "-------------------------------------------------------------------------------------------"
x = g.log("-1","--pretty='%ct'","test.xml")
#print(dt.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S'))
sys.stderr.write("The time now is %s \n" %str(time_now))
sys.stderr.write("Age of file is: %s" %str(file_age))

