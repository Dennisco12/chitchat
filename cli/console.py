#!/usr/bin/env python3
"""Module containing the entry point of the command interpreter."""
import cmd
import sys
from cli import event
import requests
from colorama import Fore, Back, Style


class ChitChatCommand(cmd.Cmd):
    """This class represents the command interpreter
    of this project."""

    prompt = '(chitchat) '
    baseurl = 'https://fb1a-102-88-63-48.ngrok-free.app'

    def precmd(self, line):
        """Runs some actions before a line of command is executed.
        Args:
            line (str): The line of command to be transformed.
        Returns:
            str: The next line of command to execute.
        """
        message = 'Welcome to ChitChat, enter "help" to see the list of available commands'
        return line

    def postcmd(self, stop, line):
        """Runs some actions after a line of command is executed.
        Args:
            stop (bool): The continuation condition.
            line (str): The line of command that was executed.
        Returns:
            bool: The continuation condition.
        """
        if not sys.__stdin__.isatty():
            print('(chitchat) ', end='')
        return stop

    def do_help(self, arg):
        """To get help on a command, type help <topic>.
        """
        return super().do_help(arg)

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Executes some actions when the command line is empty.
        """
        return False

    def do_EOF(self, line):
        """Quit command to exit the program"""
        print("")
        return True

    def do_echo(self, line):
        """Echo command"""
        print(line)

    def do_signup(self, line):
        """This creates a user in the database
        return the user id and token"""
        email = input("Please enter your email: ")
        while len(email) == 0:
            print("* Email field cannot be empty, please try again *")
            email = input("Please enter your email: ")
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        url = f'{self.baseurl}/signup'
        data = {"email": email, "username": username, "password": password}
        response = requests.post(url, data=data)
        if response.status_code != 201:
            print("An error has occurred with code:",
                  response.status_code, "\n", response.text)
        else:
            print('Your account has been created succesfully')
            otp = input('Enter the OTP sent to your email: ')
            url = self.baseurl + '/users/confirmOTP'
            res = requests.post(url, data={"otp": otp, "identifier": email})
            if res.status_code == 201:
                print("...Verification succesful...")
                token = res.text
            else:
                otp = input("Verification failed, you have one attempt left: ")
                res = requests.post(
                    url, data={"otp": otp, "identifier": email})
                if res.status_code == 201:
                    print("...Verification succesful...")
                    token = user.get('token')
                    self.prompt = "({}) ".format(username)
                else:
                    print("...Verification failed...")
        return False

    def do_login(self, line):
        """This takes in username or email and password and 
        creates a session for the user"""
        identifier = input(Fore.BLUE + "Enter your username or email: " + Style.RESET_ALL)
        password = input(Fore.BLUE + "Enter your password: " + Style.RESET_ALL)
        url = self.baseurl + '/login'
        res = requests.post(
            url, data={"identifier": identifier.lower(), "password": password})
        if res.status_code != 201 and res.status_code != 202:
            print("An error has occured with code: {} \n {}".format(
                res.status_code, res.text))
            return False
        elif res.status_code == 205:
            print("Welcome back {}, Let's get you verified".format(res.json().get('user').get('username')))
            otp = input("Please enter the OTP sent to your email: ")
            url = f'{self.baseurl}/users/confirmOTP'
            data = {"identifier": identifier, "otp": otp}
            response = requests.post(url, data=data)
            if response.status_code != 201:
                otp = input(
                    "Verification failed, you have one more attempt...")
                data = {"identifier": identifier, "otp": otp}
                response = requests.post(url, data=data)
                if response.status_code != 201:
                    print("Verification failed")
                    return False
                else:
                    print("Your account has been verified successfully, response: {}".format(
                        response.text))

            else:
                print('Your account has been verified succesfully')
        else:
            self._id = res.json().get('user').get('_id')
            self.token = res.json().get('token')
            self.username = res.json().get('user').get('username')
            print("\n Welcome back {}".format(self.username))

        self._id = res.json().get('user').get('_id')
        self.token = res.json().get('token')
        self.username = res.json().get('user').get('username')
        self.prompt = "({}) ".format(self.username)

    def do_updateMe(self, line):
        """This updates the current user profile"""
        try:
            self.prompt = '({}) '.format(self.username)
        except Exception:
            pass
        url = self.baseurl + '/users/me'
        res = requests.get(url, headers={'X-Token': self.token})
        if res.status_code != 201:
            print("User not found, Please sign-in to continue")
            return False
        self.prompt = "({}) ".format(res.json().get('user').get('username'))

        user = res.json().get('user').get('profileDetails')
        
        print("First name: {}".format(user.get('firstName')))
        firstname = input("Enter a new value or press enter to leave it unchanged: ")
        print("Last name: {}".format(user.get('lastName')))
        lastname = input("Enter a new value or press enter to leave it unchanged: ")
        print("Bio: {}".format(user.get('bio')))
        bio = input("Enter a new value or press enter to leave it unchanged: ")
        print('Level: {}'.format(user.get('level')))
        level = input("Enter a new value or press enter to leave it unchanged: ")
        print("Tech stack: {}".format(user.get('techStack')))
        techstack = input("Enter a new value or press enter to leave it unchanged: ")

        newDict = {}
        if len(firstname) != 0:
            newDict['firstName'] = firstname
        if len(lastname) != 0:
            newDict['lastName'] = lastname
        if len(bio) != 0:
            newDict['bio'] = bio
        if len(level) != 0:
            newDict['level'] = level
        if len(techstack) != 0:
            newDict['techStack'] = techstack

        url = self.baseurl + '/users/editProfile'

        res = requests.put(url, data=newDict, headers={"X-Token": self.token})
        if res.status_code != 201:
            print("An error has occured with code: {}. \nError message: {}".format(res.status_code, res.text))
            return False
        else:
            print("Your details have been updated successfully")
        return False

    def do_startchat(self, line):
        """This starts the chat with user
        Usage: startchat <username>"""
        if not line:
            print("* Please include the user you want to chat with. *")
            return False
        recepient = line.split()[0]
        if not self.username:
            print("Please log in to continue")
            return False
        url = self.baseurl + '/startChat/' + recepient
        res = requests.get(url, headers={'X-Token': self.token})
        # for key, val in res.json().items():
        #     print("{}: {}".format(key, val))
        chatroomID = res.json().get('chatroomID')
        recepientID = res.json().get('recepientID')
        messages = res.json().get('messages')

        event.connectToSocket(self.token)
        event.sendMessage(messages, chatroomID, recepientID)

    def do_show(self, line):
        """This display the current user profle"""
        if not line:
            return False
        command = line.split()[0]
        if command == 'me':
            url = self.baseurl + '/users/me'
            resp = requests.get(url, headers={'X-Token': self.token})
            if resp.status_code != 201:
                print("No user found")
                return False
            
            user = resp.json().get('user').get('profileDetails')
            for key, val in user.items():
                print("{} --> {}".format(key, val))
        else:
            print("Usage: show me")
            return False

if __name__ == '__main__':
    # event.connectToSocket()
    ChitChatCommand().cmdloop()
