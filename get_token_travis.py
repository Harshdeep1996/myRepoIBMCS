import os
import sys
import git
from datetime import datetime as dt
from datetime import timedelta
import pytz

g = git.Git()
bst = pytz.timezone('Europe/London')
time_now = dt.utcnow()
#print g.log()
print g.log("-1")
print "-------------------------------------------------------------------------------------------"
print g.log("-1","test.xml")
print "-------------------------------------------------------------------------------------------"
print g.log("-1","--pretty='%ci'","test.xml")
print "-------------------------------------------------------------------------------------------"
time_updated = dt.replace(bst.localize(dt.strptime(g.log('-1', '--pretty="%ci"', 'test.xml')[1:-7], "%Y-%m-%d %H:%M:%S")).astimezone(pytz.utc), tzinfo=None)
#print(dt.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S'))
sys.stderr.write("The time now is %s \n" %str(time_now))
sys.stderr.write("Age of file is: %s" %str(time_updated))

sys.stderr.write("The time difference between seconds: %s" %str((time_now - time_updated).total_seconds()))

