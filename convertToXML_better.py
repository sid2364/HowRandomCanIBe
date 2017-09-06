#!/usr/bin/python

import xml.etree.cElementTree as ET
import sqlite3
import json
import sys
from lxml import etree

root = 'root'
name = 'name'
under = 'under'
db = 'generic_employee.db'
xml_file = 'emp_data.xml'


def createAndFillDbAndTable():
	'''
	This function is simply to create a database and table, and add 
	entries into it. It then parses the database and returns a dictionary.
	'''
	data_dict = {}
	conn = sqlite3.connect(db)
	conn.executescript('DROP TABLE IF EXISTS EMPLOYEES;')
	conn.execute('''CREATE TABLE EMPLOYEES
	         (ID INT PRIMARY KEY     NOT NULL,
	         NAME           TEXT    NOT NULL,
	         MANAGERID            INT);''')
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (1, 'A', 2 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (2, 'B', 4 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (3, 'C', 4 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (4, 'D', NULL )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (5, 'D', 4 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (6, 'E', 7 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (7, 'F', 8 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (8, 'G', 9 )");
	conn.execute("INSERT INTO EMPLOYEES (ID,NAME,MANAGERID) VALUES (9, 'H', NULL )");
	
	cursor = conn.execute("SELECT ID, NAME, MANAGERID from EMPLOYEES")
	for row in cursor:
		key = row[2]
		if row[2] is None:
			key = root
		try:
			data_dict[key]
		except KeyError:
			data_dict[key] = []
		data_dict[key].append(row[0])
	conn.commit()
	conn.close()
	return data_dict

def getName(eid):
	conn = sqlite3.connect(db)
	cursor = conn.execute("SELECT NAME from EMPLOYEES where ID=%s" % (eid))
	retv = cursor.fetchone()[0]
	conn.close()
	return retv

def addToXML(data_dict, elements, xml_root):
	for ele in elements:
		name_ = getName(ele)
		node = ET.SubElement(xml_root, "Node", name=str(name_), eid=str(ele))
		try:
			subs = data_dict[ele]
			addToXML(data_dict, subs, node)
		except KeyError:
			pass

def writeXML(data_dict):
	root_eles = data_dict[root]
	xml_root = ET.Element("EmpInfo")
	addToXML(data_dict, root_eles, xml_root)
	tree = ET.ElementTree(xml_root)
	return tree

if __name__ == "__main__":
	data_dict = createAndFillDbAndTable()
	tree = writeXML(data_dict)

	tree.write(xml_file)

	x = etree.parse(xml_file)
	print(etree.tostring(x, pretty_print=True))
