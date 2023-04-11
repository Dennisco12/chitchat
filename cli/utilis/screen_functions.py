from globalvaribles import globalstate
import curses
from utilis import apicalls
from utilis.helper_functions import showError, log
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


def signup(message_win, text=''):
    if globalstate.STATUS == 'signup':
        if globalstate.POS == 0:
            globalstate.HOLDER['email'] = text.lower().strip()
            globalstate.POS = 1
            globalstate.PLACEHOLDER = 'Password'
            message_win.addstr(f'{text}\n', curses.color_pair(85))
            message_win.addstr('Enter your password: ', )
            message_win.refresh()
        elif globalstate.POS == 1:
            globalstate.HOLDER['password'] = text
            globalstate.POS = 2
            globalstate.PLACEHOLDER = 'Username'
            message_win.addstr('*'*len(text)+'\n', curses.color_pair(85))
            message_win.addstr('Enter a unique username: ')
            message_win.refresh()
        elif globalstate.POS == 2:
            globalstate.HOLDER['username'] = text.lower().strip()
            globalstate.USERNAME = text.lower().strip()
            globalstate.POS = 3
            globalstate.PLACEHOLDER = 'Loading'
            globalstate.STATUS = 'loading'
            message_win.addstr('*'*len(text)+'\n', curses.color_pair(85))
            message_win.addstr('\n\nCreating your account...',
                               curses.color_pair(200))
            message_win.refresh()
            try:
                apicalls.signup(message_win)
            except:
                showError("An unknown error has occured!", message_win)

    else:
        globalstate.STATUS = 'signup'
        globalstate.PLACEHOLDER = 'Email'
        globalstate.POS = 0
        globalstate.HOLDER = {}
        message_win.clear()
        message_win.addstr('Create Account\n\n', curses.color_pair(200))
        message_win.addstr('Enter your email: ', )
        message_win.refresh()


def login(message_win, text=''):
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
            globalstate.STATUS = 'loading'
            message_win.addstr('*'*len(text)+'\n', curses.color_pair(85))
            message_win.addstr('\n\nLogging you in...', curses.color_pair(200))
            message_win.refresh()
            # try:
            apicalls.login(message_win)
            # except:
            #     showError("An unknown error has occured!", message_win)

    else:
        globalstate.STATUS = 'login'
        globalstate.PLACEHOLDER = 'Email or Username'
        globalstate.POS = 0
        globalstate.HOLDER = {}
        message_win.clear()
        message_win.addstr('Login\n\n', curses.color_pair(200))
        message_win.addstr('Enter your username or email: ', )
        message_win.refresh()


def confirmOtp(message_win, text=''):

    if globalstate.STATUS == 'confirmotp':
        globalstate.HOLDER['otp'] = text
        globalstate.PLACEHOLDER = 'Loading'
        globalstate.STATUS = 'loading'
        message_win.addstr(f'{text}\n', curses.color_pair(85))
        message_win.addstr('\n\nConfirming Otp...', curses.color_pair(200))
        message_win.refresh()
        try:
            apicalls.confirmOTP(message_win)
        except:
            showError("An unknown error has occured!", message_win)

    else:
        globalstate.STATUS = 'confirmotp'
        globalstate.PLACEHOLDER = 'Otp'
        globalstate.POS = 0
        globalstate.HOLDER = {}
        message_win.clear()
        message_win.addstr('Verify Email\n\n', curses.color_pair(200))
        message_win.addstr('Enter the code sent to your email: ', )
        message_win.refresh()


def startchat(message_win, text='', input_win=None):
    if globalstate.STATUS == 'startchat':
        globalstate.HOLDER['username'] = text.lower().strip()
        message_win.addstr(f' {text}\n', curses.color_pair(85))
        globalstate.PLACEHOLDER = 'Loading'
        globalstate.STATUS = 'loading'
        input_win.clear()
        input_win.addstr("> ")
        input_win.addstr(f'{globalstate.PLACEHOLDER}...',
                         curses.color_pair(236))
        input_win.move(input_win.getyx()[0], 2)
        input_win.refresh()
        try:
            apicalls.startChat(message_win, input_win)
        except:
            showError("An unknown error has occured!", message_win)
    else:
        globalstate.STATUS = 'startchat'
        globalstate.PLACEHOLDER = 'Username'
        globalstate.POS = 0
        globalstate.HOLDER = {}
        message_win.clear()
        message_win.addstr('Start Chat\n\n', curses.color_pair(200))
        message_win.addstr(
            'Please enter the username of the person you would like to chat with:', )
        message_win.refresh()


