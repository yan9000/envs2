import pandas
import matplotlib.pyplot as plot


def test_run():
    startDate='2010-01-22'
    endDate='2010-02-26'
    dates = pandas.date_range(startDate, endDate)
    dateFrame =   pandas.DataFrame(index=dates)

    spy = pandas.read_csv("data/SPY.csv", index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
    spy = spy.rename(columns={'Adj Close': 'SPY'})
    dateFrame=dateFrame.join(spy)
    dateFrame=dateFrame.dropna()


    symbols = ['GOOG', 'IBM', 'GLD']
    for symbol in symbols:
        temp=pandas.read_csv("data/{}.csv".format(symbol), index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        temp=temp.rename(columns={"Adj Close":symbol})
        dateFrame=dateFrame.join(temp)

    print dateFrame
    print "-------------------------------------SLICING"
    print dateFrame.ix['2010-01-25':'2010-01-26']
    print "-------------------------------------"
    print dateFrame[['IBM', 'GOOG']]
    print "-------------------------------------"
    print dateFrame.ix['2010-01-25':'2010-01-26', ['IBM', 'GOOG']]
    plotData(dateFrame)

def plotData(df, title="Stock Prices"):
    myPlot = df.plot(title=title)
    myPlot.set_xlabel("date")
    myPlot.set_ylabel("price")
    plot.show()


if __name__=="__main__":
    test_run()