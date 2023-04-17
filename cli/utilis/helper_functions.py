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
        menu = ["StartChat", "Search", 'UpdateProfile',
                'ViewProfile', 'ViewUser', "Help", "Quit", "Logout"]
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


def replace(message_win, y):
    width = message_win.getmaxyx()[1]
    message_win.addstr(y, 0, ' ' * (width-2))


def starterase(fy, ly, message_win):
    n = ly - fy
    for i in range(n+2):
        replace(message_win, y=ly - i)
    message_win.scroll(-1)
    message_win.refresh()


def showError(err, message_win):

    fy = message_win.getyx()[0]

    message_win.addstr("\n\nError: ", curses.color_pair(10))
    message_win.addstr(err)
    message_win.refresh()

    ly = message_win.getyx()[0]

    timer = threading.Timer(8, homepage, args=[
        message_win])
    timer.start()


def log(text, message_win):
    message_win.addstr(f"\n{text}", curses.color_pair(22))
    message_win.refresh()


def timestampToDate(timestamp):
    timestamp_sec = int(timestamp) / 1000
    dt = datetime.fromtimestamp(timestamp_sec)
    return f'{str(dt.hour).zfill(2)}:{str(dt.minute).zfill(2)}'


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


def renderSearchUser(message_win, user={}):
    user1 = {'_id': '642ff43b427574d2800c9906', 'email': 'akinwonjowodennisco@gmail.com', 'username': 'dennisco',
             'profileDetails': {'firstName': 'Dennis', 'lastName': 'Akinwonjowodenn',
                                'bio': 'I am a Python developer, I use the flask framwork. Im also learning Javascript', 'level': 'Intermediate', 'techStack': 'Python, JavaScript, C'}}
    profileDetails = user.get('profileDetails')
    message_win.addstr(
        f'{profileDetails.get("firstName")} {profileDetails.get("lastName")}', curses.color_pair(85))
    message_win.addstr(
        f'\n{profileDetails.get("bio")}\n', curses.color_pair(200))
    message_win.addstr(
        f'{user.get("username")}  {user.get("email")}\n', curses.color_pair(46))

    message_win.addstr(
        f'{profileDetails.get("level")}', curses.color_pair(184))
    message_win.addstr(
        f'\n{profileDetails.get("techStack")}\n\n', curses.color_pair(200))
    message_win.refresh()
