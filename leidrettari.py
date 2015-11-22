#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections, re, csv, json

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

NWORDS = byteify(json.load(open('oracle.json')))
alphabet = 'aábcdðeéfghiíjklmnoópqrstuúvwxyýzþæö'
punctuations = '., '

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word, lemma, lastword):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    keyfunc = lambda c: NWORDS[c]['prevWord'][lastword] if (lastword not in punctuations and lastword in NWORDS[c]['prevWord']) else 0
    return max(candidates, key=keyfunc)

name = raw_input().strip()
#correctDataList = []
wordCounter = 0
correctCounter = 0

print name

with open(name) as csvinput:
    reader = csv.DictReader(csvinput)
    lastword = ""
    with open('solution.csv', 'w') as sol:
        fieldnames = ['Word', 'Tag', 'Lemma', 'CorrectWord']
        writer = csv.DictWriter(sol, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            data = {
                'Word': row['Word'],
                'Tag': row['Tag'],
                'Lemma': row['Lemma']
            }
            data['CorrectWord'] = correct(row['Word'], row['Lemma'], lastword)
            writer.writerow({'Word':data['Word'], 'Tag':data['Tag'], 'Lemma':data['Lemma'], 'CorrectWord':data['CorrectWord']})
            #correctDataList.append(correctData)
            lastword = data["CorrectWord"]
            wordCounter += 1
            if 'CorrectWord' in row and row['CorrectWord']==data['CorrectWord']:
                correctCounter += 1
            if wordCounter % 100 == 0:
                print wordCounter, correctCounter, 100*correctCounter/wordCounter


#with open('solution.csv', 'w') as sol:
#    fieldnames = ['Word', 'Tag', 'Lemma', 'CorrectWord']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#    writer.writeheaders()
#    for data in correctDataList:
#        writer.writerow({'Word':data['Word'], 'Tag':data['Tag'], 'Lemma':data['Lemma'], 'CorrectWord':data['CorrectWord']})