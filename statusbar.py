#!/usr/bin/python
from datetime import datetime


with open('/sys/class/power_supply/BAT0/capacity') as f:
    battery = f.read().strip()
    time = datetime.now().strftime('%H:%M:%S')
    print(f'bat: {battery}%    {time}  ')
