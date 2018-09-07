#!/usr/bin/python3

import re

def solveQuery(reverseIndex, query, numDocs, bracketAnswers):
    """Solves an individual query"""
    if query[0] == "(":
        query = query[1 : len(query) - 1]

    queryTerms = query.split()
    queryLength = len(queryTerms)
    notFlag = False
    for i in range(0, queryLength):
        if queryTerms[i] not in "^|!":
            try:
                if not notFlag:
                    if "bracketAnswer" in queryTerms[i]:
                        queryTerms[i] = bracketAnswers[queryTerms[i]]
                        continue
                    queryTerms[i] = reverseIndex[queryTerms[i].lower()]
                else:   
                    if "bracketAnswer" in queryTerms[i]:
                        queryTerms[i] = [y for y in range(1, numDocs + 1) if y not in bracketAnswers[queryTerms[i]]]
                        continue
                    queryTerms[i] = [y for y in range(1, numDocs + 1) if y not in reverseIndex[queryTerms[i].lower()]]
                    notFlag = False
            except:
                print("Invalid Query Term: " + queryTerms[i])
                raise SystemExit
    
        else:
            if(queryTerms[i] == "!"):
                notFlag = True

    answer = set(queryTerms.pop(0))
    if "!" in answer:
        answer = set(queryTerms.pop(0))
    andFlag = False
    orFlag = False
    for term in queryTerms:
        if term == "!":
            continue
        elif term == "^":
            andFlag = True
        elif term == "|":
            orFlag = True
        else:
            if andFlag:
                answer = answer.intersection(set(term))
                andFlag = False
            elif orFlag:
                answer = answer.union(set(term))
                orFlag = False
    
    return answer

def getAnswer(reverseIndex, query, numDocs):
    """Solves each bracket at a time and finally solves whole query"""
    p = re.compile(r"""\([\s\w\[\],^!\|]+\)""")
    bracketAnswers = dict()
    count = 1
    while True:
        bracket = p.search(query)
        if bracket == None:
            break
        answer = solveQuery(reverseIndex, bracket.group(), numDocs, bracketAnswers)
        bracketAnswers["bracketAnswer" + str(count)] = sorted(list(answer))
        query = query.replace(bracket.group(), "bracketAnswer" + str(count))
        count += 1
    answer = solveQuery(reverseIndex, query, numDocs, bracketAnswers)
    return answer

def buildReverseIndex(docs):
    """Builds revers index for entered document strings"""
    reverseIndex = dict()
    for doc in docs:
	    for word in re.findall(r'\w+', doc[1]):
		    word = word.lower()
		    if word not in reverseIndex:
			    reverseIndex[word] = list()
		    reverseIndex[word].append(doc[0])
    for key in reverseIndex:
	    reverseIndex[key].sort()
    return reverseIndex

def takeInput():
    """Takes input strings and returns it as a list"""
    inputList = list()
    while True:
	    try:
		    inputString = input()
		    inputList.append(inputString.strip())
	    except EOFError:
		    break
    return inputList

def main():
    print("Enter each string on one line. Press Ctrl-D to stop the input.")
    inputDocs = takeInput()
    reverseIndex = buildReverseIndex(zip(range(1, len(inputDocs) + 1), inputDocs))
    print("\nReverse Index: ")
    for key in reverseIndex:
	    print("(" + key + ", " + str(len(reverseIndex[key]))  + ") -> ", end = "")
	    print(reverseIndex[key])
	
    while True:
	    print("\nEnter Query.(^/|/!)")
	    try:
	 	    inputQuery = input()
	 	    answer = getAnswer(reverseIndex, inputQuery, len(inputDocs))
	 	    print(answer)
	    except EOFError:
		    break
	
    print("Thank you!")

if __name__ == '__main__':
    main()
