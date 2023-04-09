#!/usr/bin/python3

"""This module defines all the socket functions"""

import socketio

socket_url = 'http://localhost:3000'

sio = socketio.Client()


@sio.event
def connect():
    print('Connected to server')


@sio.event
def message(data):
    print('Received message:', data)


def connectToSocket(token):
    sio.connect(socket_url, headers={'X-Token': token})
    # sio.wait()


def sendMessage(message, chatroomID, recepientID):
    sio.emit('message', {"message": message,
             "chatroomID": chatroomID, "recepientID": recepientID})
