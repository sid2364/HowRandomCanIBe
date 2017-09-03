#!/usr/bin/python

import itertools
import sys

def flatten(ln):
	'''
	This function is used to flatten a
	list of lists into one simple list.
	'''
	if isinstance(ln,list):
		for l in ln:
			for y in flatten(l):
				yield y
	else:
		yield ln

def combine(x, y):
	'''
	This function returns all combinations of the 
	individual elements in two inputs; x and y.
	'''
	if y is None:
		return []
	if type(x) is not list:
		x = [x]
	product = list(itertools.product(x, y))
	pr_l = []
	for ele in product:
		pr_l.append(list(ele))
	ret = []
	for ele in pr_l:
		flat_list = flatten(ele[1])
		for item in flat_list:
			ret.append(str(ele[0]) + str(item))
	return ret

def generateAllCombinations(n, m):
	'''
	This is a recursive function that descends down
	breaking the problem into smaller chunks and handling
	them bottom-up with the help of combine() and flatten().
	For e.g., if n=3, m=2 then it will combine each of [0, 1, 2]
	since m=2 with the output of this function when n=2, m=2.
	The exit condition is when n=1; which is the starting point
	for combining elements and the permutations that form the
	building blocks for this algorithm.
	'''
	final = []
	if n==0 or m==0:
		return 0
	if n==1:
		return range(m+1)
	for i in range(m + 1):
		combined = combine(i, generateAllCombinations(n-1, m))
		final.append(combined)
	
	return final

if __name__=="__main__":
	try:
		'''
		Taking input from command line parameters.
		IndexError will occur if 2 arguments are not passed,
		ValueError will occur if arguments passed are not numbers,
		Extra arguments parsed are ignored.
		'''
		n, m = int(sys.argv[1]), int(sys.argv[2])
	except (IndexError, ValueError) as e:
		print("usage: python <file> <n> <m>\n" + 
			"\tn: length of the string, integer\n" + 
			"\tm: range of the digits, integer")
		sys.exit(1)

	a = flatten(generateAllCombinations(n,m))
	for ele in a:
		print(ele)
