import numpy
import math
import KNNLearner as knn

#learner = bl.BagLearner(learner = knn.KNNLearner, kwargs = {"k":3}, bags = 20, boost = False)

class BagLearner(object):


    def __init__(self, learner, kwargs, bags, boost):
        self.bags=bags
        self.learners = []
        for i in range(0,bags):
            l=learner(**kwargs)
            self.learners.append(l)


    def addEvidence(self, Xtrain, Ytrain):
        trainSize = len(Ytrain)
        for learner in self.learners:
            randomIndicies =numpy.random.randint(0,trainSize-1, size=trainSize)
            learner.addEvidence(Xtrain[randomIndicies], Ytrain[randomIndicies])

    
    '''
        for each learner in learners[]
            get yOut using query
            get average of yOut
    '''
    def query(self, Xtest):
        j=0
        yPredict = numpy.empty(len(Xtest))
        yOuts = numpy.empty([len(Xtest), self.bags])
        for learner in self.learners:
            yOut = learner.query(Xtest)
            yOuts[:,j]=yOut
            j=j+1
        yPredict = yOuts.mean(axis=1)
        return yPredict