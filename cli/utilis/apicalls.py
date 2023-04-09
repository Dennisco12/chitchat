import requests
from globalvaribles import globalstate
from utilis.helper_functions import showError, homepage, log, renderMessage
from utilis.storage import storage
from utilis.event import connectToSocket
import threading


def login(message_win):
    url = globalstate.BASEURL + '/login'
    res = requests.post(
        url, data=globalstate.HOLDER)
    if res.status_code != 201 and res.status_code != 202:
        showError("An error has occured with code: {} \n {}".format(
            res.status_code, res.text), message_win)

    elif res.status_code == 205:
        # opt
        pass
    else:
        token = res.json().get('token')
        username = res.json().get('user').get('username')
        storage.store('token', token)
        storage.store('username', username)
        globalstate.restore()
        globalstate.TOKEN = token
        homepage(message_win)


def confirmOTP():

    url = f'{globalstate.BASEURL}/users/confirmOTP'
    response = requests.post(url, data=globalstate.HOLDER)


def startChat(message_win,):
    log('\nLoading Chatroom...', message_win)
    url = globalstate.BASEURL + '/startChat/' + globalstate.HOLDER['username']
    res = requests.get(url, headers={'X-Token': globalstate.TOKEN})
    if res.status_code != 201 and res.status_code != 202:
        showError("An error has occured with code: {} \n {}".format(
            res.status_code, res.text), message_win)
    else:
        timer = threading.Timer(0.1, connectToSocket)
        timer.start()
        globalstate.chatroomID = res.json().get('chatroomID')
        globalstate.recepientID = res.json().get('recepientID')
        globalstate.messages = res.json().get('messages')
