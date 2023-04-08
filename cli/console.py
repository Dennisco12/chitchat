#!/usr/bin/python3
"""Module containing the entry point of the command interpreter."""
import cmd
import sys
# import event
import requests


class ChitChatCommand(cmd.Cmd):
    """This class represents the command interpreter
    of this project."""

    prompt = '(chitchat) '
    baseurl = 'https://1ccd-102-88-62-5.eu.ngrok.io'

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
                    token = res.text
                else:
                    print("...Verification failed...")
        return False

    def do_login(self, line):
        """This takes in username or email and password and 
        creates a session for the user"""
        identifier = input("Enter your username or email: ")
        password = input("Enter your password: ")
        url = self.baseurl + '/login'
        res = requests.post(
            url, data={"identifier": identifier.lower(), "password": password})
        if res.status_code != 201 and res.status_code != 202:
            print("An error has occured with code: {} \n {}".format(
                res.status_code, res.text))
            return False
        elif res.status_code == 205:
            print("Welcome back {}, Let's get you verified".format(res.text))
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


if __name__ == '__main__':
    # event.connectToSocket()
    ChitChatCommand().cmdloop()
