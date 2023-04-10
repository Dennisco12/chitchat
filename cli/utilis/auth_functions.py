from cli.globalvaribles import globalstate
import curses
from cli.utilis import apicalls
# def signup():
#     """This creates a user in the database
#     return the user id and token"""
#     email = input(Fore.BLUE + "Please enter your email: ")
#     while len(email) == 0:
#         print(Fore.RED + "* Email field cannot be empty, please try again *")
#         email = input(Fore.BLUE + "Please enter your email: ")
#     username = input(Fore.BLUE + "Please enter your username: ")
#     password = input(Fore.BLUE + "Please enter your password: ")
#     url = f'{self.baseurl}/signup'
#     data = {"email": email, "username": username, "password": password}
#     response = requests.post(url, data=data)
#     if response.status_code != 201:
#         print(Fore.RED + "An error has occurred with code:",
#                 response.status_code, "\n", response.text)
#     else:
#         print(Fore.GREEN+'Your account has been created succesfully')
#         otp = input(Fore.BLUE + 'Enter the OTP sent to your email: ')
#         url = self.baseurl + '/users/confirmOTP'
#         res = requests.post(url, data={"otp": otp, "identifier": email})
#         if res.status_code == 201:
#             print(Fore.GREEN + "...Verification succesful...")
#             token = res.text
#         else:
#             otp = input(
#                 Fore.RED + "Verification failed, you have one attempt left: ")
#             res = requests.post(
#                 url, data={"otp": otp, "identifier": email})
#             if res.status_code == 201:
#                 print(Fore.GREEN + "...Verification succesful...")
#                 token = user.get('token')
#                 self.prompt = "({}) ".format(username)
#             else:
#                 print(Fore.RED + "...Verification failed...")
#     return False


def login(message_win, input_win, text=''):
    """This takes in username or email and password and 
    creates a session for the user"""
    if globalstate.STATUS == 'login':
        if globalstate.POS == 0:
            globalstate.HOLDER['identifier'] = text.lower().strip()
            globalstate.POS = 1
            globalstate.PLACEHOLDER = 'Password'
            message_win.addstr(f'{text}\n', curses.color_pair(85))
            message_win.addstr('Enter your password: ', )
            message_win.refresh()
        elif globalstate.POS == 1:
            globalstate.HOLDER['password'] = text
            globalstate.POS = 1
            globalstate.PLACEHOLDER = 'Loading'
            message_win.addstr('*'*len(text)+'\n', curses.color_pair(85))
            message_win.addstr('\n\nLogging you in...', curses.color_pair(200))
            message_win.refresh()
            apicalls.login(message_win)

    else:
        globalstate.STATUS = 'login'
        globalstate.PLACEHOLDER = 'Email or Username'
        globalstate.POS = 0
        globalstate.HOLDER = {}
        message_win.clear()
        message_win.addstr('Login\n\n', curses.color_pair(200))
        message_win.addstr('Enter your username or email: ', )
        message_win.refresh()
        url = globalstate.BASEURL + '/login'
