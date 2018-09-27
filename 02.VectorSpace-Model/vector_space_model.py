#!/usr/bin/python3

import re
import math

def solveQuery(query, terms, termDocumentMatrix):
    query = query.lower()
    queryTerms = [re.search(r"""\w+""", word).group() for word in query.split()]
    query = [0] * len(terms)
    numTerm = len(terms)
    numDocs = len(termDocumentMatrix[terms[0]])
    for i in range(numTerm):
        query[i] = queryTerms.count(terms[i])
    
    queryMod = math.sqrt(sum([x * x for x in query]))
    try:
        for i in range(numTerm):
            query[i] = query[i] / queryMod
    except ZeroDivisionError:
        return None

    similarity = [0] * numDocs
    for i in range(numDocs):
        doc = list()
        for term in terms:
            doc.append(termDocumentMatrix[term][i])

        docMod = math.sqrt(sum([x * x for x in doc]))
        doc = [x / docMod for x in doc]
        
        similarity[i] = sum([doc[i] * query[i] for i in range(numTerm)])
        
    return similarity

def getDocumentFrequencies(terms, docs):
    documentFrequency = dict()
    for term in terms:
        documentFrequency[term] = 0
        for doc in docs:
            if term in doc:
                documentFrequency[term] += 1
    return documentFrequency

def printTermDocumentMatrix(matrix, terms):
    for term in terms:
        print(term + " -> " + str(matrix[term]))
    print("")

def createTermDocumentMatrix(inputDocs):
    terms = set()
    docs = list()
    for doc in inputDocs:
        docsList = list()
        for word in doc.split():
            w = re.search(r"""\w+""", word)
            if w != None:
                terms.add(w.group())
                docsList.append(w.group())
        docs.append(docsList)

    terms = list(terms)
    terms.sort()

    termDocumentMatrix = dict()
    for term in terms:
        termDocumentMatrix[term] = [0] * len(inputDocs)
        for (index, doc) in enumerate(docs):
            if term in doc:
                termDocumentMatrix[term][index] += 1
    
    print("Initial Term Document Matrix")
    printTermDocumentMatrix(termDocumentMatrix, terms)

    documentFrequency = getDocumentFrequencies(terms, docs)

    #printTermDocumentMatrix(documentFrequency, terms)

    numDocs = len(docs)
    for term in termDocumentMatrix:
        for i in range(numDocs):
            if termDocumentMatrix[term][i] != 0:
                termDocumentMatrix[term][i] = (1 + math.log10(termDocumentMatrix[term][i])) * math.log10(numDocs/documentFrequency[term])
    
    print("Modified Term Document Matrix")
    printTermDocumentMatrix(termDocumentMatrix, terms)

    return (terms, termDocumentMatrix)

def takeInput():
    inputDocs = list()
    while True:
        try:
            inputString = input()
            inputDocs.append(inputString.lower())
        except EOFError:
            break
    return inputDocs

def main():
    print("Vector Space Model")
    print("Enter each string on each line. Press Ctrl-D to stop.")
    inputDocs = takeInput()
    terms, termDocumentMatrix = createTermDocumentMatrix(inputDocs)
    
    print("Enter query on each line. Press Ctrl-D to stop.")
    while True:
        print("")
        try:
            query = input()
            similarity = solveQuery(query, terms, termDocumentMatrix)
            if similarity == None:
                print("No document contains query terms. Ranking could not be found.")
                continue
            print("Cosine Similarity: " + str(similarity))
            print("Ranking:")
            for i in range(len(inputDocs)):
                print(inputDocs[similarity.index(max(similarity))])
                similarity[similarity.index(max(similarity))] = -1
        except EOFError:
            break
    print("Thank You")
    
if __name__ == '__main__':
    main()
