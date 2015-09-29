__author__ = 'frankhe'

import cPickle
import numpy as np
import os


def generate_matrix(dtype="train"):
    """ type is "train" or "test"
        TOTAL_WORDS is the number of keywords
        TOTAL_EMAILS is the number of training emails"""
    allWordMap = cPickle.load(open("all_word_map.pkl"))
    importantWords = set([int(x) for x in open("The_most_important_words.txt").read().split()])
    TOTAL_WORDS = len(importantWords)
    keywordMap = {}
    wordIndex = 0
    for word in allWordMap:
        if allWordMap[word] in importantWords:
            keywordMap[word] = wordIndex
            wordIndex += 1
    # add training files
    files1 = os.listdir("./"+dtype+"/spam")
    files1 = ["./"+dtype+"/spam/"+x for x in files1]
    files2 = os.listdir("./"+dtype+"/ham")
    files2 = ["./"+dtype+"/ham/"+x for x in files2]
    files = files1+files2
    # print len(files)
    TOTAL_EMAILS = 0
    X = np.empty([TOTAL_WORDS+1,1])


    for file_it in files:
        if file_it == ".DS_Store":
            continue
        TOTAL_EMAILS += 1
        wordList = filter(lambda x: x.isalpha() and x in keywordMap, open(file_it).read().lower().split())
        # print wordList
        newX = np.zeros([TOTAL_WORDS+1,1])
        for word in wordList:
            newX[keywordMap[word],0] += 1
            # print newX[allWordMap[word],0]
        # './train/spam/' './test/spam/'
        if file_it[:13]=='./'+dtype+'/spam/' or file_it[:12]=='./'+dtype+'/spam/':
            newX[-1,0] = 1
        else:
            newX[-1,0] = 0
        if TOTAL_EMAILS==1:
            X = newX
        else:
            X = np.concatenate((X,newX),axis=1)
        print "collecting data:", TOTAL_EMAILS
        # raw_input()

    f = open(dtype+"_matrix.txt",mode='w')
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            f.write(str(X[i,j])+' ')
        f.write('\n')

generate_matrix()
generate_matrix("test")
