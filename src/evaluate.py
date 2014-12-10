'''
Created on Mar 13, 2014

@author: mohamed
'''
#from SVMClassifier import SVMClassifier
from NBClassifier import NaiveBayesClassifier
from SVMClassifier import SVMClassifier
import numpy as np
from sklearn import metrics
from Filter import downloadRawDocs, getTokenizedDocs
import pickle
class Evaluate(object):
    '''
    classdocs
    '''


    #def __init__(self,pages,posFile,negFile):
    def __init__(self,posFile,negFile):
        '''
        Constructor
        '''
        #saved = False
        try:
            classifierFile = open("savedClassifier.p","rb")
            self.classifier = pickle.load(classifierFile)
            classifierFile.close()
            
        except:
            #self.pages = pages
            #posURLs = getSeedURLs(posFile)
            posDocs = downloadRawDocs(posFile)
            #posDocs = getTokenizedDocs(docs)
            
            #negURLs = getSeedURLs(negFile)
            negDocs = downloadRawDocs(negFile)
            #negDocs = getTokenizedDocs(docs) 
            posLen = len(posDocs)
            negLen = len(negDocs)
            posLabels = [1]* posLen
            negLabels = [0]*negLen 
            
            posSep = int(posLen*0.7)
            negSep = int(negLen*0.7)
            
            trainingDocs = posDocs[:posSep] + negDocs[:negSep]
            
            trainingLabels = posLabels[:posSep] + negLabels[:negSep]
            
            testDocs = posDocs[posSep:] + negDocs[negSep:]
            test_labels=posLabels[posSep:] + negLabels[negSep:]
            
            self.classifier = NaiveBayesClassifier()
            #self.classifier = SVMClassifier()
            
            #trainingLabelsArr = np.array(labels)
            #classifier.trainClassifier(docs,trainingLabelsArr)
            
            trainingLabelsArr = np.array(trainingLabels)
            self.classifier.trainClassifier(trainingDocs,trainingLabelsArr)
            
            test_labelsArr = np.array(test_labels)
            print self.classifier.score(testDocs, test_labelsArr)
            
            print metrics.classification_report(test_labelsArr, self.classifier.predicted)
            classifierFile = open("savedClassifier.p","wb")
            pickle.dump(self.classifier,classifierFile)
            classifierFile.close()
    
    def evaluateFC(self,pages):
        results=[]
        for page,score in pages:
            #results.append(self.classifier.calculate_score(page.text))
            if score ==1:
                s = self.classifier.calculate_score(page.text)[0]
                results.append(s)
            else:
                results.append(0)
        return results
        
        