# -*- coding: latin-1 -*-

#
#  IS-105 LAB5
#
#  lab5.py - kildekode som inneholder studentenes l�sning.
#         
#
#


# Skriv inn fullt navn p� gruppemedlemene (erstatte '-' med navn slikt 'Kari Tr�')
gruppe = {  'student1': 'Eirik Kvarstein', \
		'student2': 'Eirik Rørstad Eisentrager', \
}

# Oppgave 
# 	Implementere pokerspill. Vi begynner med representasjon og testing.
#
#	Testing i Python kan gj�res med assert. Eksemplet under skal v�re selvforklarende.
#
#   Det er gitt et kortstokk http://en.wikipedia.org/wiki/Playing_card med 52 kort.
#	I denne oppgaven pr�ver vi � lage et prototype som gir svar p� f�lgende:
#	Hvordan representere alle kort? Hvordan finne ut hvilken h�nd er best?
#
#   Les deg opp p� hva poker er og hvordan det spilles, hvis du ikke kjenner til det fra f�r.
#	Domenkunnskap i systemutvikling er viktigst!!!
#	http://no.wikipedia.org/wiki/Poker
#	http://en.wikipedia.org/wiki/Poker
#
#	Her er et forslag for representasjon av kort og hender, som jeg anbefaler dere � bruke.
#	Dere kan gj�re egne modifikasjoner, med de m� v�re begrunnet i lab5defs.txt filen.
#
#   Typer (kind): H - heart, S - spade, C - club, D - diamond (13 kort av hver type)
#   Verdi (rank): A - ace, K - king, Q - queen, J - jack, T - ten, 9, 8, 7, 6, 5, 4, 3, 2
#   En h�nd (hand): best�r av 5 kort http://en.wikipedia.org/wiki/Hand_rankings
#   H�nd rangeres fra h�yest til lavest (i paranteser anbefalt navn p� variab: 
#		 8 - Straight flush (sf) (finnes ogs� Royal Flush, som er den beste av Straight flush
#		 7 - Four of a Kind (fk) 
#		 6 - Full House (fh) 
#	     5 - Flush (fl)
#		 4 - Straight (st) 
#		 3 - Three of a kind (tk) 
#	     2 - Two Pair (tp) 
#        1 - One Pair (op) 
#        0 - High Card (hc)
#   
#
def poker(hands):
	"""
		Returnerer den beste h�nden: poker([hand, ...]) => hand
		hand_rank er en funksjon som m� skrives og brukes i sammenligningen av "hender"
		Forel�pig fungerer den ikke
	"""
	return max(hands, key=hand_rank)

# Dette er et skall for en funksjon du kan skrive, men det er ikke en oppgave i denne laben.
# Du kan jobbe videre med denne funksjonen i p�f�lgende laber.
def hand_rank(hand):
	"""
		Returnerer en verdi som indikerer verdi av en h�nd. 
		Vi har gitt verdien til hendene i spesifikasjonen (8 Straight Flush, ...)
		Vi m� ogs� kunne skille mellom "like" hender (breaking ties).
		9 9 9 9 5 => (7,9,5) Four of Kind (7) and fife kicker
		3 3 3 3 2 => (7,3,2) Four of Kind (7) and two kicker
		TD 8D 7D 5D 3D => (5, [10,8,7,5,3]) Flush (5) men alle kort m� spesifiseres for � kunne sammenligne
		JC TC 9C 8C 7C => (8, 11) Straight Flush (8) Jack (11) High
		AS AH AC AD QH => (7, 14, 12) Four Aces (7, 14)  and a Queen kicker (12)
	"""
	ranks = card_ranks(hand)
	if straight(ranks) and flush(hand):
		return (8, max(ranks)) # 2 3 4 5 6 => (8, 6)
	elif kind(4, ranks): # kan returnere b�de boolean og tall, i Java 0 er False
		return (7, kind(4, ranks), kind(1, ranks)) # 9 9 9 9 3 (7, 9, 3)
	#elif ...
	
