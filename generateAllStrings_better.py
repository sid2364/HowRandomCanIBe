import sys

total_list = []

def generateAllCombinations(n, m, arr, ci=0):
	if ci == n:
		return
	for num in range(m+1):
		arr[ci] = num
		total_list.append(list(arr))
		generateAllCombinations(n, m, arr, ci+1)

if __name__=="__main__":
	try:
		n, m = int(sys.argv[1]), int(sys.argv[2])
	except (IndexError, ValueError) as e:
		print("usage: python <file> <n> <m>\n" +
			"\tn: length of the string, integer\n" +
			"\tm: range of the digits, integer")
		sys.exit(1)
	final = []
	generateAllCombinations(n,m,[0]*n)
	for element in total_list:
		final.append(''.join((str(x) for x in element)))
	for number in sorted(set(final)):
		print(number)
		
