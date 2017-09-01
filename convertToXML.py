import sqlite3
import json
from lxml import etree

conn = sqlite3.connect('generic_employee.db')
conn.executescript('DROP TABLE IF EXISTS EMPLOYEES;')
conn.execute('''CREATE TABLE EMPLOYEES
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         MANAGERID            INT);''')
conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) \
      VALUES (1, 'A', 2 )");
conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) \
      VALUES (2, 'B', 4 )");
conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) \
      VALUES (3, 'C', 4 )");
conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) \
      VALUES (4, 'D', NULL )");


def finditem(obj, key):
	items = []
	if key in obj:
		items.append(obj[key])
	for k, v in obj.items():
		if isinstance(v,dict):
			item = finditem(v, key)
			if item is not None:
				items.append(item)
	return items

def replaceitem(obj, key, new_item):
	if key in obj:
		obj[key] = new_item
	for k, v in obj.items():
		if isinstance(v,dict):
			item = _finditem(v, key, new_item)
			if item is not None:
				v[key] = new_item
	return obj


eid = 'id'
name = 'name'
managerid = 'managerid'
subords = 'subords'
topmost='topmost'

data_dict = {}
cursor = conn.execute("SELECT ID, NAME, MANAGERID from EMPLOYEES")
for row in cursor:
	data_dict[row[0]] = {eid:row[0], name:row[1], managerid:row[2], subords:[], topmost:-1}

print(json.dumps(data_dict, indent=4))

parsed_data_dict = dict(data_dict)

for key in data_dict:
	parsed_data_dict[key] = {}
	parsed_data_dict[key][subords] = []

for key in data_dict:
	mid = data_dict[key][managerid]
	for i in data_dict:
		if i == key:
			continue
		if mid == data_dict[i][eid]:
			parsed_data_dict[i][subords].append(data_dict[key])
			#data_dict[key] = replaceitem(data_dict[key], topmost, mid)
			data_dict[i][subords].append(data_dict[key])
			del parsed_data_dict[key]

for key in data_dict:
	data_dict[key] = replaceitem(data_dict[key], topmost, data_dict[key][managerid])

print("$$$$$$$$$$$$$$$")
print(json.dumps(parsed_data_dict, indent=4))
topmosts = finditem(data_dict, topmost)
print(topmosts)
