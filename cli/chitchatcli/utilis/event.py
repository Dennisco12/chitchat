#!/usr/bin/python3

"""This module defines all the socket functions"""

import socketio
from chitchatcli.globalvaribles import globalstate
from chitchatcli.utilis.helper_functions import renderMessage
from datetime import datetime

sio = socketio.Client()


@sio.event
def message(data):
    renderMessage(message_win=globalstate.message_win, message=data)


def connectToSocket():
    sio.connect(globalstate.BASEURL, headers={'X-Token': globalstate.TOKEN})


def disconnectFromSocket():
    sio.disconnect()


def sendMessage(message_win, message):
    msgdata = {"createdAt": int(datetime.now().timestamp() * 1000),
               "senderusername": globalstate.USERNAME,
               "message": message
               }
    renderMessage(message_win, message=msgdata)
    sio.emit('message', {"message": message,
             "chatroomID": globalstate.chatroomID, "recepientID": globalstate.recepientID})
