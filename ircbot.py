import socket
import os
import sys
import yaml
import datetime

class IRCbot:
    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        config = yaml.safe_load(open("./ircbot.config"))
        self.channel  = config['channel']
        self.server   = config['server']
        self.port     = config['port']
        self.botnick = config['nickname']

    def send(self, chan, msg):
        self.irc.send("PRIVMSG " + chan + " " + msg + "\n")


    def connect(self):
        self.irc.connect((self.server,self.port))
        self.irc.send("USER " + self.botnick + " " + self.botnick +" " + self.botnick + " :IRCbot!\n")
        self.irc.send("NICK " + self.botnick + "\n")
        self.irc.send("JOIN " + self.channel + "\n")

    def disconnect(self):
        self.irc.close()

    def get_text(self):
        text = self.irc.recv(2040)

        if text.startswith('PING'):
            self.irc.send('PONG ' + text.split()[1] + '\r\n')

        return text

    def run(self):
        text = self.get_text()
        print str(datetime.datetime.time(datetime.datetime.now())) + " " + text,


if __name__ == '__main__':

    irc = IRCbot()
    irc.connect()
    while 1:
        irc.run()

