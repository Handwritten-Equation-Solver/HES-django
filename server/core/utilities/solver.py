import numpy as np


# TODO : Takes a list of predicted characters and parses it into the required format
def isAlphabet(a):
	if ord(a) >= ord('a') and ord(a) <= ord('z'):
		return True
	if ord(a) >= ord('A') and ord(a) <= ord('Z'):
		return True
	return False

def isNum(a):
	if ord(a) <= ord('9') and ord(a) >= ord('0'):
		return True
	return False

def getExp(charList, i):
	if i == len(charList):
		return 1
	if not isNum(charList[i]):
		return 1

	ret = 0
	while i<len(charList):
		if not isNum(charList[i]):
			break
		ret = ret*10 + ord(charList[i]) - ord('0')
		i+=1

	return ret

def getNum(charList, i):
	ret = 0
	exp = 0.1
	flag = 0
	while i<len(charList):
		if(isNum(charList[i])):
			if flag == 0:
				ret = ret*10 + ord(charList[i]) - ord('0')
			else:
				ret += (ord(charList[i]) - ord('0'))*exp
				exp/=10
		elif charList[i] == '.':
			flag = 1
		else:
			break

		i+=1

	return ret

def getNumOffset(charList, i):
	cnt = 0
	while i<len(charList):
		if isNum(charList[i]) or charList[i] == '.':
			cnt+=1
		else:
			break

		i+=1

	return cnt

def getExpOffset(charList, i):
	cnt = 0
	while i<len(charList):
		if isNum(charList[i]):
			cnt+=1
		else:
			break

		i+=1

	return cnt

def parse(charList):
	#Get Degree
	degree = 0
	i = 0
	while i<len(charList):
		if isAlphabet(charList[i]):
			i+=1
			exponent = getExp(charList, i)
			i += getExpOffset(charList, i)
			degree = max(degree, exponent)
		i+=1


	eqn = [0]*(degree +1)
	i = 0
	sign = 1
	equalToFlag = 0
	while i<len(charList):
		if isNum(charList[i]):
			coeff = getNum(charList, i)
			i += getNumOffset(charList, i)
			if i == len(charList):
				eqn[0] += coeff*sign
			elif isAlphabet(charList[i]):
				i+=1
				exp = getExp(charList, i)
				i += getExpOffset(charList, i)
				eqn[exp] += coeff*sign
			else:
				eqn[0] += coeff*sign

			continue
		elif isAlphabet(charList[i]):
			i+=1
			coeff=1
			exp = getExp(charList, i)
			i += getExpOffset(charList, i)
			eqn[exp] += coeff*sign

			continue
		elif charList[i] == '-' and equalToFlag == 0:
			sign = -1
		elif charList[i] == '-':
			sign = 1
		elif charList[i] == '+' and equalToFlag == 0:
			sign = 1
		elif charList[i] == '+':
			sign = -1
		elif charList[i] == '=':
			equalToFlag = 1
			sign = -1

		i+=1

	print(eqn[::-1])

# TODO : Parse the predicted characters into required format and return the solutions
eqn = input()
parse(eqn)