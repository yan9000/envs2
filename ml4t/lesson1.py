import pandas as reader
import matplotlib.pyplot as plot

def test_run():
    dataframe = reader.read_csv("data/primes1000.csv")
    print dataframe.head()
    print dataframe.tail()
    print(dataframe[10:21])
    print dataframe['prime(n)'].max()
    print dataframe['prime(n)'].mean()

    dataframe['prime(n)'].plot()
    plot.xlabel("x")
    plot.title("primes")
    plot.show()

if __name__=="__main__":
    test_run()