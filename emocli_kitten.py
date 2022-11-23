#! /bin/python3
import curses
from curses.textpad import Textbox, rectangle
from string import ascii_letters, digits;
import subprocess


N_SEARCH_RESULTS = 10

def emocli(stdscr):
    key = ''
    search = ''
    selected = 0
    while True:
        curses.use_default_colors()
        stdscr.clear()

        if key and chr(key) in ascii_letters + ': ':
            search += chr(key)
        #escape 
        elif key == 27:
            return
        elif key == curses.KEY_UP:
            selected = max(0, selected - 1) 
        elif key == curses.KEY_DOWN or key == ord('\t'): # tab
            selected = (selected + 1) % N_SEARCH_RESULTS
        elif key == curses.KEY_BACKSPACE:
            search = search[0:-1]

        prompt = f"🔎️> {search}"
        stdscr.addstr(2, 5, prompt)

        if search:
            lines = subprocess.Popen(["emocli", "search", search, '-n', str(N_SEARCH_RESULTS)], stdout=subprocess.PIPE).communicate()[0].decode().strip().split('\n')
            if (key and chr(key) in digits and 
                int(chr(key)) in range(N_SEARCH_RESULTS)):
                selected = int(chr(key))
                return lines[selected].split('\t')[0]
            if key and chr(key) == '\n':
                return lines[selected].split('\t')[0]
            for i, line in enumerate(lines):
                style = curses.A_REVERSE if i == selected else curses.A_NORMAL
                stdscr.addstr(4+i, 5, f"{i} ", curses.A_BOLD | style)
                stdscr.addstr(4+i, 7, line, style)

        stdscr.move(2, 5 + len(prompt))
        key = stdscr.getch()
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
