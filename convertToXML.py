#!/usr/bin/python

import xml.etree.cElementTree as ET
import sqlite3
import json
import sys
from lxml import etree

xml_file = "einfo.xml"

eid = 'id'
name = 'name'
managerid = 'managerid'
subords = 'subords'
topmost='topmost'


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
			item = finditem(v, key, new_item)
			if item is not None:
				v[key] = new_item
	return obj


def parse_dict(data_dict):
	'''
	Takes input a dictionary that contains information
	about all employees and returns a heirarchically
	arranged dictionary that reflects the manager heirarchy.
	'''
	parsed_data_dict = {}
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
				data_dict[i][subords].append(data_dict[key])
				del parsed_data_dict[key]

	return parsed_data_dict



def addToXml(pd, data_dict, xml_root):
	'''
	This function recurses through the dictionary
	from the second level on and adds a new XML 
	element for each item and calls this function 
	for each of it's sub-items passing itself as the root
	so the XML is formed with this heirarchy.
	'''
	node = ET.SubElement(xml_root, "Node", name=pd[name], eid=str(pd[eid]))
	for sub in pd[subords]:
		addToXml(sub, data_dict, node)
	return

def createXml(parsed_data_dict, data_dict, xml_root):
	'''
	Driver function for the root elements (or 'top-most managers')
	for addToXml(). It calls addToXml() for each 'top-most manager'.
	'''
	for key in parsed_data_dict:
		node = ET.SubElement(xml_root, "Node", name=data_dict[key][name], eid=str(data_dict[key][eid]))

		subs = parsed_data_dict[key][subords]
		for sub in subs:
			addToXml(sub, data_dict, node)
	tree = ET.ElementTree(xml_root)
	return tree

def createAndFillDbAndTable():
	'''
	This function is simply to create a database and table, and add 
	entries into it. It then parses the database and returns a dictionary.
	'''
	data_dict = {}
	conn = sqlite3.connect('generic_employee.db')
	conn.executescript('DROP TABLE IF EXISTS EMPLOYEES;')
	conn.execute('''CREATE TABLE EMPLOYEES
	         (ID INT PRIMARY KEY     NOT NULL,
	         NAME           TEXT    NOT NULL,
	         MANAGERID            INT);''')
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (1, 'A', 2 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (2, 'B', 4 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (3, 'C', 4 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (4, 'D', NULL )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (5, 'D', 6 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (6, 'E', 9 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (7, 'F', 8 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (8, 'G', 9 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (9, 'H', NULL )");
	
	cursor = conn.execute("SELECT ID, NAME, MANAGERID from EMPLOYEES")
	for row in cursor:
		data_dict[row[0]] = {eid:row[0], name:row[1], managerid:row[2], subords:[]}

	return data_dict


if __name__ == "__main__":
	data_dict = createAndFillDbAndTable()
	try:
		parsed_data_dict = parse_dict(data_dict)
	except KeyError as e:
		'''
		KeyError will occur when there exists a 'loop' in the manager heirarchy.
		For e.g., 3 -> 4 -> 2 -> 3, is invalid.
		'''
		print("Manager heirarchy is invalid!\nCannot proceed with current setup.")
		sys.exit(1)

	root = ET.Element("EmpInfo")
	tree = createXml(parsed_data_dict, data_dict, root)

	tree.write(xml_file)

	x = etree.parse(xml_file)
	print(etree.tostring(x, pretty_print=True))
