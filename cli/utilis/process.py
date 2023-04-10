from cli.utilis import help, auth_functions
from cli.globalvaribles import globalstate
from cli.utilis.helper_functions import homepage, showError


def process_commands(text, message_win, input_win):

    if globalstate.STATUS == 'command':
        text = text.lower().strip()

        if text == 'startchat':
            pass
        elif text == 'signup':
            pass
        elif text == 'login':
            auth_functions.login(message_win, input_win)
        elif text == 'help' or text == '4':
            help.runhelp(message_win)
        elif text == 'quit' or text == '5':
            pass
        elif text == 'back':
            homepage(message_win)
        else:
            showError(f'Command {text} not found!', message_win)
    elif globalstate.STATUS == 'login':
        auth_functions.login(message_win, input_win, text)
    else:
        pass
