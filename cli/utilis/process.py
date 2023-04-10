from utilis import help, auth_functions
from globalvaribles import globalstate
from utilis.helper_functions import homepage, showError


def process_commands(text, message_win, input_win):

    if globalstate.STATUS == 'command':
        text = text.lower().strip()
        if text == 'help':
            help.runhelp(message_win)
        elif text == 'quit':
            curses.endwin()
            del message_win
            del input_win
        elif text == 'back':
            homepage(message_win)
        elif globalstate.isLoggedIn:
            if text == 'startchat':
                auth_functions.startchat(message_win, text, input_win)
            else:
                showError(f'Command {text} not found!', message_win)
        else:
            if text == 'signup':
                pass
            elif text == 'login':
                auth_functions.login(message_win)
            else:
                showError(f'Command {text} not found!', message_win)

    elif globalstate.STATUS == 'login':
        auth_functions.login(message_win, text)
    elif globalstate.STATUS == 'startchat':
        auth_functions.startchat(message_win, text, input_win)
    elif globalstate.STATUS == 'message':
        sendMessage(message_win, text)
    elif globalstate.STATUS == 'loading':
        pass
    else:
        pass
