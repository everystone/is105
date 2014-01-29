# -*- coding: latin-1 -*-

#
#  IS-105 LAB2
#
#  lab2.py - kildekode som inneholder studentenes lQsning.
#         
#
#
import sys

# Skriv inn fullt navn paa gruppemedlemene (erstatte '-' med navn slikt 'Kari Traa')
gruppe = {  'student1': 'Eirik Kvarstein', \
			'student2': 'Eirik Eisenträger', \
}

#
#  Oppgave 1
#    Leke med utskrift 
#    Skriv ut fQlgende "ascii art" i en funksjon
#    Funksjonen skal hete ascii_fugl() og skal vaere uten argumenter og uten returverdier
#    Den skal skrive ut fQlgende naar den brukes ascii_fugl
#
#       \/_
#  \,   /( ,/
#   \\\' ///
#    \_ /_/
#    (./
#     '` 
def ascii_fugl():
	print "      \\/_"
	print " \\,   /( ,/"
	print "  \\\\\\' ///"
	print "   \\_ /_/"
	print "   (./"
	print "    '`"


# 
#  Oppgave 2
#    'return 2' - 2 skal erstattes med en korrekt returverdi, 2 er kun en stedsholder
#    bitAnd - x&y
#    Eksempel: bitAnd(6, 5) = 4
#
def bitAnd(x, y):
	return x & y

 
#  Oppgave 3
#    bitAnd - x&y
#    Eksempel: bitAnd(6, 5) = 4
#
#def bitAnd(x, y):
#  return 2

#
#  Oppgave 4
#    bitXor - x^y
#    Eksempel: bitXor(4, 5) = 1
#
def bitXor(x, y):
  return x ^ y

#
#  Oppgave 5
#    bitOr - x|y
#    Eksempel: bitOr(0, 1) = 1
#
def bitOr(x, y):
  return (x | y)

#
#  Oppgave 6
#    ascii8Bin - ta et tegn som argument og returnerer ascii-verdien som 8 bits streng binaert
#    Eksempel: ascii8('A) = 01000001
#
#  Tips:
#    For aa finne desimalverdien til et tegn bruk funksjonen ord, for eksempel
#      ord('A) , det vil gi et tall 65 i ti-tallssystemet
#    For aa formattere 6 i ti-tallssystemet til 00000110 i to-tallssystemet
#      '{0:08b}'.format(6)
#      00000110
#
#    Formatteringsstrengen forklart:
#      {} setter en variabel inn i strengen
#      0 tar variabelen i argument posisjon 0
#      : legger til formatteringsmuligheter for denne variabelen (ellers hadde den 6 desimalt)
#      08 formatterer tall til 8 tegn og fuller med nuller til venstre hvis nQdvendig
#      b konverterer tallet til dets binAEre representasjon
def ascii8Bin(bokstav):
	decVal = ord(bokstav)
	return "Ascii: ", bokstav,  " Decimal: ", decVal,  " Binary:  ", '{0:08b}'.format(decVal)

# 
#  Oppgave 7
#    transferBin - ta en tilfeldig streng som argument og skriver ut en blokk av 8-bits strenger
#   som er den binre representasjon av strengen
#    Eksempel: transferBin("Hi") skriver ut: 
#                01001000
#                01101001
#
def transferBin(string): 
	l = list(string)
	print "length of list: ", len(l)
	for c in l:
		print ascii8Bin(c)
# skriv ut den binQre representasjon av hvert tegn (bruk ascii8Bin funksjonen din)

def ascii2Hex(bokstav):
	decVal = ord(bokstav)
	return "Ascii ", bokstav, "Decimal : ", decVal, "Hex: ", '{0:02x}'.format(decVal)
	

# Oppgave 8
# transferHex - gjQr det samme som transferBin, bare skriver ut representasjonen
#av strengen heksadesimalt (bruk formattering forklart i Oppgave 6)
#Skriv gjerne en stQttefunksjon ascii2Hex, som representerer et tegn
#med 2 heksadesimale tegn

def transferHex(string):
	l = list(string)
	for c in l:
		print ascii2Hex(c)




#tests
print "Lab2 - IS105"
print gruppe
print "\nOppgave 1 - ascii_fugl():"
ascii_fugl()

print "\nOppgave 3 - bitAnd(6,5):",  bitAnd(6,5)

print "\nOppgave 4 - bitXor(4,5):", bitXor(4,5)

print "\nOppgave 5 - bitOr(0,1):", bitOr(0,1)

print "\nOppgave 6 - ascii8Bin:"
bokstav = raw_input(">bokstav: ")
print ascii8Bin(bokstav)

print "\nOppgave 7 - transferBin"
setning = raw_input(">Skriv inn et ord:")
transferBin(setning)

print "\nOppgave 8 - transferHex"
setning = raw_input(">Skriv inn et ord:")
transferHex(setning)
