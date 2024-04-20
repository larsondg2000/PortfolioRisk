from typing import List
from functions import get_weights_tickers, get_historical_returns, calculate_risk


def main() -> None:
    """
    Main execution function that orchestrates the process of fetching stock tickers and weights,
    retrieving historical returns, calculating risk, and notifying the user upon completion.
    """
    # Get stock tickers and their corresponding weights
    stocks, weights = get_weights_tickers()
    stocks: List[str] = stocks
    weights: List[float] = weights

    # Retrieve historical returns for the fetched stocks
    get_historical_returns(stocks)

    # Calculate risk based on the weights of the stocks
    calculate_risk(weights)

    # Notify the user that the risk outputs have been saved
    print("Risk outputs saved to 'risk_output.csv'")


if __name__ == '__main__':
    main()
