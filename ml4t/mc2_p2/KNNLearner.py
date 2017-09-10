import numpy
import math


class KNNLearner(object):
    def __init__(self, k):
        self.k = k        
        
    '''
    just store data
    Xtrain is an ndarray where each row represents an x1, x2...xn set of feature values.
    Ytrain is a single dimension ndarray representing the values we are attempting to predict with x
    '''
    def addEvidence(self, Xtrain, Ytrain):
        self.xTrain = Xtrain
        self.yTrain = Ytrain
    
    
    '''
        for each x in Xtest
            compute the distance between it and xTrain.
            sort the xTrain
            get the first k in xTrain
            compute the average
            append to yOut
    '''
    def query(self, Xtest):        
        j=0
        yPredict = numpy.empty(len(Xtest))
        for x in Xtest:
            x1 = self.xTrain[:, 0]
            x2 = self.xTrain[:, 1]
            distance = numpy.sqrt(numpy.power(x1-x[0], 2) + numpy.power(x2-x[1], 2))
            sortedDistance = numpy.argsort(distance)
            yOfNeighbours = numpy.zeros(self.k)
            for i in range(0,self.k):
                yOfNeighbours[i]=self.yTrain[sortedDistance[i]]
            y = numpy.mean(yOfNeighbours)
            yPredict[j]= y
            j=j+1       
        
        return yPredict




        
    