# Funksjonene card_ranks(hand) returnerer en ORDNET tuple av verdier (ranks)
# Verdier for J, Q, K og A er tilsvarende 11, 12, 13, 14. 
# En h�nd TD TC TH 7C 7D skal returnere [10,10,10,7,7]
def card_ranks(hand):
	# Oppgave 4: implementer funksjonen her og legg til testtilfeller i funksjonen test()
	cards = ();
	val = ();
	
	
	#loope gjennom hand og oversette verdier
	for card in hand:
		if(card[0] == "J"):
			val = (11, )
		elif(card[0] == "Q"):
			val = (12, )
		elif(card[0] == "K"):
			val = (13, )
		elif(card[0] == "A"):
			val = (14, )
		elif(card[0] == "T"):
			val = (10, )
		else:
			val = (int(card[0]), ); # tuple

		#Legge til verdien i cards tuple
		cards = cards + val;

	#sortere cards på stigende rekkefølge
	#cards.sort()
	cards  = sorted(cards, reverse=True)
	#debug
	print "hand: %r || values: %r" %(hand,cards)
	
	return cards

# Disse hjelpefunksjonene skal vi jobbe med videre i senere lab oppgaver.
# Funksjonen straight(ranks) returner True hvis h�nden er en Straight.
def straight(ranks):
	return None

# Funksjonen flush(hand) returnerer True hvis h�nden er en Flush.
def flush(hand):
	return None

# Funksjonen kind(nr, ranks) returnerer den f�rste verdien (rank) som h�nden har n�yaktig n av.
# For en h�nd med 4 syvere, skal denne funksjonen returnere 7.
def kind(nr, ranks):
	return None

# Funksjonen two_pair(ranks) gj�r f�lgende:
# hvis det er Two Pair, skal funksjonen returnere deres verdi (rank) som en tuple.
# For eksempel, en h�nd med to toere og 2 firere vil gi en returverdi p� (4, 2).
def two_pair(ranks):
	return None


def test():
   
	# Oppgave 1
	# Den innebygde (built-in) funksjonen max kan brukes for � finne den beste h�nden
	# Skriv test for den innebygde funksjonen max p� flere "list of numbers" (lon)
	# Eksemplene er gitt, du m� kommentere disse ut og sette p� en verdi som ikke gir feil
	lon1 = [6, 7, 8, 0]
	lon2 = [6, 7, -9, 0]
	assert max(lon1) == 8
	assert max(lon2, key=abs) == -9 

	sf = "6C 7C 8C 9C TC".split() # Straight Flush => ['6C', '7C', '8C', '9C', 'TC']
	fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
	fh = "TD TC TH 7C 7D".split() # Full House
	assert poker([sf, fk, fh]) == sf

	# Oppgave 2 
	# Skriv tre nye testtilfeller som sammenligner hender basert p� eksemplet overfor
	# 1) Four of Kind (fk) mot Full House (fh) skal returnere Four of Kind (fk)
	assert poker([fk, fh]) == fk
	# 2) Full House (fh) mot Full House (fh) skal returnere Full House (fh)
	assert poker([fh, fh]) == fh
	# 3) Straight (st) skal slaa Two pair (tp) OBS! Du maa selv lage eksempler paa hender her
	
	st = "5C 6C 7H 8H 9D".split() #straight 
	tp = "6D 6H 8C 8D 3H".split()	# two pair
	
	assert poker([st, tp]) == st

	# Oppgave 3
	# Skriv 2 nye testtilfeller:
	# 1) teste et tilfelle der det kun er en h�nd og at poker returnerer den samme h�nden
	# 2) teste et tilfelle hvor man sammenligner en Straight Flush med 100 Full Houses
	# og det m� da returnere Straight Flush (urealistisk med s� mange spillere, men 
	# vi tar h�yde for det).
	# Hva skjer hvis man har en tom liste som inn-data, dvs. ingen hender?
	assert poker([tp]) == tp
	# 100 full houses ( kommentert ut for slippe spam i debug )
	#assert poker([sf, fh*100]) == sf

	# Oppgave 4
	# Implementer funksjonen card_rank(hand) og legg til tester for 
	# sf, fk og fh variabler som er definert i denne testfunksjonen
	# Du kan gjerne definere flere hender og legge til flere tester :)
	assert card_ranks(sf) == [10, 9, 8, 7, 6]
	assert card_ranks(tp) == [8, 8, 6, 6, 3]
   	assert card_ranks(fh) == [10, 10, 10, 7, 7]
	 
    # Funksjonen hard_rank er enn� ikke implementert
	# Her er gitt noen eksempler p� testing av denne funksjonen som man kan bruke p� et senere tidspunkt
    #
	#assert hand_rank(sf) == (8,10)
	#assert hand_rank(fk) == (7,9,7)
	#assert hand_rank(fh) == (6,10,7)
	return "Done testing"

print test()


