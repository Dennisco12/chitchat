import curses
from curses import wrapper
from utilis.process import process_commands
from globalvaribles import globalstate
from utilis.helper_functions import homepage


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    height, width = stdscr.getmaxyx()

    stdscr = curses.initscr()
    curses.curs_set(2)
    curses.start_color()
    curses.use_default_colors()
    try:
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
    except:
        pass
    GREY = curses.color_pair(236)

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
    overflow = 0
    globalstate.message_win = message_win
    globalstate.input_win = input_win
    try:
        while True:
            try:
                ch = input_win.getch()
            except:
                ch = None
            if ch == curses.KEY_EXIT or ch == 3:  # CTRL+C
                curses.endwin()
                del message_win
                del input_win
                break
            elif ch == curses.KEY_ENTER or ch == 10:  # Enter key
                input_win.clear()
                input_win.addstr("> ")
                process_commands(input_str,
                                 message_win, input_win)
                input_win.addstr(f'{globalstate.PLACEHOLDER}...', GREY)
                input_win.move(input_win.getyx()[0], 2)
                input_win.refresh()
                input_str = ''
            elif ch == -1:  # Terminal resized
                height, width = stdscr.getmaxyx()
                message_win.resize(height - 2, width)
                input_win.mvwin(height - 1, 1)
                input_win.resize(1, width - 2)
            # check if printable ASCII character
            elif ch and ch < 256 and chr(ch).isprintable():
                x = input_win.getyx()[1]
                input_list = list(input_str)
                input_list.insert(x-2, chr(ch))
                input_str = ''.join(input_list)
                input_win.clear()
                if len(input_str) < width-3:
                    overflow = 0
                    input_win.addstr(f'> {input_str}')
                    input_win.move(input_win.getyx()[0], x+1)
                    input_win.refresh()

                else:
                    overflow += 1
                    input_win.addstr(f'> {input_str[-1*(width-3):]}')
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
                        input_win.addstr(f'{globalstate.PLACEHOLDER}...', GREY)
                        input_win.move(input_win.getyx()[0], 2)
                        input_win.refresh()
                    elif len(input_str) >= width-3:
                        overflow += -1
                        input_win.addstr(f'> {input_str[-1*(width-3):]}')
                        input_win.refresh()

                    else:
                        overflow = 0
                        input_win.addstr(f'> {input_str}')
                        input_win.move(input_win.getyx()[0], x-1)
                        input_win.refresh()
            elif ch == curses.KEY_LEFT:
                if input_win.getyx()[1] > 2:
                    overflow += -1
                    if overflow <= 0:
                        overflow = 0
                    input_win.move(input_win.getyx()[
                                   0], input_win.getyx()[1] - 1)

            elif ch == curses.KEY_RIGHT:
                log('y', message_win)
                if input_win.getyx()[1] < input_win.getmaxyx()[1] - 1:
                    input_win.move(input_win.getyx()[
                                   0], input_win.getyx()[1] + 1)
            elif ch == curses.KEY_UP:
                message_win.scroll(1)
                message_win.refresh()
            elif ch == curses.KEY_DOWN:
                message_win.scroll(-1)
                message_win.refresh()
    except KeyboardInterrupt:
        curses.endwin()
        del message_win
        del input_win

    curses.endwin()
    del message_win
    del input_win


if __name__ == '__main__':
    wrapper(main)
