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

#try parse integer from string
def try_parse_int(s, base=10):
	try:
    		int(s, base)
		return True
  	except ValueError:
    		return False

#Check if operator is valid
def valid_operator(op):
	if op in ('+', '-', '*', '/'):
		return True
	else:
		return False


# hente username of user sending PRIVMSG to channel
#:everystone!~everyston@146.185.141.215 PRIVMSG #uia.cs :hei
def getUserNick(data):
	nick = data.split('!');
	return nick[0].lstrip('#:');


#respond to ">hva er x + y math request
def math(user, n1, op, n2):
	if( try_parse_int(n1) and try_parse_int(n2) and valid_operator(op) ): #evaluate user input
		operand = ops[op];
		result = operand(int(n1), int(n2));
		return " :%s: %s %s %s = %d" % (user, n1, op, n2, result)
	else:
		return " :%s: (!) Syntax: >hva er x [+,-,*,/] y" % (user)	
		
		

while True: # Main loop
    data=irc.recv(4096) #receive data from socket
    print data # ( debug - print all socket data )

    if data.find('PING') != -1: #If PING is Found in the Data
        irc.send('PONG ' + data.split()[1] + '\r\n') #Send back a PONG
        print "PONG ",data.split()[1]

	################	JOIN CHANNEL		###############
    if data.find(':everyb0t!~everyb0t@146.185.141.215 MODE everyb0t +i') != -1: #we are connected
        irc.send('JOIN ' + chan + '\r\n') #join channel
	print "** Joining channel ", chan
        irc.send('PRIVMSG ' + chan + ' hello\r\n') #say hello to chan

	################# 	CS SERVER STATUS	 ######################
    if data.find('!status') != -1: #CS SERVER STATUS ( TODO: query port 27015 with status query )
        irc.send('PRIVMSG ' + chan + ' :server status: 0\r\n')

	################## 	Matte operasjoner	 #####################
    if data.find('>hva er') != -1: #hva er x (op) y
        raw=data.split(' ');
	user = getUserNick(data)
	svar = math(user, raw[5], raw[6], raw[7].rstrip('\n\r'))	

	irc.send('PRIVMSG ' + chan + svar + '\r\n')
	#print raw
