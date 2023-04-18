from chitchatcli.utilis import screen_functions
from chitchatcli.globalvaribles import globalstate
from chitchatcli.utilis.helper_functions import homepage, showError
from chitchatcli.utilis.event import sendMessage
from chitchatcli.utilis.apicalls import logout


def process_commands(text, message_win, input_win):
    if text.lower().strip() == 'help':
        screen_functions.runhelp(message_win)
    elif text.lower().strip() == 'quit':
        globalstate.RUNNING = False
        return
    elif text == 'back':
        homepage(message_win)
    elif len(text) <= 0:
        return
    elif globalstate.STATUS == 'confirmotp':
        screen_functions.confirmOtp(message_win, text)
    elif globalstate.STATUS == 'command':
        text = text.lower().strip()

        if globalstate.isLoggedIn:
            if text == 'startchat':
                screen_functions.startchat(message_win, text, input_win)
            elif text == 'updateprofile':
                screen_functions.updateprofile(message_win, text)
            elif text == 'viewprofile':
                screen_functions.viewprofile(message_win, input_win)
            elif text == 'viewuser':
                screen_functions.viewuser(message_win, input_win)
            elif text == 'search':
                screen_functions.search(message_win, text, input_win)
            elif text == 'logout':
                logout(message_win)
            else:
                showError(f'Command {text} not found!', message_win)
        else:
            if text == 'signup':
                screen_functions.signup(message_win)
            elif text == 'login':
                screen_functions.login(message_win)
            elif text == 'forgotpassword':
                screen_functions.forgotpassword(message_win, text)
            else:
                showError(f'Command {text} not found!', message_win)
    elif globalstate.STATUS == 'login':
        screen_functions.login(message_win, text)
    elif globalstate.STATUS == 'signup':
        screen_functions.signup(message_win, text)
    elif globalstate.STATUS == 'startchat':
        screen_functions.startchat(message_win, text, input_win)
    elif globalstate.STATUS == 'message':
        sendMessage(message_win, text)
    elif globalstate.STATUS == 'updateprofile':
        screen_functions.updateprofile(message_win, text)
    elif globalstate.STATUS == 'viewuser':
        screen_functions.viewuser(
            message_win, input_win, text=text.lower().strip())
    elif globalstate.STATUS == 'search':
        screen_functions.search(message_win, text, input_win)
    elif globalstate.STATUS == 'forgotpassword':
        screen_functions.forgotpassword(message_win, text)
    elif globalstate.STATUS == 'loading':
        pass
    else:
        pass
