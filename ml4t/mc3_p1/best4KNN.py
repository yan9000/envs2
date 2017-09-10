

import numpy as np
import math
import time

if __name__=="__main__":


    t1 = time.time()
    f = open('Data/best4knn.csv', 'w')

    for i in range(0,500):
        s = str(i)+ ","+ str(i)+ "," + str(i)+"\n";
        f.write(s)

    for i in range(500,600):
        s = str(i)+ ","+ str(i)+ ",500"+"\n";
        f.write(s)

    for i in range(600,1100):
        s = str(i)+ ","+ str(i)+ "," + str(np.random.randint(0, 500))+"\n";
        f.write(s)

    f.close
    t2=time.time()
    print "data generation time: ", t2-t1, "seconds"
    

