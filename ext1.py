#!/usr/bin/python
from sys import argv
script, user_name = argv
prompt = '> '

print "Hello %s, im the %s script." % (user_name, script) #skriver ut script + argv 0
print "is it true that 3 + 2 < 5 - 7?"
print 3 + 2 < 5 - 7 # returnerer true/false
print "what is 3 + 2?", 3+2
print "what is 5-7?", 5-7
print "give me a number"
number = raw_input(prompt) #input 
print "You gave me %r" % (number )

print """
flere linjer
i en print
very clever.
"""
