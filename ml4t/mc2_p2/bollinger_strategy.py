"""Bollinger Bands."""

import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import math

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
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.rolling_std(values, window=window)


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + 2 * rstd
    lower_band = rm - 2 * rstd
    return upper_band, lower_band

def get_portfolio_stats(port_val, daily_rf=0, samples_per_year=252):
    cum_ret = (port_val[-1] / port_val[0]) - 1

    dailyReturns = (port_val / port_val.shift(1)) -1
    dailyReturns=dailyReturns[1:] #exlcude 0th value from portfolio statistics because it's always zero.

    avg_daily_ret = dailyReturns.mean()
    std_daily_ret = dailyReturns.std()

    sharpe_ratio = math.sqrt(samples_per_year) * (avg_daily_ret - daily_rf)/std_daily_ret
    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio

def get_portfolio_value(prices, allocs, start_val=1):
    normalized = prices/prices.ix[0, :]
    allocated = normalized * allocs * start_val
    dailySum= allocated.sum(axis=1)

    port_val = dailySum
    return port_val

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def plot_normalized_data(df, title="Normalized prices", xlabel="Date", ylabel="Normalized price"):
    df = df/df.ix[0, :]
    plot_data(df, title, xlabel, ylabel)


def test_run():
    # Read data
    startDate ='2007-12-31'
    endDate='2009-12-31'
    dates = pd.date_range(startDate, endDate )
    symbols = ['IBM']
    df = get_data(symbols, dates)

    # Compute Bollinger Bands
    # 1. Compute rolling mean
    rm_IBM = get_rolling_mean(df['IBM'], window=20)

    # 2. Compute rolling standard deviation
    rstd_IBM = get_rolling_std(df['IBM'], window=20)

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_IBM, rstd_IBM)

     # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = df['IBM'].plot(title="Bollinger Band Strategy Chart for IBM", label='IBM', color="blue")
    rm_IBM.plot(label='SMA', ax=ax, color='purple')
    upper_band.plot(label='Upper Band', ax=ax, color="grey")
    lower_band.plot(label='Lower Band', ax=ax, color="grey")
    #df['SPY'].plot(label='spy', ax=ax, color="yellow")

    dfTop = df['IBM'] - upper_band
    dfMiddle = df['IBM'] - rm_IBM
    dfBottom = df['IBM'] - lower_band

    dfTop.name='top'
    dfMiddle.name='middle'
    dfBottom.name='bottom'

    dfPrices =  df.join(dfTop, how='left').join(dfMiddle, how='left').join(dfBottom, how='left')
    dfPrices = dfPrices.dropna()
    dfPrices['cash'] =  1
    #print dfPrices

    trades = dfPrices.copy()
    trades.ix[:, :] =0

    '''
        region 1
    top
        region 2
    middle
        region 3
    bottom
        region 4
    '''
    currentState = 'unknown'
    for i, row in dfPrices.iterrows():
        price=dfPrices.ix[i, 'IBM']
        #print i, row['top'], row['middle'], row['bottom']
        if row['top'] >= 0 and (currentState == 'unknown' or currentState=='exitLong' or currentState == 'exitShort'):
            currentState = 'startShort'
        if row['middle'] >= 0 and row['top']<0  and currentState == 'startShort':
            currentState = 'short'
            ax.axvline(i, color='red', linestyle='--')
            trades.ix[i, 'IBM'] = trades.ix[i, 'IBM'] - 100
            trades.ix[i, "cash"]= trades.ix[i, "cash"] + (100 * price)
            print str(i) + " IBM SELL 100"
        if row['bottom'] >= 0 and row['middle']<0 and currentState == 'short':
            currentState = 'exitShort'
            ax.axvline(i, color='black', linestyle='--')
            trades.ix[i, 'IBM'] = trades.ix[i, 'IBM'] + 100
            trades.ix[i, "cash"]= trades.ix[i, "cash"] - (100 * price)
            print str(i) + " IBM BUY 100"

        if row['middle'] >= 0 and currentState == 'long':
            currentState = 'exitLong'
            ax.axvline(i, color='black', linestyle='-')
            trades.ix[i, 'IBM'] = trades.ix[i, 'IBM'] - 100
            trades.ix[i, "cash"]= trades.ix[i, "cash"] + (100 * price)
            print str(i) + " IBM SELL 100"
        if row['bottom'] >= 0 and currentState == 'startLong':
            currentState = 'long'
            ax.axvline(i, color='green', linestyle='-')
            trades.ix[i, 'IBM'] = trades.ix[i, 'IBM'] + 100
            trades.ix[i, "cash"]= trades.ix[i, "cash"] - (100 * price)
            print str(i) + " IBM BUY 100"
        if row['bottom'] < 0 and (currentState == 'unknown' or currentState == 'exitShort' or currentState == 'exitLong'):
            currentState = 'startLong'

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()

    #print 'trades'
    #print trades

    holdings = trades.copy()
    holdings.ix[0, "cash"]= holdings.ix[0, "cash"] + 10000
    holdings = holdings.cumsum()

    #print 'holdings'
    #print holdings

    holdingValues = holdings * dfPrices
    #print "holdingValues"
    #print  holdingValues

    portvals = holdingValues.sum(axis=1)
    #print "portVals"
    #print  portvals


    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # if a DataFrame is returned select the first column to get a Series

    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals)

    # Simulate a SPY-only reference portfolio to get stats
    prices_SPX = get_data(['SPY'], pd.date_range(startDate, endDate))
    prices_SPX = prices_SPX[['SPY']]  # remove SPY
    #print "prices spy"
    #print prices_SPX
    portvals_SPX = get_portfolio_value(prices_SPX, [10000.0])
    #print "portvals spy"
    #print portvals_SPX
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = get_portfolio_stats(portvals_SPX)

    # Compare portfolio against SPY
    print "Data Range: {} to {}".format(startDate, endDate)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY: {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY: {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY: {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY: {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

    # Plot computed daily portfolio value
    df_temp = pd.concat([portvals, portvals_SPX], keys=['Portfolio', 'SPY'], axis=1)
    df_temp = df_temp.fillna(method="backfill")
    #print "dftemp"
    #print df_temp
    plot_normalized_data(df_temp, title="Daily portfolio value and SPY")



if __name__ == "__main__":
    test_run()
