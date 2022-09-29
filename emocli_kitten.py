#! /bin/python3
import curses
from curses.textpad import Textbox, rectangle
from string import ascii_letters;
import subprocess

def emocli(stdscr):
    key = ''
    search = ''
    selected = 0
    while True:
        stdscr.clear()
        if key in ascii_letters:
            search += key
        elif key == 'KEY_UP':
            selected = max(0, selected - 1) 
        elif key == 'KEY_DOWN':
            selected = min(4, selected + 1) 
        elif key == 'KEY_BACKSPACE':
            search = search[0:-1]
        prompt = f"🔎️> {search}"
        stdscr.addstr(2, 5, prompt)

        if search:
            lines = subprocess.Popen(["emocli", "search", search], stdout=subprocess.PIPE).communicate()[0].decode().split('\n')
            if key == '\n':
                return lines[selected][0]
            for i, line in enumerate(lines):
                if i == selected:
                    stdscr.addstr(3+i, 5, line, curses.A_REVERSE)
                else:
                    stdscr.addstr(3+i, 5, line)

        stdscr.move(2, 5 + len(prompt))
        key = stdscr.getkey()
        stdscr.refresh()



def main(args):
    return curses.wrapper(emocli)

def handle_result(args, answer, target_window_id, boss):
    # get the kitty window into which to paste answer
    w = boss.window_id_map.get(target_window_id)
    if w is not None:
        w.paste(answer)

if __name__ == '__main__':
    main([])
