"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import os

from util import get_data, plot_data
from portfolio.analysis import get_portfolio_value, get_portfolio_stats, plot_normalized_data

def getValidOrders(start_date, end_date, orders_file):
    myDates = pd.date_range(start_date, end_date)
    dfDates = pd.DataFrame(index=myDates)

    dfSpy = pd.read_csv("../data/SPY.csv", index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
    orders= pd.read_csv(orders_file, index_col="Date", parse_dates=True)
    sortedOrders=orders.sort_index()
    businessDayOrders = sortedOrders.join(dfSpy).dropna().ix[:,0:3]

    validOrders =dfDates.join(businessDayOrders, how='left').dropna()
    return validOrders

def getUniqueSymbols(validOrders):
    return pd.Series(validOrders['Symbol'].ravel()).unique()

def compute_portvals(start_date, end_date, orders_file, start_val):
    """Compute daily portfolio value given a sequence of orders in a CSV file.

    Parameters
    ----------
        start_date: first date to track
        end_date: last date to track
        orders_file: CSV file to read orders from
        start_val: total starting cash available

    Returns
    -------
        portvals: portfolio value for each trading day from start_date to end_date (inclusive)
    """
    # TODO: Your code here

    validOrders = getValidOrders(start_date, end_date, orders_file)    
    #print validOrders
    uniqueSymbols = getUniqueSymbols(validOrders).tolist()    
    #print uniqueSymbols    

    prices = get_data(uniqueSymbols, pd.date_range(start_date, end_date), True)        
    prices['CASH']=1
    #print "prices"
    #print prices
    
    trades = prices.copy()
    trades.ix[:, :] =0
    for index, order in validOrders.iterrows():        
        symbol = [order['Symbol']]        
        symbol = symbol[0]
        price=prices.ix[index, symbol]
        action = [order['Order']]
        action = action[0]
        shares = [order['Shares']]
        shares = shares[0]                
        if action == "SELL":            
            shares = shares * -1 
        trades.ix[index, symbol]= trades.ix[index, symbol] + shares
        trades.ix[index, "CASH"]= trades.ix[index, "CASH"] + (shares * price * -1)    
    #print "trades"
    #print trades
    
    
    holdings = trades.copy()    
    holdings.ix[0, "CASH"]= holdings.ix[0, "CASH"] + start_val
    holdings = holdings.cumsum()
    #print "holdings"
    #print holdings
    
    holdingValues = holdings * prices
    #print "holdingValues"
    #print  holdingValues
    
    portvals = holdingValues.sum(axis=1)
    #print "portvals"
    #print portvals
    
    return portvals


def test_run():
    """Driver function."""
    # Define input parameters    
    #start_date = '2011-01-14'
    #end_date = '2011-12-14'
    start_date ='2008-1-1'
    end_date='2009-12-31'
    start_date ='2010-1-1'
    end_date='2010-12-31'

    orders_file = os.path.join("orders", "yanOutOfSampleOrders.csv")
    start_val = 1000000

    # Process orders
    portvals = compute_portvals(start_date, end_date, orders_file, start_val)

    
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # if a DataFrame is returned select the first column to get a Series
    
    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals)

    # Simulate a $SPX-only reference portfolio to get stats
    prices_SPX = get_data(['SPY'], pd.date_range(start_date, end_date))
    prices_SPX = prices_SPX[['SPY']]  # remove SPY
    portvals_SPX = get_portfolio_value(prices_SPX, [1.0])
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = get_portfolio_stats(portvals_SPX)

    # Compare portfolio against $SPX
    print "Data Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX: {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX: {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX: {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX: {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

    # Plot computed daily portfolio value
    df_temp = pd.concat([portvals, prices_SPX['SPY']], keys=['Portfolio', 'SPY'], axis=1)
    plot_normalized_data(df_temp, title="Daily portfolio value and SPY")
    


if __name__ == "__main__":
    test_run()
