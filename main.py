"""
Program to calculate the risk of individual stocks and your overall portfolio risk
"""

from functions import get_weights_tickers, get_historical_returns, calculate_risk


def main():
    stocks, weights = get_weights_tickers()
    get_historical_returns(stocks)
    calculate_risk(weights)
    print("Risk outputs saved to 'risk_output.csv'")


if __name__ == '__main__':
    main()

