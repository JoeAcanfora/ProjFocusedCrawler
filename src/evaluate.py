'''
Created on Mar 13, 2014

@author: mohamed
'''
'''
#from SVMClassifier import SVMClassifier
from NBClassifier import NaiveBayesClassifier
import numpy as np
from sklearn import metrics
from Filter import downloadRawDocs
'''
from eventUtils import getFreq, train_SaveClassifier, readFileLines,getTokens, getScalar,getSorted
import os
import math
import pickle
from document import Document

class VSMClassifier(object):
    def __init__(self, topVocabDic,targetDocsTF,relevTh):
        self.docsTF = targetDocsTF
        self.relevanceth = relevTh
        self.topVocabDic = topVocabDic
    def cosSim(self, doc1,doc2):
        sim = 0
        for k in doc1:
            #if k in doc2:
            a = (1 + math.log(doc1[k]))
            b = (1+math.log(doc2[k]))
            sim +=  a * b 
        
        if sim > 0:
            
            sim = float(sim)/(getScalar(doc1) * getScalar(doc2))
            
        else:
            sim = 0
        return sim
    
    def calculate_score(self, doc):
        sims=[]
        docWords = getTokens(doc)
        docTF = getFreq(docWords)
        ndocTF = dict.fromkeys(self.topVocabDic)
        for k in ndocTF:
            if k in docTF:
                ndocTF[k] = docTF[k]
            else:
                ndocTF[k] = 1/math.e
        for dTF in self.docsTF:
            s = self.cosSim(ndocTF, dTF)
            sims.append(s)
        sim = max(sims)
        if sim >= self.relevanceth:
            return [1,sim]
        else:
            return [0,sim]
    
    
class Evaluate(object):
    '''
    classdocs
    '''


    #def __init__(self,pages,posFile,negFile):
    '''
    def __init__(self):
        
        
        #saved = False
        #try:
        #classifierFile = open(classifierFileName,"rb")
        #self.classifier = pickle.load(classifierFile)
        #self.classifier = classifier
        #classifierFile.close()
            
        #except:
        #    self.classifier = train_SaveClassifier(posFile, negFile, classifierFileName)
            
    '''

    def buildClassifierFolder(self,posFile,negFolder,classifierFileName):
        #negURLsFile = 'negFile.txt'
        try:
            classifierFile = open(classifierFileName,"rb")
            self.classifier = pickle.load(classifierFile)
            classifierFile.close()
            
        except:
            posURLs = readFileLines(posFile)
            posLen = len(posURLs)
            negFiles = os.listdir(negFolder)
            negFiles = [os.path.join(negFolder,f) for f in negFiles if f.endswith(".txt")]
            #print negFiles
            negFilesURLs = [readFileLines(f) for f in negFiles]
            
            num = int(round(1.0* posLen/len(negFiles)))
            negURLs = []
            for nfu in negFilesURLs:
                #print len(nfu)
                if num < len(nfu):
                    #negURLs.extend(nfu[:num] )
                    negURLs.append(nfu[:num] )
                else:
                    #negURLs.extend(nfu )
                    negURLs.append(nfu )
            #print len(negURLs)
            #self.classifier = train_SaveClassifierRandom(posURLs, negURLs, classifierFileName)
            self.classifier = train_SaveClassifier(posURLs, negURLs, classifierFileName)
            #return cls

    def buildClassifier(self,posFile,negFile,classifierFileName):
        #negURLsFile = 'negFile.txt'
        try:
            classifierFile = open(classifierFileName,"rb")
            self.classifier = pickle.load(classifierFile)
            classifierFile.close()
            
        except:
            posURLs = readFileLines(posFile)
            negURLs = readFileLines(negFile)
            self.classifier = train_SaveClassifier(posURLs, negURLs, classifierFileName)
            #return cls
    
    def buildVSMClassifier(self,posFile,vsmClassifierFileName,th,topK):
        
        try:
            classifierFile = open(vsmClassifierFileName,"rb")
            self.classifier = pickle.load(classifierFile)
            classifierFile.close()
        except:
            docs = []
            f = open(posFile,'r')
            for url in f:
                url = url.strip()
                d = Document(url)
                if d and d.text:
                    docs.append(d)
            f.close()
            '''
            docsTF = []
            for d in docs:
                wordsFreq = getFreq(d.getWords())
                docsTF.append(wordsFreq)
            self.classifier = VSMClassifier(docsTF,th)
            '''
            docsTF = []
            vocabTFDic = {}
            for d in docs:
                wordsFreq = getFreq(d.getWords())
                docsTF.append(wordsFreq)
                for w in wordsFreq:
                    if w in vocabTFDic:
                        vocabTFDic[w] += wordsFreq[w]
                    else:
                        vocabTFDic[w] = wordsFreq[w]
            
            vocabSorted = getSorted(vocabTFDic.items(), 1)
            topVocabDic = dict(vocabSorted[:topK])
            ndocsTF = []
            for d in docsTF:
                ndocTF = {}
                for k in topVocabDic:
                    if k in d:
                        ndocTF[k] = d[k]
                    else: 
                        ndocTF[k] = 1/math.e
                ndocsTF.append(ndocTF)
                
            
            self.classifier = VSMClassifier(topVocabDic,ndocsTF,th)
            classifierFile = open(vsmClassifierFileName,"wb")
            pickle.dump(self.classifier,classifierFile)
            classifierFile.close()
        
    def evaluateFC(self,pages):
        results=[]
        scores = []
        #for page,score in pages:
        for page in pages:
            #if page.estimatedScore > 0:
            s = self.classifier.calculate_score(page.text)
            r = s[0]
            results.append(r)
            scores.append(s[1])
            #else:
            #    results.append(0)
        print scores
        return results
        
        