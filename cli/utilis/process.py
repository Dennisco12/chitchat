from utilis import help, screen_functions
from globalvaribles import globalstate
from utilis.helper_functions import homepage, showError
import curses
from utilis.event import sendMessage


def process_commands(text, message_win, input_win):
    if text.lower().strip() == 'help':
        help.runhelp(message_win)
    elif text.lower().strip() == 'quit':
        globalstate.RUNNING = False
        return
    elif text == 'back':
        homepage(message_win)
    elif len(text) <= 0:
        return
    if globalstate.STATUS == 'command':
        text = text.lower().strip()

        if globalstate.isLoggedIn:
            if text == 'startchat':
                screen_functions.startchat(message_win, text, input_win)
            elif text == 'updateme':
                screen_functions.updateme(message_win, text)
            else:
                showError(f'Command {text} not found!', message_win)
        else:
            if text == 'signup':
                pass
            elif text == 'login':
                screen_functions.login(message_win)
            else:
                showError(f'Command {text} not found!', message_win)
    elif globalstate.STATUS == 'login':
        screen_functions.login(message_win, text)
    elif globalstate.STATUS == 'startchat':
        screen_functions.startchat(message_win, text, input_win)
    elif globalstate.STATUS == 'message':
        sendMessage(message_win, text)
    elif globalstate.STATUS == 'updateme':
        screen_functions.updateme(message_win, text)
    elif globalstate.STATUS == 'loading':
        pass
    else:
        pass
