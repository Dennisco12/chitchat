import requests
from globalvaribles import globalstate
from utilis.helper_functions import showError, homepage, log, renderMessage
from utilis.storage import storage
import curses
from utilis.event import connectToSocket


def login(message_win):
    url = globalstate.BASEURL + '/login'
    log(globalstate.HOLDER, message_win)
    log(url, message_win)

    # try:
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

    # except:
    #     showError("An error has occured!", message_win)


def confirmOTP():

    url = f'{globalstate.BASEURL}/users/confirmOTP'
    response = requests.post(url, data=globalstate.HOLDER)


def startChat(message_win):
    url = globalstate.BASEURL + '/startChat/' + globalstate.HOLDER['username']
    res = requests.get(url, headers={'X-Token': globalstate.TOKEN})
    if res.status_code != 201 and res.status_code != 202:
        showError("An error has occured with code: {} \n {}".format(
            res.status_code, res.text), message_win)
    else:
        connectToSocket()
        globalstate.chatroomID = res.json().get('chatroomID')
        globalstate.recepientID = res.json().get('recepientID')
        globalstate.messages = res.json().get('messages')
        message_win.clear()
        message_win.addstr("Chatting with: ", curses.color_pair(47))
        message_win.addstr(f'{globalstate.HOLDER["username"]}\n\n',
                           curses.color_pair(200))
        globalstate.restore()
        globalstate.PLACEHOLDER = 'Message'
        globalstate.STATUS = 'message'
        height = message_win.getmaxyx()[0]
        for message in globalstate.messages[-1*(height-7):]:
            renderMessage(message_win, message)
        message_win.refresh()
