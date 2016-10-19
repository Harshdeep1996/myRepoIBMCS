import os
import sys
import git
from datetime import datetime as dt
from datetime import timedelta

g = git.Git('myRepoIBMCS')
time_now = dt.now()
file_age = g.log('-1', '--pretty="%cI"', 'test.xml')[1:-7]
sys.stderr.write("The time now is %s \n" %str(time_now))
sys.stderr.write("Age of file is: %s" %str(file_age))