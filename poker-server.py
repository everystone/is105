# -*- coding: latin-1 -*-

# http://pymotw.com/2/select/
# http://www.tutorialspoint.com/python/python_dictionary.htm

# Sockets programmering i Python
# Utforskning av sockets api og andre Python moduler
# Module kan betraktes som en slags plug-in som utvider funksjonaliteten til et grunnlag
# Et grunnlag er programmeringsmiljø som man kan bruke for å gjøre "beregninger" / implementere "systemer"

# select module gir tilgang til platform-spesifikke INN/UT monitorerings-funksjoner
# select() er en POSIX funksjon som det finnes gode implementasjoner for i både UNIX- og Windows miljøer
# POSIX er et forsøk på å standardisere et operativsystem
import select

import socket
import sys
import Queue

import poker

# Her er data for pokerspillet
# For enkelhets skyld deler vi ut kort i det vi starter server
# Dette bør skje på forespørsel fra en klient i neste versjon av programmet
hands = poker.deal(3)
handsdelt = 0 # Vi trenger en variabel som holder styr på hvor mange hender er delt ut
players = 0;
players_ready = 0;
# Lage en TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Binde socketen på lokalmaskinen til porten 10000
server_address = ('localhost', 10000)
print >>sys.stderr, '[+]starter socket på %s og port %s' % server_address
server.bind(server_address)

# Høre / vente på innkommende forbindelser
server.listen(5)

# Med select() kan man følge med på mer enn en forbindelse av gangen
# Argumenter til select() er tre lister som inneholder kommunikasjonskanaler som skal observeres / monitoreres
# (1) liste av objekter for data som kommer inn fra andre enheter og skal leses/avleses/konsumeres
# (2) liste av objekter som vil motta data som er på vei ut, dvs. en slags lagerplass for data som sendes ut til andre enheter
# (3) en liste over de objektene som har feilet, kan være objekter fra både "input" og "output" kanaler
# Man må sette opp lister som inneholder INN-kilder og UT-bestemmelsessted
# Forbindelser blir lagt til og fjernet fra disse listen av hovedløkken til serveren

# Sockets som vi forventer å lese fra (kilder)
inputs = [ server ]

# Sockets hvilke vi forventer å skrive til (bestemmelsessted)
outputs = [ ]

# Man kan ha forskjellige kommunikasjonsstrategier
# Server kan vente for at en socket blir skrivbar (man kan skrive til den) før man sender noen data,
# istedenfor å sende responsen umiddelbart.
# I et slikt tilfelle, trenger hver UT-forbindelse en meldingskø, som fungerer som en mellomlager (buffer)
# Data må da sendes gjennom denne "bufferen", typen som brukes her er dictionary
message_queues = {}

#playernames
playerNames = {}

#player's hand
playerHands = {}

#Broadcast - send to all connected clients
def broadcast(message):
	for key in message_queues.keys():
		message_queues[key].put(message); # legg til message i meldings køen
		outputs.append(key) # legg til socket mottaker i outputs
	
#Announce Winner	
def showdown(s):
	global players_ready;
	if(players_ready < 2): #ikke nok spillere er klare
		message_queues[s].put("[!]Not enough players are ready ("+str(players_ready)+")");
		outputs.append(s); #tell player
	else:
		#Show cards
		response = "*** Player Cards ***\n";
		for key in playerNames.keys():
			cards = ' '.join(str(x) for x in playerHands.get(key))
			response = response + playerNames.get(key)+": "+cards+"\n";
		broadcast(response);
			
		#TODO: kalkulere vinner med poker.hand_rank()
		poker_winner();
		
		players_ready = 0; # new round
	
