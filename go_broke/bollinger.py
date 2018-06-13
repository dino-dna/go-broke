

def bollinger(df):
  pass


import os
import pandas as pd
# import matplotlib.pyplot as plt


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


def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.rolling_std(values, window = window)
    # TODO: Compute and return rolling standard deviation


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    # TODO: Compute upper_band and lower_band
    upper_band = rm + (2 * rstd)
    lower_band = rm - (2 * rstd)
    return upper_band, lower_band

def bollinger_strategy(df, rolling_mean, upper_band, lower_band, symbol):
    rolling_mean_df = pd.DataFrame(index = df.index, data=rolling_mean, columns=['Rolling Mean'])
    upper_band_df = pd.DataFrame(index = df.index, data=upper_band, columns=['Upper Band'])
    lower_band_df = pd.DataFrame(index = df.index, data=lower_band, columns=['Lower Band'])
    orders = pd.DataFrame(index = df.index, columns=['Order'])
    specific_orders = orders

    df = df.join(rolling_mean_df)
    df = df.join(upper_band_df)
    df = df.join(lower_band_df)
    #df = df.join(orders)

    row_iterator = df.iterrows()
    first_i, prev = row_iterator.next()

    short_exit_allowed = 0
    long_exit_allowed = 0
    short_entry_allowed = 1
    long_entry_allowed = 1

    for i, row in row_iterator:
        if row[symbol] > row['Lower Band'] and prev[symbol] < prev['Lower Band'] and long_entry_allowed == 1:
            #print i
            #print "LONG ENTRY - BUY"
            long_exit_allowed = 1
            long_entry_allowed = 0
            orders.ix[i] = "BUY"
            specific_orders.ix[i] = "LONG ENTRY"
        if row[symbol] > row['Rolling Mean'] and prev[symbol] < prev['Rolling Mean'] and long_exit_allowed == 1:
            #print i
            #print "LONG EXIT - SELL"
            long_exit_allowed = 0
            long_entry_allowed = 1
            orders.ix[i] = "SELL"
            specific_orders.ix[i] = "LONG EXIT"
        if row[symbol] < row['Upper Band'] and prev[symbol] > prev['Upper Band'] and short_entry_allowed == 1:
            #print i
            #print "SHORT ENTRY - SELL"
            short_exit_allowed = 1
            short_entry_allowed = 0
            orders.ix[i] = "SELL"
            specific_orders.ix[i] = "SHORT ENTRY"
        if row[symbol] < row['Rolling Mean'] and prev[symbol] > prev['Rolling Mean'] and short_exit_allowed == 1:
            #print i
            #print "SHORT EXIT - BUY"
            short_exit_allowed = 0
            short_entry_allowed = 1
            orders.ix[i] = "BUY"
            specific_orders.ix[i] = "SHORT EXIT"
        prev = row


    orders = orders.dropna()
    symbol_df = pd.DataFrame(index = df.index, columns=['Symbol'])
    symbol_df = symbol_df.fillna(symbol)
    shares_df = pd.DataFrame(index = df.index, columns=['Shares'])
    shares_df = shares_df.fillna(100)
    orders = symbol_df.join(orders, how='inner')
    orders = orders.join(shares_df, how='inner')
    #print orders

    f = open('Orders.csv', 'w')
    orders.to_csv(f, index_label='Date')
    f.close()

    specific_orders = specific_orders.dropna()
    return specific_orders

    #print "joined df"
    #print df

def test_run():
    # Read data
    dates = pd.date_range('2007-12-31', '2009-12-31')
    symbol = 'IBM'
    df = get_data([symbol], dates)

    # Compute Bollinger Bands
    # 1. Compute rolling mean
    rolling_mean = get_rolling_mean(df[symbol], window=20)

    # 2. Compute rolling standard deviation
    rolling_std = get_rolling_std(df[symbol], window=20)

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rolling_mean, rolling_std)

    df = df.drop('SPY', 1)
    orders = bollinger_strategy (df, rolling_mean, upper_band, lower_band, symbol)

    # Plot raw values, rolling mean and Bollinger Bands
    ax = df.plot(title="Bollinger Strategy", label=symbol)
    rolling_mean.plot(label='Rolling mean', ax=ax, color='yellow')
    upper_band.plot(label='Bollinger Bands', ax=ax, color='cyan')
    lower_band.plot(label='', ax=ax, color='cyan')



    row_iterator = orders.iterrows()
    for i, row in row_iterator:
        if row['Order'] == "LONG ENTRY":
            plt.axvline(i, color='green')
        elif row['Order'] == "LONG EXIT":
            plt.axvline(i, color='black')
        elif row['Order'] == "SHORT ENTRY":
            plt.axvline(i, color='red')
        elif row['Order'] == "SHORT EXIT":
            plt.axvline(i, color='black')
    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()
