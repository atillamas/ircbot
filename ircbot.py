import socket
import os
import sys
import yaml

class IRCbot:
    irc = socket.socket()
    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        config = yaml.safe_load(open("./ircbot.config"))
        self.channel  = config['channel']
        self.server   = config['server']
        self.port     = config['port']
        self.botnick = config['nickname']

    def send(self, chan, msg):
        self.irc.send("PRIVMSG " + chan + " " + msg + "\n")


    def connect(self, server, port, channel, botnick):
        self.irc.connect((server,port))
        self.irc.send("USER " + botnick + " " + botnick +" " + botnick + " :l33tbot!\n")
        self.irc.send("NICK " + botnick + "\n")
        self.irc.send("JOIN " + channel + "\n")

    def get_text(self):
        text = self.irc.recv(2040)

        if text.startswith('PING'):
            self.irc.send('PONG ' + text.split()[1] + '\r\n')

        return text


irc = IRCbot()
irc.connect(server, port, channel, nickname)


while 1:
    text = irc.get_text()
    print text

