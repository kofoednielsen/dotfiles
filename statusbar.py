#!/usr/bin/python3
from datetime import datetime
from os import system
from pathlib import Path
from requests import get
from subprocess import Popen
from time import sleep
from typing import List
import netifaces
import os, signal
import psutil
import socket
import yaml


RED_B = '\033[41m'
END = '\033[0m'
battery = "50"
charging = ""
HOME = Path(os.getenv('HOME'))
TMP = Path("/tmp/")
DOTFILES_FOLDER = HOME / 'dotfiles'

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

emojis = yaml.load(open(DOTFILES_FOLDER / "emojicator.yaml"),
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
            ips.append((i, netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']))
        except:
            pass
if_map = { 'wlp9s0': 'wifi', 'enp0s31f6': 'lan' }
ip_str = "    ".join(f'{if_map.get(i, i)}: {ip}'for i, ip in ips if i in if_map )

# PRINT OUTPUT
print(f'{warning.ljust(45)}{ip_str}    {time}    {charging_emoji}{emoji}')


# HANDLE BACKGROUND
hex_code = f'{ord(emoji):x}'
emoji_path = DOTFILES_FOLDER / f"emojis/{hex_code}.png"
if emoji_path.is_file():
    emoji_img = open(emoji_path, 'rb').read()
else:
    url = f"https://github.com/googlefonts/noto-emoji/raw/main/png/512/emoji_u{hex_code}.png"
    emoji_img = get(url).content
    open(emoji_path, 'wb').write(emoji_img)

swaybg_pid_file = TMP / "swaybg_pid"
swaybg_emoji_file = TMP / "swaybg_emoji"

# terminate early if background is already correct
if swaybg_emoji_file.is_file():
    with open(swaybg_emoji_file) as f:
        emoji = f.read()
        if emoji == hex_code:
            exit()
         

swaybg = Popen(["swaybg", "-i", emoji_path, "-m", "center", "-c", "#005063"])
sleep(0.1)
if swaybg_pid_file.is_file():
    with open(swaybg_pid_file) as f:
        pid = int(f.read())
        try:
            os.kill(pid, signal.SIGINT)
        except: 
            pass
open(swaybg_pid_file, "w").write(str(swaybg.pid))
open(swaybg_emoji_file, "w").write(str(hex_code))

