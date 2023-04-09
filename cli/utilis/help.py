import curses


def runhelp(message_win,):
    message_win.clear()
    message_win.addstr('Welcome to the ')
    message_win.addstr('ChitChat ', curses.color_pair(200))
    message_win.addstr('Help Center!\n\n')
    message_win.addstr('To use ChitChat, follow these steps:\n')
    message_win.addstr('1. Launch the app from the command line\n')
    message_win.addstr(
        '2. Choose a login or create account to start chatting with others\n')
    message_win.addstr(
        '3. Get the username of someone you want to chat with\n')
    message_win.addstr(
        '4. Enter "StartChat" to enter a chatroom and start chatting\n')
    message_win.addstr(
        '5. Use the "Quit" option or "Ctrl C" to quit the app\n\n')
    message_win.addstr(
        'If you experience any issues or need further assistance, please contact our customer support team at chitchatcli@gmail.com.\n')
    message_win.addstr("\nMenu:\n", curses.color_pair(47))
    message_win.addstr(
        '1. Back')
    message_win.refresh()
