"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import os
import csv

from util import get_data, plot_data
from portfolio.analysis import get_portfolio_value, get_portfolio_stats, plot_normalized_data

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
        df_portvals: portfolio value for each trading day from start_date to end_date (inclusive)
    """

    orders = pd.read_csv(orders_file, names=['year', 'month', 'day', 'symbol', 'action', 'num'], header=None, parse_dates={'date':[0,1,2]}, index_col='date')
    sortedOrders = orders.sort_index()
    print sortedOrders

    ordersWithPrice = pd.DataFrame
    for index, order in sortedOrders.iterrows():
        print index, order['symbol'], order['action'], order['num']
        myDate = pd.date_range(index, index)
        mySymbol = [order['symbol']]
        price = get_data(mySymbol, myDate, False)
        print price

        

    dateRange = pd.date_range(start_date, end_date)
    df_portvals = pd.DataFrame(index=dateRange)
    print df_portvals


    return df_portvals


def test_run():
    """Driver function."""
    # Define input parameters
    start_date = '2011-01-05'
    end_date = '2011-01-20'
    orders_file = os.path.join("orders", "orders-short.csv")
    start_val = 1000000

    # Process orders
    df_portvals = compute_portvals(start_date, end_date, orders_file, start_val)
    '''
    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(df_portvals)

    # Simulate a $SPX-only reference portfolio to get stats
    prices_SPX = get_data(['$SPX'], pd.date_range(start_date, end_date))
    prices_SPX = prices_SPX[['$SPX']]  # remove SPY
    df_portvals_SPX = get_portfolio_value(prices_SPX, [1.0])
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = get_portfolio_stats(df_portvals_SPX)

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

    # Plot computed daily portfolio value
    df_temp = pd.concat([df_portvals, prices_SPX], keys=['Portfolio', '$SPX'], axis=1)
    plot_normalized_data(df_temp, title="Daily portfolio value and $SPX")
    '''


if __name__ == "__main__":
    test_run()
