#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Oracle
import csv, json

dataStuff = {}
wordCount = 0;

fileNameList = ['079', '080', '081', '082', '084', '085', '089', '090', '091', '092', '093', '094', '095', '096',
	'097', '099', '100', '101', '102', '103', '105', '106', '107', '108', '110']

for name in fileNameList:
	with open('althingi_errors/' + name + '.csv') as csvinput:
		reader = csv.DictReader(csvinput)
		lastword = ""
		for row in reader:
			currword = row['CorrectWord']
			if currword != "":
				if currword not in dataStuff: #if word is missing from current data
					dataStuff[currword] = { #log attributes of word
						'count': 1,
						'wrongSpelling': {},
						'prevWord': {}
					}
					if currword != row['Word']:
						ws = row['Word']
						dataStuff[currword]['wrongSpelling'][ws] = 1
					if lastword != "":
						dataStuff[currword]['prevWord'][lastword] = 1
				else: #if word is found in current data
					dataStuff[currword]['count'] += 1
					if currword != row['Word']:
						ws = row['Word']
						if ws not in dataStuff[currword]['wrongSpelling']:
							dataStuff[currword]['wrongSpelling'][ws] = 1
						else:
							dataStuff[currword]['wrongSpelling'][ws] += 1
					if lastword != "":
						if lastword not in dataStuff[currword]['prevWord']:
							dataStuff[currword]['prevWord'][lastword] = 1
						else:
							dataStuff[currword]['prevWord'][lastword] += 1
			lastword = currword
			wordCount += 1
			if wordCount % 100000 == 0:
				print wordCount, lastword, name

with open('oracle.json', 'w+') as doc: #export json
	json.dump(dataStuff, doc)
