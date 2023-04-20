#!/usr/bin/python3

"""This module contains functions for the ChitChat CLI application.

It includes functions for rendering the homepage, showing errors, logging, 
rendering messages, and rendering search users.
"""
import curses
import threading
from chitchatcli.globalvaribles import globalstate
from datetime import datetime


def homepage(message_win):
    """Render the homepage of the ChitChat CLI application.

    Args:
        message_win (curses window object): The curses window object to render the homepage in.
    """
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
    """Replace a line in the curses window with blank spaces.

    Args:
        message_win (curses window object): The curses window object to replace the line in.
        y (int): The y coordinate of the line to be replaced.
    """
    width = message_win.getmaxyx()[1]
    message_win.addstr(y, 0, ' ' * (width-2))


def starterase(fy, ly, message_win):
    """Erase a range of lines in the curses window.

    Args:
        fy (int): The y coordinate of the first line to be erased.
        ly (int): The y coordinate of the last line to be erased.
        message_win (curses window object): The curses window object to erase the lines in.
    """
    n = ly - fy
    for i in range(n+2):
        replace(message_win, y=ly - i)
    message_win.scroll(-1)
    message_win.refresh()


def showError(err, message_win):
    """Show an error message in the curses window.

    Args:
        err (str): The error message to be displayed.
        message_win (curses window object): The curses window object to display the error in.
    """
    fy = message_win.getyx()[0]

    message_win.addstr("\n\nError: ", curses.color_pair(10))
    message_win.addstr(err)
    message_win.refresh()

    ly = message_win.getyx()[0]

    timer = threading.Timer(8, homepage, args=[
        message_win])
    timer.start()


def log(text, message_win):
    """Log a message in the curses window.

    Args:
        text (str): The message to be logged.
        message_win (curses window object): The curses window object to log the message in.
    """
    message_win.addstr(f"\n{text}", curses.color_pair(22))
    message_win.refresh()


def timestampToDate(timestamp):
    """Convert a timestamp to a date string.

    Args:
        timestamp (int): The timestamp to be converted.

    Returns:
        str: The date string in the format HH:MM.
    """
    timestamp_sec = int(timestamp) / 1000
    dt = datetime.fromtimestamp(timestamp_sec)
    return f'{str(dt.hour).zfill(2)}:{str(dt.minute).zfill(2)}'


def renderMessage(message_win, message):
    """Render a message in the curses window.

    Args:
        message_win (curses window object): The curses window object to render the message in.
        message (dict): The message to be rendered.
    """
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
    """Render a searched user in the curses window.

    Args:
        message_win (curses window object): The curses window object to render the message in.
        user: The user details to be rendered
    """
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
