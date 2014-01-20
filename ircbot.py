#!/usr/bin/python
#Simple IRC bot
# Eirik Kvarstein

import socket;

nick = 'everyb0t'
network = 'irc.quakenet.org'
port = 6667;
chan = "#uia.cs"

#define socket
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Connecting to ", network
irc.connect((network,port)) #connect
print "Connected! sending user info"
# send info
irc.recv(4096)
irc.send('NICK ' + nick + '\r\n') #send nickname
irc.send('USER everyb0t everyb0t everyb0t :everystone_bot\r\n') #send user info
print "********* Bot online *********"


while True: #loop
    data=irc.recv(4096) #receive data from socket
    print data #Print data to console

    if data.find('PING') != -1: #If PING is Found in the Data
        irc.send('PONG ' + data.split()[1] + '\r\n') #Send back a PONG
        print "PONG ",data.split()[1]

    if data.find(':everyb0t!~everyb0t@146.185.141.215 MODE everyb0t +i') != -1: #we are connected
        irc.send('JOIN ' + chan + '\r\n') #join channel
	print "** Joining channel ", chan
        irc.send('PRIVMSG ' + chan + ' hello\r\n') #say hello to chan

    if data.find('!status') != -1: #CS SERVER STATUS ( TODO: query port 27015 with status query )
        irc.send('PRIVMSG ' + chan + ' CS\ server\ status:\ \r\n')
