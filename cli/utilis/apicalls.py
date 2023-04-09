import requests
from globalvaribles import globalstate
from utilis.helper_functions import showError, homepage, log
from utilis.storage import storage


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
