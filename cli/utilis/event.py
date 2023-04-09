#!/usr/bin/python3

"""This module defines all the socket functions"""

import socketio
from globalvaribles import globalstate
from utilis.helper_functions import renderMessage, showError
from datetime import datetime
import curses

sio = socketio.Client()


@sio.event
def connect():
    globalstate.message_win.clear()
    globalstate.message_win.addstr("Chatting with: ", curses.color_pair(47))
    globalstate.message_win.addstr(f'{globalstate.HOLDER["username"]}\n\n',
                                   curses.color_pair(200))
    globalstate.restore()
    globalstate.PLACEHOLDER = 'Message'
    globalstate.STATUS = 'message'
    height = globalstate.message_win.getmaxyx()[0]
    for message in globalstate.messages[-1*(height-7):]:
        renderMessage(globalstate.message_win, message)


@sio.event
def disconnect():
    showError('Disconnected from server', message_win=globalstate.message_win)


@sio.event
def message(data):
    renderMessage(message_win=globalstate.message_win, message=data)


def connectToSocket():
    sio.connect(globalstate.BASEURL, headers={'X-Token': globalstate.TOKEN})


def sendMessage(message_win, message):
    msgdata = {"createdAt": int(datetime.now().timestamp() * 1000),
               "senderusername": globalstate.USERNAME,
               "message": message
               }
    renderMessage(message_win, message=msgdata)
    sio.emit('message', {"message": message,
             "chatroomID": globalstate.chatroomID, "recepientID": globalstate.recepientID})
