"""Module for GlobalState class"""

from chitchatcli.utilis.storage import storage


class GlobalState():
    """Class to store global state of the application"""

    BASEURL = 'https://chitchat-25ug.onrender.com'
    STATUS = 'command'
    PLACEHOLDER = "Command"
    HOLDER = {}
    TOKEN = ''
    POS = 0
    USERNAME = ''
    isLoggedIn = False
    RUNNING = True

    def __init__(self):
        """Initialize the global state"""
        token = storage.retrieve('token')
        if token:
            self.TOKEN = token
            self.USERNAME = storage.retrieve('username')
            self.isLoggedIn = True

    def restore(self):
        """Restore the global state"""
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
