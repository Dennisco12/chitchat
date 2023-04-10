from utilis.storage import storage


class GlobalState():

    BASEURL = 'https://7648-102-88-63-34.ngrok-free.app'
    STATUS = 'command'
    PLACEHOLDER = "Command"
    HOLDER = {}
    TOKEN = ''
    POS = 0
    USERNAME = ''
    isLoggedIn = False

    def __init__(self):
        token = storage.retrieve('token')
        if token:
            self.TOKEN = token
            self.USERNAME = storage.retrieve('username')
            self.isLoggedIn = True

    def restore(self):
        self.STATUS = 'command'
        self.PLACEHOLDER = "Command"
        self.HOLDER = {}
        self.POS = 0
        token = storage.retrieve('token')
        if token:
            self.TOKEN = token
            self.USERNAME = storage.retrieve('username')
            self.isLoggedIn = True


globalstate = GlobalState()
