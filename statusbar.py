#!/usr/bin/python
from datetime import datetime
from typing import List
import socket
import yaml
import psutil


RED_B = '\033[41m'
END = '\033[0m'
battery = ""
chargin = ""
with open('/sys/class/power_supply/BAT0/capacity') as f:
    battery = f.read().strip()
with open('/sys/class/power_supply/BAT0/status') as f:
    charging = f.read().strip() == "Charging"

# ░█▀▄░█▀█░▀█▀░▀█▀░█▀▀░█▀▄░█░█
# ░█▀▄░█▀█░░█░░░█░░█▀▀░█▀▄░░█░
# ░▀▀░░▀░▀░░▀░░░▀░░▀▀▀░▀░▀░░▀░
warning = ''
if int(battery) < 10 and not charging:
    warning = '⚠️ LOW BATTERY ⚠️ '
if int(battery) > 90 and charging:
    warning = '⚠️ FULL BATTERY ⚠️ '
battery_icon = '🔌' if charging else ''


# ░█▀▀░█▄█░█▀█░▀▀█░▀█▀░█▀▀░█▀█░▀█▀░█▀█░█▀▄
# ░█▀▀░█░█░█░█░░░█░░█░░█░░░█▀█░░█░░█░█░█▀▄
# ░▀▀▀░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀

emojis = yaml.load(open('/home/kofoednielsen/dotfiles/emojicator.yaml'),
                   Loader=yaml.FullLoader)
default_emoji = emojis['default']


def get_emoji(emojis: List[dict], percent: int) -> dict:
    return max(filter(lambda e: percent > e['from'], emojis),
               key=lambda e: e['from'],
               default=default_emoji)


# get system stats for cpu and memory
ram_percent = psutil.virtual_memory().percent
# get the most stressed core
cpu_percent = max(psutil.cpu_percent(percpu=True))
# find out which emojis matches state of the system
ram_emoji = get_emoji(emojis['ram'], ram_percent)
cpu_emoji = get_emoji(emojis['cpu'], cpu_percent)
# battery is inversed, cause higher is better
bat_emoji = get_emoji(emojis['bat'], 100-int(battery))
# find the most critical emoji
emoji_options = [ram_emoji, cpu_emoji, bat_emoji]
emoji = max(emoji_options, key=lambda e: e['from'])['emoji']


time = datetime.now().strftime('%H:%M:%S')
ip = socket.gethostbyname(socket.gethostname())

print(f'{warning.ljust(60)}{ip}    {battery_icon}{time}  {emoji}')
