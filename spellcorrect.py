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
alphabet = ['a','á','b','c','d','ð','e','é','f','g','h','i','í','j','k','l','m','n','o','ó','p','q','r','s','t','u','ú','v','w','x','y','ý','z','þ','æ','ö']
print alphabet
punctuations = '., '
#Check whether deleting, transposing, replacing or inserting gives a better result
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   if len(word) <= 2:
       singletons = [c for c in alphabet]
   else:
       singletons = []
   return set(deletes + transposes + replaces + inserts + singletons)

#Checks whether edits are feasible
def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

#Checks if a word is already known from training
def known(words): return set(w for w in words if w in NWORDS)

#Find the most likely correction if needed
def correct(word, lemma, lastword):
    if word == 'i': return 'í' #algorithm finds 'i' to be a legit word
    candidates = known([word]) or known(edits1(word)) or known_edits2(word)# or [word]
    keyfunc = lambda c: NWORDS[c]['prevWord'][lastword] if (lastword not in punctuations and lastword in NWORDS[c]['prevWord']) else 0
    if len(candidates) <= 0:
        return word
    return max(candidates, key=keyfunc)

#filename taken from stdin
name = raw_input().strip()
wordCounter = 0

#read input csv
with open(name) as csvinput:
    reader = csv.DictReader(csvinput)
    lastword = ""
    #open output csv, create if not exists
    with open('solution.csv','w+') as sol:
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
            lastword = data["CorrectWord"]
            wordCounter += 1
            if wordCounter % 100 == 0:
                print wordCounter #show progress in terminal

