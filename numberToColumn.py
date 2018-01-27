'''
Converts a number to it's column name, 
like in Excel. For e.g.:-
    1 -> A
    2 -> B
    27 -> AA
'''

from string import ascii_lowercase as al
alpha_dict = {x:i for i, x in enumerate(al, 1)}
num_dict = {}
for key, value in alpha_dict.items():
    num_dict[value] = key


def calculateColumnName(n):
    string = []

    while n > 0:
        rem = n % 26

        if rem == 0:
            string.append('z')
            n = (n/26)-1
        else:
            string.append(chr((rem-1) + ord('A')))
            n = n/26
    
    string = string[::-1]
    print(''.join(string).upper())

calculateColumnName(5899) # HRW
calculateColumnName(5899999) # LWQUA
calculateColumnName(2) # B
calculateColumnName(2500)
calculateColumnName(13) # M
calculateColumnName(96) # CR
calculateColumnName(2800) # DCR
calculateColumnName(27) # AA
