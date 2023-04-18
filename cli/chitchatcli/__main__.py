import curses
from curses import wrapper
from chitchatcli.utilis.process import process_commands
from chitchatcli.globalvaribles import globalstate
from chitchatcli.utilis.helper_functions import homepage, log, showError


def main(stdscr):
    stdscr = curses.initscr()
    stdscr.clear()
    height, width = stdscr.getmaxyx()
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
    globalstate.message_win = message_win
    globalstate.input_win = input_win
    scroll_upnum = -1
    screen_uptext = []
    upatrr = {}
    downatrr = {}

    scroll_downnum = -1
    screen_downtext = []
    try:
        while globalstate.RUNNING:
            ch = input_win.getch()
            if ch == curses.KEY_EXIT or ch == 3:  # CTRL+C
                del message_win
                del input_win
                curses.endwin()
                break
            elif ch == curses.KEY_ENTER or ch == 10:  # Enter key
                input_win.clear()
                input_win.addstr("> ")
                process_commands(input_str,
                                 message_win, input_win)
                input_win.clear()
                input_win.addstr("> ")
                input_win.addstr(f'{globalstate.PLACEHOLDER}...', GREY)
                input_win.move(input_win.getyx()[0], 2)
                input_win.refresh()
                input_str = ''
            elif ch == -1:  # Terminal resized
                height, width = stdscr.getmaxyx()
                message_win.mvwin(0, 0)
                message_win.resize(height - 2, width)
                input_win.mvwin(height - 1, 0)
                input_win.resize(1, width)
                input_win.refresh()
                message_win.refresh()

            # check if printable ASCII character
            elif ch and ch < 256 and chr(ch).isprintable():
                x = input_win.getyx()[1]
                input_list = list(input_str)
                input_list.insert(x-2, chr(ch))
                input_str = ''.join(input_list)
                input_win.clear()
                if len(input_str) < width-3:
                    input_win.addstr(f'> {input_str}')
                    input_win.move(input_win.getyx()[0], x+1)
                    input_win.refresh()

                else:
                    input_win.addstr(f'> {input_str[-1*(width-3):]}')
                    input_win.refresh()

            elif ch == curses.KEY_DC or ch == 127 or ch == 8 or ch == curses.KEY_BACKSPACE:  # delete key
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
                        input_win.addstr(f'> {input_str[-1*(width-3):]}')
                        input_win.refresh()

                    else:
                        input_win.addstr(f'> {input_str}')
                        input_win.move(input_win.getyx()[0], x-1)
                        input_win.refresh()
            elif ch == curses.KEY_LEFT:
                if input_win.getyx()[1] > 2:
                    input_win.move(input_win.getyx()[
                        0], input_win.getyx()[1] - 1)

            elif ch == curses.KEY_RIGHT:
                if input_win.getyx()[1] < input_win.getmaxyx()[1] - 1:
                    input_win.move(input_win.getyx()[
                        0], input_win.getyx()[1] + 1)
            elif ch == curses.KEY_UP:
                x = message_win.getyx()[1]
                my, mx = message_win.getmaxyx()
                line1_text = message_win.instr(0, 0, mx).decode()
                screen_uptext.append(line1_text.strip())
                scroll_upnum += 1
                atr = []

                for i in range(len(line1_text.strip())):
                    style = message_win.inch(0, i) & curses.A_ATTRIBUTES
                    atr.append(style)

                upatrr[scroll_upnum] = atr

                message_win.scroll(1)
                if scroll_downnum > -1:
                    # log(f'up {screen_downtext[scroll_downnum]}', message_win)
                    for i in range(len(screen_downtext[scroll_downnum])):
                        message_win.addstr(
                            my-1, i, screen_downtext[scroll_downnum][i], downatrr[scroll_downnum][i]
                        )

                    del screen_downtext[scroll_downnum]
                    scroll_downnum -= 1
                message_win.refresh()

            elif ch == curses.KEY_DOWN:
                x = message_win.getyx()[1]
                my, mx = message_win.getmaxyx()
                last_text = message_win.instr(my-1, 0, mx).decode()
                screen_downtext.append(last_text.strip())
                scroll_downnum += 1
                atr = []

                for i in range(len(last_text.strip())):
                    style = message_win.inch(my-1, i) & curses.A_ATTRIBUTES
                    atr.append(style)

                downatrr[scroll_downnum] = atr

                message_win.scroll(-1)

                if scroll_upnum > -1:
                    for i in range(len(screen_uptext[scroll_upnum])):
                        message_win.addstr(
                            0, i, screen_uptext[scroll_upnum][i], upatrr[scroll_upnum][i])

                    del screen_uptext[scroll_upnum]
                    scroll_upnum -= 1
                message_win.refresh()

    except:
        pass
    curses.endwin()


if __name__ == '__main__':
    wrapper(main)
