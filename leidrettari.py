import collections, re, csv, json

#stafrof = re.compile('[a-z\sáðéíótúýþæö]+', re.UNICODE)

#def words(text): return stafrof.findall(text)

NWORDS = json.load(open('oracle.json'))
alphabet = 'aábcdðeéfghiíjklmnoópqrstuúvwxyýzþæö'

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

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

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

name = raw_input().strip()
correctDataList = []

with open(name) as csvinput:
    csvData = csv.DictReader(csvinput)
    for row in csvData:
      correctData = {
          'Word': csvData["Word"],
          'Tag': csvData["Tag"],
          'Lemma': csvData["Lemma"]
      }
      correctData["CorrectWord"] = correct(csvData["Word"])
      correctDataList.append(correctData)

with open('solution.csv', 'w') as sol:
    fieldnames = ['Word', 'Tag', 'Lemma', 'CorrectWord']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheaders()
    for data in correctDataList:
        writer.writerow({'Word':data['Word'], 'Tag':data['Tag'], 'Lemma':data['Lemma'], 'CorrectWord':data['CorrectWord']})