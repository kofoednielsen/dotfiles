#!/usr/bin/python
import netifaces
from datetime import datetime
from os import system
from pathlib import Path
from requests import get
from typing import List
import os
import psutil
import socket
import yaml


RED_B = '\033[41m'
END = '\033[0m'
battery = "50"
charging = ""
HOME = os.getenv('HOME')

with open('/sys/class/power_supply/BAT0/capacity') as f:
    battery = f.read().strip()
with open('/sys/class/power_supply/BAT0/status') as f:
    charging = f.read().strip() == "Charging"

# ░█▀▄░█▀█░▀█▀░▀█▀░█▀▀░█▀▄░█░█
# ░█▀▄░█▀█░░█░░░█░░█▀▀░█▀▄░░█░
# ░▀▀░░▀░▀░░▀░░░▀░░▀▀▀░▀░▀░░▀░
warning = ''
if int(battery) <= 10 and not charging:
    warning = '⚠️ LOW BATTERY ⚠️ '
if int(battery) >= 90 and charging:
    warning = '⚠️ FULL BATTERY ⚠️ '


# ░█▀▀░█▄█░█▀█░▀▀█░▀█▀░█▀▀░█▀█░▀█▀░█▀█░█▀▄
# ░█▀▀░█░█░█░█░░░█░░█░░█░░░█▀█░░█░░█░█░█▀▄
# ░▀▀▀░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀

emojis = yaml.load(open(f'{HOME}/dotfiles/emojicator.yaml'),
                   Loader=yaml.FullLoader)
default_emoji = emojis['default']


def get_emoji(emojis: List[dict], percent: int) -> dict:
    return max(filter(lambda e: percent > e['from'], emojis),
               key=lambda e: e['from'],
               default=default_emoji)


# get system stats for cpu and memory
ram_percent = psutil.virtual_memory().percent

# get the most stressed core
cpu_percent = max(psutil.cpu_percent(interval=0.1, percpu=True))

# find out which emojis matches state of the system
ram_emoji = get_emoji(emojis['ram'], ram_percent)
cpu_emoji = get_emoji(emojis['cpu'], cpu_percent)
# battery is inversed, cause higher is better
bat_emoji = get_emoji(emojis['bat'], 100-int(battery))
charging_emoji = '⚡' if charging else ' '

# find the most critical emoji
emoji_options = [ram_emoji, cpu_emoji, bat_emoji]
emoji = max(emoji_options, key=lambda e: e['from'])['emoji']


time = datetime.now().strftime('%d/%m  %H:%M:%S')
ips = []

for i in netifaces.interfaces(): #Will cycle through all available interfaces and check each one.
    if i != "lo": #This will remove lo from the interfaces it checks.
        try:
            ips.append(netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr'])
        except:
            pass

hex_code = f'{ord(emoji):x}'
path = Path(f'{HOME}/dotfiles/emojis/{hex_code}.png')
if path.is_file():
    emoji_img = open(path, 'rb').read()
else:
    url = f"https://noto-website-2.storage.googleapis.com/emoji/emoji_u{hex_code}.png"
    emoji_img = get(url).content
    open(path, 'wb').write(emoji_img)
open(f'{HOME}/dotfiles/background.png', 'wb').write(emoji_img)
# system("swaymsg output '*' background /home/asbi/dotfiles/background.png center")

print(f'{warning.ljust(60)}{"    ".join(ips)}    {time}    {charging_emoji}{emoji}')
