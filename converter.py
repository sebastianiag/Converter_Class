import sys
from math import log

class Converter:

	def __init__(self, number):
		number= float(number)	#In case number is type int, then I don't have to worry about a non-existent decimal point
		if 'e' in str(number):
			number = "%.10f" %number
		point = str(number).find('.')				#Position of the decimal point
		self.integer= str(number)[:point]
		if self.integer[0]=="-":	#If number is signed, first bit is eliminated and sign is equal to "1"
			self.integer = self.integer[1:]
			self.sign = "1"
		else:
			self.sign = "0"

		self.decimal = str(number)[point:]
		self.result = ""

	def integerConverter(self):

		array=[]
		n =  int(self.integer)
		if n ==0:
			return 0

		pows = int(log(n,2))
		x=range(pows+1)
		x.reverse()

		for i in x:
			if pow(2,i) > n:
				array.append(str(0))
			else:
				n= n - pow(2,i)
				array.append(str(1))

		x = ''.join(array)
		return x						#Returns string

	def fractionalConverter(self):		#Converts fractional part of the number to binary
		
		result = ""
		num =  float(self.decimal)
		for i in range(1, 101):				#Up to 100 units to the right

			if  1.0/pow(2.0,i) > num:					
				result = result + "0"
			else:
				num =  num -  1.0/pow(2, i)
				result = result +"1"

		return result

	def scientificFormatting(self):

		integerB =  self.integerConverter()
		decimalB =  self.fractionalConverter()

		if int(integerB) != 0:
			
			exponent =  integerB.__len__() -1	#int

			result =  integerB[1:] + decimalB        #The mantissa of our scientific notation number

		else:
			exponent= -(decimalB.find('1')+1)		#int
			result = decimalB[abs(exponent):]				#Same as the result above

		return (result, exponent)

	def BtoHex(self):
		stack =  self.result
		i = 0
		Hex= ""
		hashes = {10 : "A", 11: "B", 12: "C", 13: "D", 14:"E", 15:"F"}	#Used a hash for simplicity...the program is still too lenghty for my taste
		while i < stack.__len__():
			part =  stack[i:i+4]		#Gets the first four elements
			j = 3						#Sets initial exponent of '2' to 3
			accumulate = 0				#Initialization of the variable that will hold the value for every 4 bits
			for K in part:
				if K == "1":
					accumulate = accumulate+ pow(2, j)
				j-=1
			if accumulate >=10:
				Hex = Hex + hashes[accumulate]		#For the range of 10-15, it pulls a letter from the hash instead 
			else:
				Hex =  Hex + str(accumulate)		#For the range of 0-9, it converts that number into string
			i += 4
		return Hex
				
	def floatIt(self, expWidth, mantissa, bias):

		result, exponent =  self.scientificFormatting()
		exponent = Converter(exponent+bias).integerConverter()
		while exponent.__len__() < expWidth:
			exponent = "0"+exponent				#Sign extension so that we can make sure we always have the desired width

		self.result= self.sign + exponent + result[0:mantissa]	#Type: string

		return self.BtoHex()+"h"
		


def main():
	
	number =  Converter(float(sys.argv[1]))
	print number.floatIt(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
	
	
if __name__ == "__main__":
	main()