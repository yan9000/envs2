import numpy

def test_run():
    print numpy.array(([2,3,4],[3,4,5]))
    print "---------------------"
    print numpy.empty(4)
    print "---------------------"
    print numpy.ones((5,4), dtype=numpy.int)
    print "---------------------"
    print numpy.random.rand(5,4)
    print "---------------------"
    print numpy.random.randint(10)
    print numpy.random.randint(0,10)
    print numpy.random.randint(0,10, size=5)
    randints = numpy.random.randint(0, 10, size=(2, 3))
    print "---------------------"
    print randints
    print randints.max(axis=1) # X axis or rows
    print randints.max(axis=0) # Y axis or columns




if __name__ == "__main__":
    test_run()
