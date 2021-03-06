#!/usr/bin/env python2

import socket
import os
import sys
import yaml
import datetime

class IRCbot:
    def __init__(self):
        ''' Initialize instance'''
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        config = self.load_config("./ircbot.config")
        self.channel = config['channel']
        self.server = config['server']
        self.port = config['port']
        self.botnick = config['nickname']

    def load_config(self, filename):
        ''' Loads config file if it exist, else exit with error message '''
        if os.path.isfile(filename):
            try:
                config = yaml.safe_load(open("./ircbot.config"))
            except:
                print "Error loading config file"
                sys.exit(1)
        return config


    def send(self, chan, msg):
        ''' Function to send message to irc channel '''
        self.irc.send("PRIVMSG " + chan + " " + msg + "\n")


    def connect(self):
        ''' Connect to IRC channel '''
        self.irc.connect((self.server,self.port))
        self.irc.send("USER " + self.botnick + " " + self.botnick +" " + self.botnick + " :IRCbot!\n")
        self.irc.send("NICK " + self.botnick + "\n")
        self.irc.send("JOIN " + self.channel + "\n")

    def disconnect(self):
        ''' Disconnect from IRC server, closing socket '''
        self.irc.close()

    def reconnect(self):
        ''' Reconnect to IRC Channel '''
        self.irc.close()
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def get_text(self):
        ''' Function that recieves text from IRC server and returns it '''
        text = self.irc.recv(2040)

        if text.startswith('PING'):
            self.irc.send('PONG ' + text.split()[1] + '\r\n')

        return text

    def check_url(self, string):
	''' Function that checks if given string contains one or more urls, returns a list with found urls '''
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
	if urls:
	    print "Found url: ", urls
	    return urls
	else:
	    return False

    def run(self):
        ''' Main function running logic'''
        text = self.get_text()
        print str(datetime.datetime.time(datetime.datetime.now())) + " " + text,


if __name__ == '__main__':

    irc = IRCbot()
    irc.connect()
    while 1:
        irc.run()

