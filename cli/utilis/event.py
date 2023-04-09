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
    pass


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
