import yfinance as yf

class StockTradingBot:
    def __init__(self, symbol, short_window, long_window, initial_cash):
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.cash = initial_cash
        self.stock_balance = 0
        self.history = []
        self.data = None  # Initialize data attribute

    def get_stock_data(self, start_date, end_date):
        self.data = yf.download(self.symbol, start=start_date, end=end_date)
        return self.data

    def calculate_sma(self, data, window):
        return data['Close'].rolling(window=window).mean()

    def buy(self, price, amount):
        total_cost = price * amount
        if self.cash >= total_cost:
            self.cash -= total_cost
            self.stock_balance += amount
            self.history.append(f"Bought {amount} shares at ${price:.2f} each")

    def sell(self, price, amount):
        if self.stock_balance >= amount:
            total_sale = price * amount
            self.cash += total_sale
            self.stock_balance -= amount
            self.history.append(f"Sold {amount} shares at ${price:.2f} each")

    def execute_strategy(self, data):
        short_sma = self.calculate_sma(data, self.short_window)
        long_sma = self.calculate_sma(data, self.long_window)

        for i in range(1, len(data)):
            if i < self.long_window:  # Skip the period before the long SMA has values
                continue
            if short_sma[i] > long_sma[i] and self.stock_balance == 0:  # Buy condition
                self.buy(data['Close'][i], 10)  # Example: Buy 10 shares
            elif short_sma[i] < long_sma[i] and self.stock_balance > 0:  # Sell condition
                self.sell(data['Close'][i], 10)  # Example: Sell 10 shares

    def run(self):
        data = self.get_stock_data("2022-01-01", "2023-01-01")  # Adjust date range as needed
        self.execute_strategy(data)
        self.display_portfolio()

    def display_portfolio(self):
        print("Portfolio Summary:")
        print(f"Cash: ${self.cash:.2f}")
        print(f"Stock Balance: {self.stock_balance} shares")
        # Ensure `data` is available via `self.data`
        if self.data is not None:
            print(f"Portfolio Value: ${(self.cash + self.stock_balance * self.data['Close'].iloc[-1]):.2f}")
        else:
            print("Data not loaded.")

if __name__ == "__main__":
    bot = StockTradingBot(symbol="AAPL", short_window=50, long_window=200, initial_cash=10000)
    bot.run()
