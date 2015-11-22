#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections, re, csv, json

NWORDS = json.load(open('oracle.json'))
alphabet = 'aábcdðeéfghiíjklmnoópqrstuúvwxyýzþæö'

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

def correct(word, lastword):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=lambda c: NWORDS[c]['prevWord'][lastword] if lastword in NWORDS[c]['prevWord'] else 0)

name = raw_input().strip()
correctDataList = []

with open(name) as csvinput:
    csvData = csv.DictReader(csvinput)
    lastword = ""
    for row in csvData:
      correctData = {
          'Word': csvData["Word"],
          'Tag': csvData["Tag"],
          'Lemma': csvData["Lemma"]
      }
      correctData["CorrectWord"] = correct(csvData["Word"], lastword)
      correctDataList.append(correctData)
      lastword = correctData["CorrectWord"]

with open('solution.csv', 'w') as sol:
    fieldnames = ['Word', 'Tag', 'Lemma', 'CorrectWord']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheaders()
    for data in correctDataList:
        writer.writerow({'Word':data['Word'], 'Tag':data['Tag'], 'Lemma':data['Lemma'], 'CorrectWord':data['CorrectWord']})