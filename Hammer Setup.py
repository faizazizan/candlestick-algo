#!/usr/bin/env python
# coding: utf-8

# In[18]:


import backtrader as bt
import pandas as pd

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.candle_count = 0

    def next(self):
        if not self.position and self.is_hammer_candle():
            self.buy()
            self.total_trades += 1
            self.candle_count = 0

        elif self.position:
            self.candle_count += 1

            if self.candle_count >= 4:
                self.sell()
                self.total_trades += 1
                self.winning_trades += 1

    def is_hammer_candle(self):
        return self.data.close[0] > self.data.open[0] and \
               (self.data.close[0] - self.data.low[0]) > 2 * (self.data.open[0] - self.data.close[0]) and \
               (self.data.high[0] - self.data.close[0]) < (self.data.close[0] - self.data.open[0])

# Fetch historical stock price data using yfinance
import yfinance as yf
data = yf.download('TSLA', start='2010-01-01', end='2022-12-31')

# Create a backtest instance
cerebro = bt.Cerebro()

# Add the data to the backtest
data = bt.feeds.PandasData(dataname=data)
cerebro.adddata(data)

# Add the strategy to the backtest
cerebro.addstrategy(MyStrategy)

# Set the initial capital
cerebro.broker.setcash(10000)

# Run the backtest
results = cerebro.run()

# Get the strategy instance
strategy = results[0]

# Calculate summary statistics
total_trades = strategy.total_trades
winning_trades = strategy.winning_trades
losing_trades = total_trades - winning_trades
win_rate = (winning_trades / total_trades) * 100

# Create summary table
summary = {
    'Total Trades': total_trades,
    'Winning Trades': winning_trades,
    'Losing Trades': losing_trades,
    'Win Rate (%)': win_rate
}
df_summary = pd.DataFrame([summary])

# Print the summary table
print(df_summary)


# In[24]:


import backtrader as bt
import pandas as pd

class BullishEngulfing(bt.Strategy):
    def __init__(self):
        self.total_trades = 0
        self.bullish_engulfing_trades = 0

    def next(self):
        if len(self) < 2:
            return

        # Check for Bullish Engulfing pattern
        if self.data.close[-2] < self.data.open[-2] and self.data.close[-1] > self.data.open[-2] and \
                self.data.open[-1] < self.data.close[-2] and self.data.close[-1] > self.data.open[-1]:
            self.buy()
            self.total_trades += 1
            self.bullish_engulfing_trades += 1

    def stop(self):
        # Print summary statistics at the end of the backtest
        win_rate = (self.bullish_engulfing_trades / self.total_trades) * 100

        summary = {
            'Total Trades': self.total_trades,
            'Bullish Engulfing Trades': self.bullish_engulfing_trades,
            'Win Rate (%)': win_rate
        }
        df_summary = pd.DataFrame([summary])
        print(df_summary)


# Fetch historical stock price data using yfinance
import yfinance as yf
data = yf.download('AAPL', start='2010-01-01', end='2022-12-31')

# Create a backtest instance
cerebro = bt.Cerebro()

# Add the data to the backtest
data = bt.feeds.PandasData(dataname=data)
cerebro.adddata(data)

# Add the strategy to the backtest
cerebro.addstrategy(BullishEngulfing)

# Set the initial capital
cerebro.broker.setcash(10000)

# Run the backtest
cerebro.run()


# In[1]:


import backtrader as bt
import pandas as pd

class HexadStrategy(bt.Strategy):
    def __init__(self):
        self.total_trades = 0
        self.profitable_trades = 0

    def next(self):
        if not self.position:
            if self.bullish_hexad():
                self.buy()

        elif self.position:
            if self.bearish_hexad():
                self.sell()
                self.profitable_trades += 1

        self.total_trades += 1

    def bullish_hexad(self):
        return self.data.close[0] > self.data.open[0] and \
               self.data.close[-1] > self.data.open[-1] and \
               self.data.close[-2] > self.data.open[-2] 

    def bearish_hexad(self):
        return self.data.close[0] < self.data.open[0] and \
               self.data.close[-1] < self.data.open[-1] and \
               self.data.close[-2] > self.data.open[-2]

    def stop(self):
        # Print summary statistics at the end of the backtest
        win_rate = (self.profitable_trades / self.total_trades) * 100

        summary = {
            'Total Trades': self.total_trades,
            'Profitable Trades': self.profitable_trades,
            'Win Rate (%)': win_rate
        }
        df_summary = pd.DataFrame([summary])
        print(df_summary)


# Fetch historical stock price data using yfinance
import yfinance as yf
data = yf.download('TSLA', start='2010-01-01', end='2022-12-31')

# Create a backtest instance
cerebro = bt.Cerebro()

# Add the data to the backtest
data = bt.feeds.PandasData(dataname=data)
cerebro.adddata(data)

# Add the strategy to the backtest
cerebro.addstrategy(HexadStrategy)

# Set the initial capital
cerebro.broker.setcash(10000)

# Run the backtest
cerebro.run()


# In[ ]:




