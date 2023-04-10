import curses
import threading
from globalvaribles import globalstate
from datetime import datetime


def homepage(message_win):
    message_win.clear()
    message_win.addstr("Welcome to ")
    message_win.addstr('ChitChat!\n\n', curses.color_pair(200))
    message_win.addstr(
        "To run a command, type the command name and hit Enter.\n")
    menu = []
    if globalstate.isLoggedIn:
        menu = ["StartChat", "Search", 'UpdateMe',
                'ViewProfile', 'ViewUser', "Help", "Quit"]
    else:
        menu = ["Signup", "Login", "ForgotPassword", "Help", "Quit"]

    message_win.addstr("\nMenu:\n", curses.color_pair(47))
    for i, item in enumerate(menu):
        message_win.addstr(f'{i+1}. {item}'+'\n', )
    globalstate.restore()

    if globalstate.isLoggedIn:
        message_win.addstr("\nLogged In User: ", curses.color_pair(47))
        message_win.addstr(f'{globalstate.USERNAME}\n\n',
                           curses.color_pair(200))

    else:
        message_win.addstr("\nNot Logged In!", curses.color_pair(10))

    message_win.refresh()


def showError(err, message_win):
    message_win.addstr("\n\nError: ", curses.color_pair(10))
    message_win.addstr(err)
    message_win.refresh()
    timer = threading.Timer(4, homepage, args=[message_win])
    timer.start()


def log(text, message_win):
    message_win.addstr(f"\n{text}", curses.color_pair(22))
    message_win.refresh()


def timestampToDate(timestamp):
    timestamp_sec = int(timestamp) / 1000
    dt = datetime.fromtimestamp(timestamp_sec)
    return dt.strftime("%-I:%M%p")


def renderMessage(message_win, message):
    COLOR = ''
    time = timestampToDate(message['createdAt'])
    msg = message['message']
    senderusername = message['senderusername']
    if (senderusername == globalstate.USERNAME):
        COLOR = curses.color_pair(22)
    else:
        COLOR = curses.color_pair(200)
    message_win.addstr(f"[{time} {senderusername}]: ", COLOR)
    message_win.addstr(msg+'\n')
    message_win.refresh()
