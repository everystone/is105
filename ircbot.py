#!/usr/bin/python
#Simple IRC bot
# Eirik Kvarstein

import socket;
import operator;

nick = 'everyb0t'
network = 'irc.quakenet.org'
port = 6667;
chan = "#uia.cs"

#operators
ops = {"+": operator.add,
	"-": operator.sub,
	"*": operator.mul,
	"/": operator.div}

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
        irc.send('PRIVMSG ' + chan + ' :server status: 0\r\n')

    if data.find('>hva er') != -1: #hva er x (op) y
        raw=data.split(' ');
	number1 = int(raw[5]);
	operand = ops[raw[6]];
	number2 = int(raw[7].rstrip('\n\r'));
	result = operand(number1, number2)
	svar =  " :%r %r %r = %r" % (number1, raw[6], number2, result)
	irc.send('PRIVMSG ' + chan + svar + '\r\n')
	#print raw
