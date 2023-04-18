import requests
from chitchatcli.globalvaribles import globalstate
from chitchatcli.utilis.helper_functions import showError, homepage, log, renderSearchUser
from chitchatcli.utilis.storage import storage
from chitchatcli.globalvaribles import globalstate
from chitchatcli.utilis.helper_functions import showError, homepage, log, renderMessage
from chitchatcli.utilis.storage import storage
from chitchatcli.utilis.event import connectToSocket
import curses
import time
from chitchatcli.utilis import screen_functions


def signup(message_win):
    url = globalstate.BASEURL + '/signup'
    res = requests.post(
        url, data=globalstate.HOLDER)
    if res.status_code != 201 and res.status_code != 202:
        showError("An error has occured with code: {} \n {}".format(
            res.status_code, res.text), message_win)
    else:
        screen_functions.confirmOtp(message_win)


def login(message_win):
    url = globalstate.BASEURL + '/login'
    res = requests.post(
        url, data=globalstate.HOLDER)
    if res.status_code != 201 and res.status_code != 202:
        showError("An error has occured with code: {} \n {}".format(
            res.status_code, res.text), message_win)

    elif res.status_code == 202:
        globalstate.USERNAME = globalstate.HOLDER['identifier']
        screen_functions.confirmOtp(message_win, text='')
    else:
        token = res.json().get('token')
        username = res.json().get('user').get('username')
        storage.store('token', token)
        storage.store('username', username)
        globalstate.restore()
        globalstate.TOKEN = token
        homepage(message_win)


def confirmOTP(message_win):
    url = f'{globalstate.BASEURL}/users/confirmOTP'
    res = requests.post(
        url, data={"identifier": globalstate.USERNAME, "otp": globalstate.HOLDER['otp']})

    if res.status_code != 201 and res.status_code != 202:
        showError("An error has occured with code: {} \n {}".format(
            res.status_code, res.text), message_win)
    else:
        token = res.json().get('token')
        username = res.json().get('user').get('username')
        storage.store('token', token)
        storage.store('username', username)
        globalstate.restore()
        globalstate.TOKEN = token
        message_win.clear()
        log('Welcome to ChitChat\n', message_win)
        log('To make your account publicly searchable, update your profile.\n', message_win)
        time.sleep(6)
        homepage(message_win)


def startChat(message_win, input_win):
    log('\nLoading Chatroom...', message_win)
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
        globalstate.message_win.clear()
        globalstate.message_win.addstr(
            "Chatting with: ", curses.color_pair(47))
        globalstate.message_win.addstr(f'{globalstate.HOLDER["username"]}\n\n',
                                       curses.color_pair(200))
        message_win.refresh()
        globalstate.restore()
        globalstate.PLACEHOLDER = 'Message'
        globalstate.STATUS = 'message'
        input_win.clear()
        input_win.addstr("> ")
        input_win.addstr(
            f'{globalstate.PLACEHOLDER}...', curses.color_pair(236))
        input_win.move(input_win.getyx()[0], 2)
        input_win.refresh()
        height = message_win.getmaxyx()[0]
        # [-1*(height-7):]
        for message in globalstate.messages:
            renderMessage(globalstate.message_win, message)


def updateprofile(message_win):
    url = globalstate.BASEURL + '/users/editProfile'

    res = requests.put(url, data=globalstate.HOLDER, headers={
                       "X-Token": globalstate.TOKEN})
    if res.status_code != 201:
        showError("An error has occured with code: {}. \nError message: {}".format(
            res.status_code, res.text), message_win)
    else:
        log("Your details have been updated successfully", message_win)
        time.sleep(4)
        globalstate.restore()
        homepage(message_win)


def getProfile(message_win):
    url = globalstate.BASEURL + '/users/me'

    res = requests.get(url, headers={
                       "X-Token": globalstate.TOKEN})
    if res.status_code != 201:
        showError("An error has occured with code: {}. \nError message: {}".format(
            res.status_code, res.text), message_win)
    else:
        user = res.json().get('user')
        globalstate.EMAIL = user['email']
        globalstate.profileDetails = user.get('profileDetails')


def getUser(message_win, username):
    url = globalstate.BASEURL + f'/users/{username}'

    res = requests.get(url, headers={
                       "X-Token": globalstate.TOKEN})
    if res.status_code != 201:
        showError("An error has occured with code: {}. \nError message: {}".format(
            res.status_code, res.text), message_win)
    else:
        user = res.json().get('user')
        globalstate.USERUSERNAME = user['username']
        globalstate.USEREMAIL = user['email']
        globalstate.USERprofileDetails = user.get('profileDetails')


def search(message_win, term):
    url = globalstate.BASEURL + '/users/search'

    res = requests.post(url, data={"term": term}, headers={
        "X-Token": globalstate.TOKEN})
    if res.status_code != 201:
        showError("An error has occured with code: {}. \nError message: {}".format(
            res.status_code, res.text), message_win)
    else:
        re = res.json()
        message_win.clear()
        message_win.addstr('Search Results for ', curses.color_pair(200))
        message_win.addstr(f'[{term}]\n\n', curses.color_pair(57))
        if len(re) > 0:
            for user in re:
                renderSearchUser(message_win, user)
        else:
            log('\nNo user found for that search term!\n\n', message_win)


def logout(message_win):
    storage.delete('token')
    storage.delete('username')
    globalstate.restore()
    globalstate.TOKEN = None
    globalstate.isLoggedIn = False
    globalstate.USERNAME = None
    homepage(message_win)

    url = globalstate.BASEURL + '/logout'

    requests.post(url, headers={
        "X-Token": globalstate.TOKEN})


def sendpasswordreset(message_win):
    url = globalstate.BASEURL + '/resetPassword'

    res = requests.post(url, data={
        "identifier": globalstate.HOLDER['identifier']})
    if res.status_code != 201:
        showError("An error has occured with code: {}. \nError message: {}".format(
            res.status_code, res.text), message_win)
    else:
        message_win.clear()
        globalstate.PLACEHOLDER = 'Otp'
        message_win.addstr('Reset Password\n\n', curses.color_pair(200))
        message_win.addstr('Enter otp sent to your email: ', )
        message_win.refresh()


def passwordreset(message_win):
    url = globalstate.BASEURL + '/resetPassword'

    res = requests.put(url, data={
        "identifier": globalstate.HOLDER['identifier'], "otp": globalstate.HOLDER['otp'], "password": globalstate.HOLDER['password']})
    if res.status_code != 201:
        showError("An error has occured with code: {}. \nError message: {}".format(
            res.status_code, res.text), message_win)
    else:
        log('\n\nPassword reset successfully!\nPlease login.\n', message_win)
        message_win.refresh()
        time.sleep(6)
        homepage(message_win)
