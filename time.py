# coding=utf-8
from __future__ import print_function
import time
from datetime import datetime, timedelta

dt = datetime.now()

print("Timestamp: %d" % time.mktime(dt.timetuple()))
print("Timestamp: %s" % datetime.strftime(dt, "%s"))
print("Timestamp: %f" % time.time())

print("Sleeping for 5 secs...")
time.sleep(5)

print("Datetime:\t%s" % datetime.strftime(dt, "%Y%m%d %H:%M:%S"))
print("UTC Time:\t%s" % datetime.strftime(dt.utcnow(), "%Y%m%d %H:%M:%S"))
print("New York Time:\t%s" % datetime.strftime(dt - timedelta(hours=12), "%Y%m%d %H:%M:%S"))

print("星期%d" % (dt.weekday() + 1))
print("Year:%d, Weeknumber:%d, Weekday:%d" % dt.isocalendar())
