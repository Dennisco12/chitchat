import curses
from curses import wrapper
from cli.utilis.process import process_commands
from cli.globalvaribles import globalstate
from cli.utilis.helper_functions import homepage


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    height, width = stdscr.getmaxyx()

    stdscr = curses.initscr()
    curses.curs_set(2)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    GREY = curses.color_pair(236)
    PINK = curses.color_pair(200)

    message_height = height - 2
    message_win = curses.newwin(message_height, width, 0, 0)
    message_win.scrollok(True)
    homepage(message_win)

    input_win = curses.newwin(1, width, height - 1, 0)
    input_win.keypad(True)
    input_win.addstr("> ")
    input_win.addstr('Command...', GREY)
    input_win.move(input_win.getyx()[0], 2)
    input_win.refresh()
    input_str = ''
    while True:
        try:
            ch = input_win.getch()
        except:
            ch = None

        if ch == curses.KEY_ENTER or ch == 10:  # Enter key
            input_win.clear()
            input_win.addstr("> ")
            process_commands(input_str,
                             message_win, input_win)
            input_win.addstr(f'{globalstate.PLACEHOLDER}...', GREY)
            input_win.move(input_win.getyx()[0], 2)
            input_win.refresh()
            input_str = ''
        if ch < 256 and chr(ch).isprintable():  # check if printable ASCII character
            x = input_win.getyx()[1]
            input_list = list(input_str)
            input_list.insert(x-2, chr(ch))
            input_str = ''.join(input_list)
            input_win.clear()
            input_win.addstr(f'> {input_str}')
            input_win.move(input_win.getyx()[0], x+1)
            input_win.refresh()
        elif ch == curses.KEY_DC or ch == 127 or ch == curses.KEY_BACKSPACE:  # delete key
            x = input_win.getyx()[1]
            input_list = list(input_str)
            if len(input_list) == 0:
                pass
            elif x-3 < 0:
                pass
            elif x-3 > len(input_list)-1:
                pass
            else:
                del input_list[x-3]
                input_str = ''.join(input_list)
                input_win.clear()
                if len(input_list) == 0:
                    input_win.addstr("> ")
                    input_win.addstr('Command...', GREY)
                    input_win.move(input_win.getyx()[0], 2)
                    input_win.refresh()
                else:
                    input_win.addstr(f'> {input_str}')
                    input_win.move(input_win.getyx()[0], x-1)
                    input_win.refresh()
        elif ch == curses.KEY_LEFT:
            if input_win.getyx()[1] > 2:
                input_win.move(input_win.getyx()[0], input_win.getyx()[1] - 1)
        elif ch == curses.KEY_RIGHT:
            if input_win.getyx()[1] < input_win.getmaxyx()[1] - 1:
                input_win.move(input_win.getyx()[0], input_win.getyx()[1] + 1)
        if ch == curses.KEY_EXIT or ch == 3:  # CTRL+C
            break


if __name__ == '__main__':
    wrapper(main)