def updateprofile(message_win, text=''):
    if globalstate.STATUS == 'updateprofile':
        if globalstate.POS == 0:
            globalstate.HOLDER['firstName'] = text.strip()
            message_win.addstr(f' {text}\n', curses.color_pair(85))
            globalstate.PLACEHOLDER = 'LastName'
            globalstate.POS = 1
            message_win.addstr('Enter your Last Name: ', )
            message_win.refresh()
        elif globalstate.POS == 1:
            globalstate.HOLDER['lastName'] = text.strip()
            message_win.addstr(f' {text}\n', curses.color_pair(85))
            globalstate.PLACEHOLDER = 'Bio'
            globalstate.POS = 2
            message_win.addstr('Enter your Bio: ', )
            message_win.refresh()
        elif globalstate.POS == 2:
            globalstate.HOLDER['bio'] = text.strip()
            message_win.addstr(f' {text}\n', curses.color_pair(85))
            globalstate.PLACEHOLDER = 'Level'
            globalstate.POS = 3
            message_win.addstr(
                'Enter your Level ')
            message_win.addstr('(Junior, Intermidiate or Senior): ',
                               curses.color_pair(236))
            message_win.refresh()
        elif globalstate.POS == 3:
            globalstate.HOLDER['level'] = text.strip()
            message_win.addstr(f' {text}\n', curses.color_pair(85))
            globalstate.PLACEHOLDER = 'Tech Stack'
            globalstate.POS = 4
            message_win.addstr('Enter technologies you use: ', )
            message_win.refresh()
        elif globalstate.POS == 4:
            globalstate.HOLDER['techStack'] = text.strip()
            message_win.addstr(f' {text}\n', curses.color_pair(85))
            globalstate.PLACEHOLDER = 'Loading..'
            globalstate.POS = 4
            message_win.addstr('\n\nSaving your details...\n',
                               curses.color_pair(200))
            message_win.addstr(
                'Your profile would be publicly searchable now!')
            message_win.refresh()
            try:
                apicalls.updateprofile(message_win)
            except:
                showError("An unknown error has occured!", message_win)
    else:
        globalstate.STATUS = 'updateprofile'
        globalstate.PLACEHOLDER = 'Firstname'
        globalstate.POS = 0
        globalstate.HOLDER = {}
        message_win.clear()
        message_win.addstr('Update Profile\n\n', curses.color_pair(200))
        message_win.addstr(
            'Enter your First Name:', )
        message_win.refresh()


def viewprofile(message_win,  input_win=None):
    message_win.clear()
    message_win.addstr('View Profile\n\n', curses.color_pair(200))
    log(
        'Loading Profile Details...', message_win)
    globalstate.PLACEHOLDER = 'Loading'
    globalstate.STATUS = 'loading'
    input_win.clear()
    input_win.addstr("> ")
    input_win.addstr(f'{globalstate.PLACEHOLDER}...',
                     curses.color_pair(236))
    input_win.move(input_win.getyx()[0], 2)
    input_win.refresh()

    try:
        apicalls.getProfile(message_win)
    except:
        showError("An unknown error has occured!", message_win)
    globalstate.STATUS = 'viewprofile'
    globalstate.PLACEHOLDER = 'Back'
    message_win.clear()
    message_win.addstr('View Profile\n\n', curses.color_pair(200))
    message_win.addstr("Username: ")
    message_win.addstr(
        f'{globalstate.USERNAME}', curses.color_pair(200))
    message_win.addstr("\nEmail: ")
    message_win.addstr(
        f'{globalstate.EMAIL}', curses.color_pair(200))
    if globalstate.profileDetails:
        message_win.addstr("\nFirst Name: ")
        message_win.addstr(
            f'{globalstate.profileDetails.get("firstName")}', curses.color_pair(200))
        message_win.addstr("\nLast Name: ")
        message_win.addstr(
            f'{globalstate.profileDetails.get("lastName")}', curses.color_pair(200))
        message_win.addstr("\nBio: ")
        message_win.addstr(
            f'{globalstate.profileDetails.get("bio")}', curses.color_pair(200))
        message_win.addstr("\nLevel: ")
        message_win.addstr(
            f'{globalstate.profileDetails.get("level")}', curses.color_pair(200))
        message_win.addstr("\nTech Stack: ")
        message_win.addstr(
            f'{globalstate.profileDetails.get("techStack")}', curses.color_pair(200))
    message_win.addstr("\n\nMenu:\n", curses.color_pair(47))
    message_win.addstr(
        '1. Back')
    message_win.refresh()


