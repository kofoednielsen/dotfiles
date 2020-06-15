#!/usr/bin/python
from datetime import datetime


RED_B = '\033[41m'
END = '\033[0m'
with open('/sys/class/power_supply/BAT0/capacity') as f:
    battery = f.read().strip()
    time = datetime.now().strftime('%H:%M:%S')
    warning = ''
    if int(battery) < 10:
        warning = '#### LOW BATTERY ####'
    print(f'{warning.ljust(68)} bat: {battery}%    {time}  ')
