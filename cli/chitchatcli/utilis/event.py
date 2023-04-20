#!/usr/bin/python3

import socketio
from chitchatcli.globalvaribles import globalstate
from chitchatcli.utilis.helper_functions import renderMessage
from datetime import datetime

"""
This module contains functions to connect and disconnect from the socket, 
as well as send messages.
"""

sio = socketio.Client()


@sio.event
def message(data):
    """
    This function is triggered when a message is received.
    It renders the message in the message window.
    """
    renderMessage(message_win=globalstate.message_win, message=data)


def connectToSocket():
    """
    This function connects to the socket.
    """
    sio.connect(globalstate.BASEURL, headers={'X-Token': globalstate.TOKEN})


def disconnectFromSocket():
    """
    This function disconnects from the socket.
    """
    sio.disconnect()


def sendMessage(message_win, message):
    """
    This function sends a message to the socket.
    """
    msgdata = {"createdAt": int(datetime.now().timestamp() * 1000),
               "senderusername": globalstate.USERNAME,
               "message": message
               }
    renderMessage(message_win, message=msgdata)
    sio.emit('message', {"message": message,
             "chatroomID": globalstate.chatroomID, "recepientID": globalstate.recepientID})
