'''
Created on Dec 25, 2014

@author: mmagdy
'''
import codecs

from eventUtils import getTokens
from evaluate import Evaluate
def evaluate(collFolder,k):
    evalres = []
    for j in range(k):
        
        fn = collFolder+str(j)+'.txt'
        f = codecs.open(fn, encoding='utf-8')
        ftext = f.read()
        text =  ftext.split()#getTokens(ftext)
        text = [t.lower() for t in text]
        '''
        if 'shoot' in text or 'shooter' in text or 'shooting' in text:
            if 'fsu' in text:
                evalres.append(1)
            elif 'florida' in text and 'state' in text :#and 'university' in text:
                evalres.append(1)
            else:
                evalres.append(0)
        else:
            evalres.append(0)
        '''
        '''
        if 'hagupit' in text or 'ruby' in text:
            if 'typhoon' in text:
                evalres.append(1)
            elif 'philippin' in text:
                evalres.append(1)
            else:
                evalres.append(0)
            #evalres.append(1)
        else:
            evalres.append(0)
        '''
        '''
        if 'fire' in text:
            if 'la' in text:
                if 'downtown' in text:
                    evalres.append(1)
                else:
                    evalres.append(0)
            elif 'los' in text and 'angeles' in text:
                if 'downtown' in text:
                    evalres.append(1)
                else:
                    evalres.append(0)
            else:
                evalres.append(0)
        else:
            evalres.append(0)
        '''
        if 'charlie' in text and 'hebdo' in text or 'paris' in text:
            if 'shooting' in text or 'shoot' in text:
                evalres.append(1)
            elif 'attack' in text:
                evalres.append(1)
            else:
                evalres.append(0)
        else:
            evalres.append(0)
        f.close()
    return evalres
class myObj(object):
    def __init__(self):
        self.text =""

def evaluateClassifier(classifierFile,cf,k):
    
    evaluator = Evaluate()
    evaluator.buildClassifier("posFile","negFolder",classifierFile)
    collFiles = []
    for j in range(k):
        
        fn = cf+str(j)+'.txt'
        f = codecs.open(fn, encoding='utf-8')
        ftext = f.read()
        o = myObj()
        o.text = ftext
        collFiles.append(o)
    res = evaluator.evaluateFC(collFiles)
    f = open(cf+'evaluationRes_Words.txt','w')
    f.write('\n'.join([str(r) for r in res]))
    f.close()
    print sum(res)

if __name__ == '__main__':
    '''
    classifierFile = "classifier_Charlie.p"
    collFiles = 'event-webpages/'
    #collFiles = '/base-webpages/'
    evaluateClassifier(classifierFile,collFiles,500)
    '''
    
    j = 2
    #for i in range(3):
    #i=0
    #collFiles = '/Users/mmagdy/fc results/'+str(j)+'/event-'+str(i)+'/event-webpages/'
    #collFiles = '/Users/mmagdy/fc results/'+str(j)+'/base-'+str(i)+'/base-webpages/'
    
    collFiles = 'event-webpages/'
    #collFiles = 'base-webpages/'
    res = evaluate(collFiles,500)
    f = open(collFiles+'evaluationRes_Words.txt','w')
    f.write('\n'.join([str(r) for r in res]))
    f.close()
    print sum(res)
    