# synctime.py
import os
import ntplib
import datetime
import time


start = datetime.datetime.now()
c = ntplib.NTPClient()
host = 'edu.ntp.org.cn'
response = c.request(host)
current_time = response.tx_time
_date, _time = str(datetime.datetime.fromtimestamp(current_time))[:22].split(' ')
end = datetime.datetime.now()
print(end-start)
print("系统当前时间", str(datetime.datetime.now())[:22])
print("北京标准时间", _date, _time)
# a, b, c = _time.split(':')
# c = float(c) + 0.5
# _time = "%s:%s:%s" % (a, b, c)
os.system('date %s && time %s' % (_date, _time))
print("同步后时间:", str(datetime.datetime.now()))
# os.system("pause")
