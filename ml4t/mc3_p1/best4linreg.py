"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import LinRegLearner as lrl
import time

if __name__=="__main__":


    t1 = time.time()
    f = open('Data/best4linreg.csv', 'w')
    i=0
    for i in range(0,2000):
        s = str(i)+ ","+ str(i)+ "," + str(i)+"\n";
        f.write(s)
    f.close
    t2=time.time()
    print "data generation time: ", t2-t1, "seconds"
    
    