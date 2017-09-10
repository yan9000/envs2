import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import math
import KNNLearner as knn
import numpy as np

stockSymbol = 'ML4T-399'
#stockSymbol = 'IBM'
windowSize = 20


def test_run():
    
    startDate ='2008-1-1'
    endDate='2009-12-31'
    #startDate ='2010-1-1'
    #endDate='2010-12-31'

    trainX, trainY, trainingData = getFeaturesInDateRange(endDate, startDate)
    learner = knn.KNNLearner(3)
    learner.addEvidence(trainX, trainY)
    predY = learner.query(trainX)
    print "In sample results"
    printRmseAndCorrelation(predY, trainY)
    implementTradingPolicy(predY, trainingData, "yanInSampleOrders.csv")


    startDate ='2010-1-1'
    endDate='2010-12-31'

    testX, testY, testData = getFeaturesInDateRange(endDate, startDate)
    testPredY = learner.query(testX)
    print
    print "Out of sample results"
    printRmseAndCorrelation(testPredY, testY)
    implementTradingPolicy(testPredY, testData, "yanOutOfSampleOrders.csv")


def implementTradingPolicy(predY, trainingData, ordersFileName):
    trainingData['predY'] = predY
    trainingData['trainYPrice'] = trainingData[stockSymbol] * (1 + trainingData['trainY'])
    trainingData['predYPrice'] = trainingData[stockSymbol] * (1 + trainingData['predY'])
    ax = trainingData['trainYPrice'].plot(title='knn', label="training Y", color='blue', fontsize=12)
    trainingData[stockSymbol].plot(label='price', ax=ax, color='grey')
    trainingData['predYPrice'].plot(label='predicted Y', ax=ax, color='red')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    state = 'none'
    holdCount = 0
    f = open(ordersFileName, 'w')
    f.write("Date,Symbol,Order,Shares\n")
    for i, row in trainingData.iterrows():
        predReturn = trainingData.ix[i, 'predY']

        if (state != 'long' and predReturn >= 0.03 and holdCount == 0):
            state = 'long'
            holdCount = 5
            ax.axvline(i, color='green', linestyle='--')
            f.write(str(i) + "," + stockSymbol + "," + "BUY" + "," + "100\n")

        if (state != 'short' and predReturn <= -0.03 and holdCount == 0):
            state = 'short'
            holdCount = 5
            ax.axvline(i, color='red', linestyle='--')
            f.write(str(i) + "," + stockSymbol + "," + "SELL" + "," + "100\n")

        if ((state == 'long' or state == 'short') and holdCount > 0):
            holdCount = holdCount - 1

        if (state == 'long' and holdCount == 0):
            state = 'none'
            f.write(str(i) + "," + stockSymbol + "," + "SELL" + "," + "100\n")
            ax.axvline(i, color='black', linestyle='--')

        if (state == 'short' and holdCount == 0):
            state = 'none'
            f.write(str(i) + "," + stockSymbol + "," + "BUY" + "," + "100\n")
            ax.axvline(i, color='black', linestyle='--')
    plt.show()


def printRmseAndCorrelation(predY, trainY):
    rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0, 1]


def getFeaturesInDateRange(endDate, startDate):
    dates = pd.date_range(startDate, endDate)
    symbols = [stockSymbol]
    df = get_data(symbols, dates)
    dfPrice = pd.DataFrame(df[stockSymbol])
    trainingData = getTrainingData(dfPrice)
    trainX = trainingData.values[:, 1:4]
    trainY = trainingData.values[:, 4]
    return trainX, trainY, trainingData


def getTrainingData(dfPrice):
    rollingMean = get_rolling_mean(dfPrice, window=windowSize)
    standardDeviation = get_rolling_std(dfPrice, window=windowSize)
    normalizedBollinger = (dfPrice - rollingMean) / (2 * standardDeviation)
    normalizedBollinger = normalizedBollinger.rename(columns={stockSymbol: 'bollinger'})
    # print normalizedBollinger[windowSize-1:].head()
    # print "bollinger size: ", len(normalizedBollinger[windowSize-1:])
    trainData = dfPrice.join(normalizedBollinger[windowSize - 1:]).dropna()
    momentum = dfPrice / dfPrice.shift(-windowSize) - 1
    momentum = momentum.rename(columns={stockSymbol: 'momentum'})
    # print momentum[:-windowSize].tail()
    # print "momentum size: ", len(momentum[:-windowSize])
    trainData = trainData.join(momentum[:-windowSize]).dropna()
    dailyReturns = (dfPrice / dfPrice.shift(1)) - 1
    volatility = get_rolling_std(dailyReturns[1:], window=windowSize)
    volatility = volatility.rename(columns={stockSymbol: 'volatility'})
    # print volatility[windowSize-1:].head()
    # print "volatility size: ", len(volatility[windowSize-1:])
    trainData = trainData.join(volatility[windowSize - 1:]).dropna()
    # print trainData.head()
    trainY = (dfPrice.shift(-5) / dfPrice) - 1
    trainY=trainY.rename(columns={stockSymbol: 'trainY'})

    trainData =  trainData.join(trainY).dropna()
    return trainData


def symbol_to_path(symbol, base_dir="../data"):
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])
    return df

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified winsdow size."""
    return pd.rolling_std(values, window=window)

if __name__ == "__main__":
    test_run()
