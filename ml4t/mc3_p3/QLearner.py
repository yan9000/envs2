"""
Template for implementing Q  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0
        
        self.learningRate =  alpha
        self.discountRate = gamma        
        self.rar=rar
        self.radr=radr        
        self.Q = np.random.uniform(low=-1.0,high=1.0,size=(num_states,num_actions))


    def getRandomActionOrQActionWithDecay(self):
        randomNumber=np.random.random()
        if randomNumber < self.rar:
            randomAction = np.random.randint(0,4)
            self.rar = self.rar * self.radr
            #print "randomAction: ", randomAction, self.rar
            return randomAction
        else:
            qLookupAction = np.argmax(self.Q[self.s,:])
            self.rar = self.rar * self.radr
            #print "qLookup: ", qLookupAction, self.rar
            return qLookupAction
        
                 

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        action = self.getRandomActionOrQActionWithDecay()
        self.a=action
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action

        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        
        #print (self.s, self.a, s_prime, r)
        
        oldValue = (1-self.learningRate) * self.Q[self.s, self.a]        
        #stuck here
        aPrime = np.argmax(self.Q[s_prime,:])        
        improvementValue = self.learningRate * (r + self.discountRate * self.Q[s_prime, aPrime])        
        self.Q[self.s, self.a] = oldValue + improvementValue        
        #print "Q[%s, %s] = %s" % (self.s, self.a, self.Q[self.s, self.a])
        
        self.s=s_prime
        action = self.getRandomActionOrQActionWithDecay()
        self.a=action        
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action
    



if __name__=="__main__":
    '''
    learner = QLearner(num_states=100,\
        num_actions = 4, \
        rar = 0.98, \
        radr = 0.9999, \
        verbose=True)

    print learner.Q[0:5, :]
    print learner.query(0, 0)
    print learner.query(1, 0)
    print learner.query(2, 0)
    print learner.query(3, 0)    
    print learner.Q[0:5, :]
    '''