def viewuser(message_win,  input_win=None, text=''):
    if globalstate.STATUS == 'viewuser':
        message_win.clear()
        message_win.addstr('View User Profile\n\n', curses.color_pair(200))
        log(
            'Loading Profile Details...', message_win)
        globalstate.PLACEHOLDER = 'Loading'
        globalstate.STATUS = 'loading'
        input_win.clear()
        input_win.addstr("> ")
        input_win.addstr(f'{globalstate.PLACEHOLDER}...',
                         curses.color_pair(236))
        input_win.move(input_win.getyx()[0], 2)
        input_win.refresh()

        try:
            apicalls.getUser(message_win, text)
        except:
            showError("An unknown error has occured!", message_win)
        globalstate.STATUS = 'viewprofile'
        globalstate.PLACEHOLDER = 'Back'
        message_win.clear()
        message_win.addstr('View User Profile\n\n', curses.color_pair(200))
        message_win.addstr("Username: ")
        message_win.addstr(
            f'{globalstate.USERUSERNAME}', curses.color_pair(200))
        message_win.addstr("\nEmail: ")
        message_win.addstr(
            f'{globalstate.USEREMAIL}', curses.color_pair(200))
        if globalstate.USERprofileDetails:
            message_win.addstr("\nFirst Name: ")
            message_win.addstr(
                f'{globalstate.USERprofileDetails.get("firstName")}', curses.color_pair(200))
            message_win.addstr("\nLast Name: ")
            message_win.addstr(
                f'{globalstate.USERprofileDetails.get("lastName")}', curses.color_pair(200))
            message_win.addstr("\nBio: ")
            message_win.addstr(
                f'{globalstate.USERprofileDetails.get("bio")}', curses.color_pair(200))
            message_win.addstr("\nLevel: ")
            message_win.addstr(
                f'{globalstate.USERprofileDetails.get("level")}', curses.color_pair(200))
            message_win.addstr("\nTech Stack: ")
            message_win.addstr(
                f'{globalstate.USERprofileDetails.get("techStack")}', curses.color_pair(200))
        message_win.addstr("\n\nMenu:\n", curses.color_pair(47))
        message_win.addstr(
            '1. Back')
        message_win.refresh()
    else:
        globalstate.STATUS = 'viewuser'
        globalstate.PLACEHOLDER = 'Username'
        globalstate.POS = 0
        globalstate.HOLDER = {}
        message_win.clear()
        message_win.addstr('View User Profile\n\n', curses.color_pair(200))
        message_win.addstr(
            'Enter the username of the user:', )
        message_win.refresh()


def runhelp(message_win,):
    message_win.clear()
    message_win.addstr('Welcome to the ')
    message_win.addstr('ChitChat ', curses.color_pair(200))
    message_win.addstr('Help Center!\n\n')
    message_win.addstr('To use ChitChat, follow these steps:\n')
    message_win.addstr('1. Launch the app from the command line\n')
    message_win.addstr(
        '2. Choose a login or create account to start chatting with others\n')
    message_win.addstr(
        '3. Get the username of someone you want to chat with\n')
    message_win.addstr(
        '4. Enter "StartChat" to enter a chatroom and start chatting\n')
    message_win.addstr(
        '5. Use the "Quit" option or "Ctrl C" to quit the app\n\n')
    message_win.addstr(
        'If you experience any issues or need further assistance, please contact our customer support team at chitchatcli@gmail.com.\n')
    message_win.addstr("\nMenu:\n", curses.color_pair(47))
    message_win.addstr(
        '1. Back')
    message_win.refresh()


def search(message_win, text='', input_win=None):
    if globalstate.STATUS == 'search':
        message_win.addstr(f'{text}\n', curses.color_pair(85))
        globalstate.PLACEHOLDER = 'Loading'
        globalstate.STATUS = 'loading'
        input_win.clear()
        input_win.addstr("> ")
        input_win.addstr(f'{globalstate.PLACEHOLDER}...',
                         curses.color_pair(236))
        input_win.move(input_win.getyx()[0], 2)
        message_win.refresh()
        input_win.refresh()
        try:
            apicalls.search(message_win, term=text.strip())
        except:
            showError("An unknown error has occured!", message_win)
        globalstate.PLACEHOLDER = 'Search'
        globalstate.STATUS = 'search'
        message_win.addstr("\nMenu:\n", curses.color_pair(47))
        message_win.addstr(
            '1. [Another search term]\n')
        message_win.addstr(
            '2. Back')
        message_win.refresh()

    else:
        globalstate.STATUS = 'search'
        globalstate.PLACEHOLDER = 'Search'
        globalstate.POS = 0
        globalstate.HOLDER = {}
        message_win.clear()
        message_win.addstr('Find People\n\n', curses.color_pair(200))
        message_win.addstr(
            'Please enter a term to search for users: ', )
        message_win.refresh()
