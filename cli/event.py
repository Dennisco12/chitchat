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


def connectToSocket():
    sio.connect(socket_url)


def sendMessage():
    sio.emit('my_event', {'data': 'my_data'})
