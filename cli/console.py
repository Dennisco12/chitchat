#!/usr/bin/python3
"""Module containing the entry point of the command interpreter."""
import cmd
import sys

class ChitChatCommand(cmd.Cmd):
    """This class represents the command interpreter
    of this project."""

    prompt = '(chitchat) '

    def precmd(self, line):
        """Runs some actions before a line of command is executed.
        Args:
            line (str): The line of command to be transformed.
        Returns:
            str: The next line of command to execute.
        """
        pass
    
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


if __name__ == '__main__':
    ChitChatCommand().cmdloop()