def poker_winner():
	size=0;
	announce = "*** WINNER ***\n-------------\n";
	msg = "";
	
	for key in playerNames.keys():
		hand = playerHands.get(key);
		player = playerNames.get(key);
		result = poker.hand_rank(hand);
		size = len(result);
		if size == 2:
			if result[0] == 0:
				#player has nothing ( 0 )
				msg =  player + "has nothing.\n ";
			elif result[0] == 4:
				msg = player +" has Straigt! " + str(result[1])+"\n";
		elif size == 3:
			if result[0] == 1: #One pairs
				msg =  player + " has One pair of " + str(result[1])+"\n";
			elif result[0] == 2: #Two pairs
				msg =  player  + " has Two pairs of" + str(result[1])+"\n";
			elif result[0] == 3: #Three of a kind
				msg =  player + " has Three of a kind! " + str(result[1])+"\n";
		
		#Take away players cards
		del playerHands[key];
		announce = announce+msg; #append message
		
	#send message
	broadcast(announce);
				
		
def dealCard(s):
	global players_ready;
	if playerHands.get(s) == None: #player has no cards
		hands = poker.deal(1)
		cards = ' '.join(str(x) for x in hands[0])
		#playerHands.update({s:cards}); #give cards to player
		playerHands.update({s:hands[0]});
		message_queues[s].put("Welcome!\nYour hand: "+cards+"\n"); # add message to queue
		outputs.append(s); #send to player
		players_ready+=1; #one more player is ready
		
		#broadcast that player joined
		broadcast(playerNames.get(s)+"Is ready to play!\n");
		
	else : #player already has cards
		cards = ' '.join(str(x) for x in playerHands.get(s))
		message_queues[s].put("You already joined!\nYour hand: "+cards);
		outputs.append(s);
		
def showPlayers(s):
	response = "\n*** POKER PLAYERS ***\n";
	for key in playerNames.keys():
		response = response + playerNames.get(key)+"\n";
		
	message_queues[s].put(response); #send playerlist
	outputs.append(s); #to client asking
	
def isRegistered(s):
	test = playerNames.get(s);
	if test == None:
		return -1; # not registered
	else:
		return 0; # registered
		
def register_player(name, s):
	if isRegistered(s) == -1: #not registered
		playerNames.update({s:name});
		#message_queues[s].put(">>Registered!");
		#outputs.append(s);
		#broadcast that player registered
		broadcast("[+]"+name+" Registered!");
	else:
		message_queues[s].put("You are already registered as: "+playerNames.get(s));
	


# Hoveddelen av serverprogrammet er denne løkken som løper, og kaller select() som blokkerer utførelsen og 
# venter på nettverksaktivitet
while inputs:
	# Vent inntil minst en av socketene er klar for prosessering
	#print >>sys.stderr, '\nventer på neste hendelse'
	readable, writable, exceptional = select.select(inputs, outputs, inputs)

# select returnerer tre nye lister, som er subset av de opprinnelige listene
# (1) alle socketene i readable listen har mellomlagret INN-data og er klare til å bli lest
# (2) alle socketene i writable har fri lagringsplass i deres lager og kan bli skrevet til
# (3) socketene som er returnert gjennom exceptional har hatt en feil (definisjon av uttak er platformavhengig)

	#for key in message_queues.keys():
		#print >>sys.stderr, '[!]spiller %s er meldt seg for spill' % str(key.getpeername())



# Behandler inputs her
	for s in readable:
		if s is server:
			# En lesbar (readable) server socket er klar til å akseptere forbindelser
			connection, client_address = s.accept()
			print >>sys.stderr, '[+]en ny forbindelse fra', client_address
			connection.setblocking(0)
			inputs.append(connection)
			players+=1; #increase total players
			
			welcome_status = "Welcome to root poker!\nTotal players: %d\n------------------------\nuse \"help\" if you are stuck\n" % players
			
			# Gi forbindelse en kø for data som man ønsker å sende
			message_queues[connection] = Queue.Queue()
			message_queues[connection].put(welcome_status);
			#broadcast at en ny bruker har joina
			broadcast("[+]"+client_address[0]+" has joined!");
			
			
