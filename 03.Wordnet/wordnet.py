#! /usr/bin/python3

from nltk.corpus import wordnet as wn

#All nouns present in Wordnet
print("All nouns present in Wordnet:")
for (i, synset) in enumerate(list(wn.all_synsets('n'))[:10]):
    print(str(i + 1) + ". " + synset.lemmas()[0].name())
try:
    word = input("Enter a word: ")
except:
    print("No word found. Quitting!")
    raise SystemExit

#Different meanings/senses, synonyms and antonyms of a given word
print("\n")
synonyms = set()
antonyms = set()
print("Different meanings of " + word + ":")
for (i, synset) in enumerate(wn.synsets(word)):
    print(i + 1, end = ". ")
    print(synset.definition())
    #synonyms and antonyms
    for l in synset.lemmas():
        synonyms.add(l.name())
        if l.antonyms():
            antonyms.add(l.antonyms()[0].name())

#Synonyms
print("\n")
print("Synonyms for " + word + ":")
for (i, syn) in enumerate(synonyms):
    print(str(i + 1) + ". " + syn)
print("Number of synonyms for " + word + " : " + str(len(synonyms)))

#Antonyms
print("\n")
print("Antonyms for " + word + ":")
for (i, ant) in enumerate(antonyms):
    print(str(i + 1) + ". " + ant)

#Number of senses in all part of speech category
print("\n")
nouns = wn.synsets(word, pos = wn.NOUN)
verbs = wn.synsets(word, pos = wn.VERB)
adjectives = wn.synsets(word, pos = wn.ADJ)
adverbs = wn.synsets(word, pos = wn.ADV)

print("Number of senses of " + word + " in noun category : " + str(len(nouns)))
print("Number of senses of " + word + " in verb category : " + str(len(verbs)))
print("Number of senses of " + word + " in adjective category : " + str(len(adjectives)))
print("Number of senses of " + word + " in adverb category : " + str(len(adverbs)))

#Hypernyms and Hyponyms
print("\n")
synset = wn.synsets(word)
hypernyms = list()
hyponyms = list()
for syn in synset:
    hypernyms += syn.hypernyms()
    hyponyms += syn.hyponyms()
print("Hypernyms for " + word + " : ")
if len(hypernyms) == 0:
    print("No hypernym found")
else:
    for (i, hypernym) in enumerate(hypernyms):
        print(str(i + 1) + ". " + str(hypernym))
print("Hyponyms for " + word + " : ")
if len(hyponyms) == 0:
    print("No hyponym found")
else:
    for (i, hyponym) in enumerate(hyponyms):
        print(str(i + 1) + ". " + str(hyponym))

#All the words related to sports
print("\n")
print("All words related to sports:")
sports = wn.synsets('sport',pos = 'n')
hypo = lambda s: s.hyponyms()
for sport in sports:
    for synset in list(sport.closure(hypo)):
        print(synset.lemmas()[0].name())

#Similarity
print("\n")
print("First word: " + word)
try:
    word2 = input("Enter second word: ")
except:
    print("No word found. Quitting!")
    raise SystemExit

try:
    w1 = wn.synsets(word)[0]
    w2 = wn.synsets(word2)[0]
except:
    print(word2 + " is an invalid word.")
    raise SystemExit

print("Similarity between " + word + " and " + word2 + " is: " + str(w1.wup_similarity(w2)))
