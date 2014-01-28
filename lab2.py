#!/usr/bin/python
# LAB2 - Eirik Kvarstein
import operator; # operator functions
from sys import exit # to invoke exit

#operators
ops = {"+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.div}

#try parse integer from string, returns false if int(string) fails.
def try_parse_int(s, base=10):
        try:
                int(s, base)
                return True
        except ValueError:
                return False

#Check if operator is valid ( check if op is in list )
def valid_operator(op):
        if op in ('+', '-', '*', '/'):
                return True
        else:
                return False


#respond to  math request. 
def math(n1, op, n2):
        if( try_parse_int(n1) and try_parse_int(n2) and valid_operator(op) ): #evaluate user input
                operand = ops[op]; # assign valid operator function
                result = operand(int(n1), int(n2)); # perform math operation
                return "%s %s %s = %d" % (n1, op, n2, result) # return answer
        else:
                return " (!) Syntax: x [+,-,*,/] y, ex: 5 * 2" # return error message


print "LAB2 - functions. Im a simple Math bot,\nI accept questions like this: x [+,-,*,/] y\n"


# main loop
while True:
	question = raw_input("> ") # input fra bruker
	q =  question.split(' '); # splitte opp question ved hver space
	#print "debug: %d items in q" % (len(q)) # debug msg to check number of items in array
	if( len(q) < 3 ): # om q arrayet inneholder mindre enn 3 elementer
		print " (!) Syntax: x [+,-,*,/] y"
				
	else:
		ans = math(q[0], q[1], q[2])	
		print ans

	if ("exit" in question):
		print "Good bye!"
		exit(0)