# (2) Dette er tilfelle når man har en allerede etablert forbindelse som man allerede 
#     har brukt for å sende data
#     Data leses med recv(), så blir plassert i en kø, slik at den kan bli sendt gjennom socketen tilbake til klienten
		else:
			data = s.recv(1024)
			if data:
			
				#if newline in data, remove it
				if '\n' in data:
					data = data.rstrip('\n');
					
				# En lesbar klient-socket som har data
				print >>sys.stderr, "mottok \"%s\" fra %s" % (data, s.getpeername())

				

				# Koden skrevet av studenter
				# Sjekk meldingskø og også inputs
				# Her kan man behandle data som man mottar
				# Man kan også gi forskjellig respons til forskjellige klienter
				# OPPGAVE: del ut en hånd til en klient som sender JOIN
				# Her må du tenke på en algoritme som klarer å begrense antall klienter som kan spille
				# og hvor du også må finne en måte å dele ut kort på til hver av spillere
				# hands er her laget ved start av server, men finn også ut 

				if data.startswith("REG"):
					register_player(data[4:], s); #start at char 4 after reg, and host s.getpeername()[0]
					
				#check if player is registered
				elif playerNames.get(s) == None:
					data = "\nPlease register first with REG <name>";
					message_queues[s].put(data);
				
				elif data == 'JOIN':
					dealCard(s); #deal hand to player
				
				elif data == "SHOWDOWN":
					showdown(s) # Announce winner
				
				elif data == "help": #help message
					data = "\nJOIN\t-Join a game of poker!\nSHOWDOWN\t-Show winner of hand\nsay <msg>\t-send chat to everyone\nPLAYERS\t-Show connected players\n";
					message_queues[s].put(data);
				
				elif data == "PLAYERS": #show total players
					showPlayers(s);
				
				elif data.startswith("say"): # chat melding
					meld = playerNames.get(s) + ": "+data[4:];
					broadcast(meld);
				else:
					message_queues[s].put("Unknown command - try \"help\"");
				

				# Legg til UT-kanalen for responsen
				if s not in outputs:
					outputs.append(s)
# (3) En lesbar socket uten tilgjengelige data er fra en klient som har koblet seg fra, slik at strømmen kan lukkes
			else:
				# Interpreter en tom resultat som en lukket forbindelse
				print >>sys.stderr, 'lukker', client_address, 'etter at ingen data kunne leses'
				# Stopper å høre for IN-data på denne forbindelsen
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				s.close()

				# Fjern meldingskø
				del message_queues[s]
				#fjern spillerens kort
				if playerHands.get(s) != None:
					del playerHands[s];
				
				#broadcast at spilleren har forlatt spillet
				if playerNames.get(s) != None:
					broadcast(playerNames.get(s)+" has left the game!");
					#fjern playerName fra playerNames
					del playerNames[s];

# Det er mindre antall muligheter for writable
# Hvis det er data i køen for en forbindelse, neste melding blir sendt
# Ellers, forbindelsen fjernes fra liste for UT-forbindelser, slik at i neste omgang i løkken select()
# ikke skal indikere at socketen er klar til å sende data
	for s in writable:
		try:
			next_msg = message_queues[s].get_nowait()
		except Queue.Empty:
			# Ingen meldinger venter -> stoppe sjekking for skrivbarhet
			print >>sys.stderr, 'UT køen for', s.getpeername(), 'er tom'
			outputs.remove(s)
		else:
			print >>sys.stderr, 'sender "%s" til %s' % (next_msg, s.getpeername())
			s.send(next_msg)

# Til slutt, hvis det er en feil i socketen, den blir lukket
	for s in exceptional:
		print >>sys.stderr, 'behandler feilsituasjon for', s.getpeername()
		# Stoppe å høre for input for forbindelsen
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()

		# Fjern meldingskø
		del message_queues[s]


		
	#for key in message_queues.keys():
		#print >>sys.stderr, '[!]spiller %s er meldt seg for spill' % str(key.getpeername())
s.close()
sys.stdout.write("Terminating Server..");