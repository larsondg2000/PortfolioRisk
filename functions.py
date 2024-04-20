import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def get_weights_tickers():
    """
    input sheet
    create ticker list
    create weights list (individual stock value/portfolio total)
    :return:
    """
    # Read the Excel file and specify the sheet name
    df = pd.read_csv('my_stocks.csv')

    # Create a list stock tickers
    tickers = 'Ticker'
    stock_list = df[tickers].tolist()

    # Create a list of weights (assumes 'Value' is percentage of portfolio)
    current_stock_value = 'Value'
    stock_value_weights = df[current_stock_value].tolist()

    # Optional Method: use if my_stocks file list values as dollar amounts vs portfolio percentage
    # Total the list and divide by total to get individual stock weights
    # list_total = sum(stock_value_list)
    # stock_weights = [item / list_total for item in stock_value_list]

    return stock_list, stock_value_weights


def get_historical_returns(stocks):
    """
    use yahoo finance to create df of returns for 5 years
    :return:
    """
    # Calculate the start and end dates for the past five years
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365 * 5)).strftime('%Y-%m-%d')

    # Create an empty dictionary to store the data
    data = {}

    # Fetch stock prices for each stock
    for stock in stocks:
        ticker = yf.Ticker(stock)
        history = ticker.history(start=start_date, end=end_date)
        data[stock] = history['Close']

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)

    # Convert the index (datetimes) to timezone-unaware
    df.index = df.index.tz_localize(None)

    # Clean df by back filling NaN values
    df.bfill(inplace=True)

    # Save the DataFrame to a csv file
    df.to_csv('stock_prices.csv', index=True)

    return None


def calculate_risk(weights):
    """
    vcv_matrix
    calc variance
    calc std dev
    portfolio risk annual
    portfolio risk indiv stocks
    :return:
    """
    # import stock prices csv file
    df = pd.read_csv("stock_prices.csv")

    # Set Date as index
    df.set_index('Date', inplace=True)

    # calculate returns
    returns_df = df.pct_change(1)

    # Generate covariance matrix
    vcv_matrix = returns_df.cov()

    # Calculate variance
    var_p = np.dot(np.transpose(weights), np.dot(vcv_matrix, weights))

    # Calculate standard deviation (daily)
    sd_p = np.sqrt(var_p)

    # Calculate standard deviation annually
    sd_p_annual = sd_p * np.sqrt(250)
    print(f"Portfolio Risk- annual: {sd_p_annual}")
    print("**********************")

    # Get annual risk of individual stocks
    individual_risks = np.std(returns_df, axis=0, ddof=1) * np.sqrt(250)
    print(f"Individual Risks: \n {individual_risks}")
    print("**********************")

    # create new df total risks and add portfolio risk
    total_risks = individual_risks
    new_row = sd_p_annual
    total_risks.loc['PORTFOLIO'] = new_row

    # Add column names to total_risks
    total_risks.index.name = 'Ticker'
    total_risks.name = 'Risk'

    # save individual stock and portfolio risks
    total_risks.to_csv('risk_output.csv', index=True)

    # call plot function
    plot_risks()

    return None


def plot_risks():
    """
    risk chart or graph
    :return:
    """
    # sort values in descending order
    df = pd.read_csv('risk_output.csv')
    df_sorted = df.sort_values(by=['Risk'], ascending=False)
    midpoint_df = len(df) / 2

    # Create chart
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
    plt.ylabel('Risk', fontdict={'size': 14})
    plt.text(midpoint_df, 1, "<- Higher Risk                        Lower Risk ->", fontsize=12, color='red')
    plt.show()
