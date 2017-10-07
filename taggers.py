import math

# Extract only the lines with the tag 'WORDTAG'
# From the counts output file
def extractWordTags():
    file = open('onlyWordTags.txt','w')
    for i in open('out.counts'):
        if i.split()[1]=='WORDTAG':
            file.write(i)
    file.close()


# There were around 1000 duplicate words
# So, create a list of all the unique words
def uniqueWords():
    temp = []
    for j in open('onlyWordTags.txt','r'):
        temp.append(j.split()[3])
    return list(set(temp))


# Creates a simple model - a dictionary with
# the word as a key and another dictionary as it's value
# This second dictionary contains the Entity type of the word
# and it's count
# Example: {'Games':{'I-LOC': 3, 'I-MISC': 4, 'I-PER': 2}}
# This function also returns another dictionary called neCounts
# Which contains the total number of occurances of particular
# Named Entity type
# Example: {'I-LOC': 678, 'I-MISC': 7898, ....}
def createAModel():
    """
    Creates a dictionary model with all the unique words
    and their occurrences as different Named Entities
    """
    extractWordTags()
    unique = uniqueWords()
    unique.append('_RARE_')
    finalDict = {}
    listOfNE = ['I-LOC', 'I-PER', 'I-MISC', 'I-ORG', 'O', 'B-LOC', 'B-PER',
              'B-MISC', 'B-ORG']
    neCounts = {}
    for i in listOfNE:
        neCounts[i] = 0
    ## Count the total number of Named Entities of each type
    for i in open('onlyWordTags.txt','r'):
        if i.split()[2] in listOfNE:
            neCounts[i.split()[2]]+=int(i.split()[0])

    ## Create the model dictionary
    for i in unique:
        typeDict = {}
        for j in open('onlyWordTags.txt'):
            tempy = j.split()
            if tempy[3]==i:
                typeDict[tempy[2]]=tempy[0]

        finalDict[i]=typeDict

    return finalDict, neCounts


# Finds which named Entity occured most in the dictionary
# And returns the Named Entity and it's count
def maxOfDict(x):
    temp = 0
    winner = ''
    for i in x:
        if float(x[i])>temp:
            temp = float(x[i])
            winner = i
    return winner, temp

# This method predicts the Entity type of the test data
# Along with the Log probability
# It writes the output to '4-2.txt'
def calcEmis(model, necounts):
    """
    Predicts the Entity type along with the log probabilities
    """
    e_dict = {}
    four2 = open('4-2.txt','w')
    for i in open('ner_dev.dat','r'):
        if i=='\n':
            four2.write('\n')
        else:
            curWrd = i.split()[0]
            if curWrd in model:
                buff = model[curWrd]
                highestNE, highestVal = maxOfDict(buff)
                four2.write(curWrd + ' ' + highestNE + ' '+ str(math.log(highestVal/necounts[highestNE], 2)) + '\n')
                e_dict[(curWrd, highestNE)] = math.log(highestVal/necounts[highestNE], 2)
            else:
                buff = model['_RARE_']
                highestNE, highestVal = maxOfDict(buff)
                four2.write(curWrd + ' ' +highestNE+ ' '+ str(math.log(highestVal/necounts[highestNE], 2)) + '\n')
                e_dict[(curWrd, highestNE)] = math.log(highestVal/necounts[highestNE], 2)
    four2.close()
    return e_dict