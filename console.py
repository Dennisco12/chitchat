#!/usr/bin/python3

import cmd

class Chitchat(cmd.Cmd):
    """This is the entry for the console"""
    prompt = '(chitchat): '
    
    def do_quit(self, args):
        """This quits the console"""
        return True

if __name__ == '__main__':
    Chitchat().cmdloop()
