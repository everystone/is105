# -*- coding: latin-1 -*-

"""
Poker klient v 0.2
Eirik Kvarstein

"""

import socket
import sys
import select

host = 'localhost'
port = 10000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to server
try:
	s.connect((host,port));
except:
	sys.stdout.write("Connection failed");
	sys.exit();
	
sys.stdout.write('[+]Connected to server\n');



while 1:
	socket_list = [sys.stdin, s] # userinput og  netsocket
	
	# get readable socket ( tcp socket or stdin ( user input ) )
	ready_to_read,ready_to_write,in_error = select.select(socket_list, [], []);
	
	for sock in ready_to_read:
		if sock == s:
			#incoming message from server
			data = sock.recv(size);
			if not data:
				sys.stdout.write("[!] Disconnected.\n\n");
				sys.exit(0);
			else :
				#print data from server
				sys.stdout.write(">>"+data+"\n");
				sys.stdout.write('%');
				sys.stdout.flush(); #flush output buffer
		else :
			# User input
			msg = sys.stdin.readline().rstrip(); #strip newline
			s.send(msg); #send meldingen
	
	

s.close()
sys.stdout.write("Terminating client..");
