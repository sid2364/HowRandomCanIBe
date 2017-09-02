#!/usr/bin/python

import itertools
import sys

def flatten(ln):
	if isinstance(ln,list):
		for l in ln:
			for y in flatten(l):
				yield y
	else:
		yield ln

def combine(x, y):
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
	final = []
	if n==0 or m==0:
		return
	if n==1:
		return range(m+1)
	for i in range(m + 1):
		combined = combine(i, generateAllCombinations(n-1, m))
		final.append(combined)
	
	return final

if __name__=="__main__":
	try:
		n, m = int(sys.argv[1]), int(sys.argv[2])
	except (IndexError, ValueError) as e:
		print("usage: python generateAllStrings.py <n> <m>\n" + 
			"\tn: length of the string, integer\n" + 
			"\tm: range of the digits, integer")
		sys.exit(1)

	a = flatten(generateAllCombinations(n,m))
	for ele in a:
		print(ele)
