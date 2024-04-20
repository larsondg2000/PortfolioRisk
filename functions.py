import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Tuple


def get_weights_tickers() -> Tuple[List[str], List[float]]:
    """
    Reads a CSV file to create lists of stock tickers and their corresponding weights in the portfolio.

    :return: A tuple containing two lists - one for stock tickers and one for their weights.
    """
    df = pd.read_csv('my_stocks.csv')

    tickers = 'Ticker'
    stock_list: List[str] = df[tickers].tolist()

    current_stock_value = 'Value'
    stock_value_weights: List[float] = df[current_stock_value].tolist()

    return stock_list, stock_value_weights


def get_historical_returns(stocks: List[str]) -> None:
    """
    Fetches 5-year historical closing prices for each stock using Yahoo Finance and saves it to a CSV file.

    :param stocks: A list of stock tickers.
    :return: None
    """
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365 * 5)).strftime('%Y-%m-%d')

    data = {}

    for stock in stocks:
        ticker = yf.Ticker(stock)
        history = ticker.history(start=start_date, end=end_date)
        data[stock] = history['Close']

    df = pd.DataFrame(data)
    df.index = df.index.tz_localize(None)
    df.bfill(inplace=True)

    df.to_csv('stock_prices.csv', index=True)


def calculate_risk(weights: List[float]) -> None:
    """
    Calculates the portfolio risk and the risk of individual stocks, saving the results to a CSV file.

    :param weights: A list of weights representing the proportion of each stock in the portfolio.
    :return: None
    """
    df = pd.read_csv("stock_prices.csv")
    df.set_index('Date', inplace=True)

    returns_df = df.pct_change(1)
    vcv_matrix = returns_df.cov()

    var_p = np.dot(np.transpose(weights), np.dot(vcv_matrix, weights))
    sd_p = np.sqrt(var_p)

    sd_p_annual = sd_p * np.sqrt(250)
    print(f"Portfolio Risk- annual: {sd_p_annual}")
    print("**********************")

    individual_risks = np.std(returns_df, axis=0, ddof=1) * np.sqrt(250)
    print(f"Individual Risks: \n {individual_risks}")
    print("**********************")

    total_risks = individual_risks
    total_risks.loc['PORTFOLIO'] = sd_p_annual

    total_risks.index.name = 'Ticker'
    total_risks.name = 'Risk'

    total_risks.to_csv('risk_output.csv', index=True)

    plot_risks()


def plot_risks() -> None:
    """
    Plots a bar chart visualizing the risk levels of individual stocks and the overall portfolio risk.

    :return: None
    """
    df = pd.read_csv('risk_output.csv')
    df_sorted = df.sort_values(by=['Risk'], ascending=False)

    sns.set_style("whitegrid", {'grid.linestyle': '-.'})
    sns.catplot(
        data=df_sorted,
        x='Ticker',
        y='Risk',
        kind='bar'
    )
    plt.title('Risk for Individual Stocks and Overall Portfolio Risk', fontdict={'size': 20})
    plt.xlabel('Ticker', fontdict={'size': 14})
    plt.xticks(rotation=90)
