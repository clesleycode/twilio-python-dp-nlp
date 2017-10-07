import math

# takes in the file of words and turns them into trigrams
def create_trigram_text(filename):
    f1 = open(filename, 'r')
    f2 = open('trigrams.txt', 'w')
    current_tri = []
    for i in f1:
        if len(current_tri) < 3:
            current_tri.append(i.strip())
        else:
            f2.write(" ".join(current_tri)+"\n")
            current_tri = []
            current_tri.append(i.strip())


# Filter Trigrams and Bigrams from the counts file
def trigrams(filename):
    tri_dict = {}
    bi_dict = {}
    for i in open(filename):
        current = i.split()
        if current[1] == '3-GRAM':
            tri_dict[current[2] + ' ' + current[3] + ' ' + current[4]] = current[0];
        ## Need Bi-Gram counts in further computations
        if current[1] == '2-GRAM':
            bi_dict[current[2] + ' ' + current[3]] = current[0];
    return tri_dict, bi_dict

""" 
    Usage: This function computes the log probabilities
        p(yi|yi−2, yi−1) = Count(yi−2, yi−1, yi)/Count(yi−2, yi−1)
        For example: p(I_MISC| I_PER, I_ORG) = trigram count of 
        I_PER I_ORG I_MISC / bigram count of I_PER I_ORG      
"""
def computeLogProb(tri, bi):
    file = open('5-1.txt','w')
    for i in tri.keys():
        temp = i.split()
        prob = math.log(int(tri[i]) / int(bi[temp[0] + ' ' + temp[1]]), 2)
        file.write(i + ' ' + str(prob) + '\n');
    file.close()


if __name__ == '__main__':
    create_trigram_text('ner_dev.dat')
    tri, bi = trigrams('out.counts')
    computeLogProb(tri, bi)

