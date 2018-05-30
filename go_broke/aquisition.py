from os import path, makedirs
from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
from go_broke.constants import DATA_DIR, SP500_TICKERS_FILENAME
from pathlib import Path
import pandas as pd
from threading import Thread
import logging

LOGGER = logging.getLogger(__file__)

def ticker_filename(ticker, start_date, period='1Y'):
  stamp = f'{start_date.day}_{start_date.month}_{start_date.year}_{str(period)}'
  return Path.joinpath(DATA_DIR, 'stock_data', f'{ticker}_{stamp}.csv')


def get_constituents():
  return pd.read_csv(SP500_TICKERS_FILENAME)

def fetch_df(ticker, start_date, exchange='NYSE', refresh=False):
  filename = ticker_filename(ticker, start_date)
  if not Path.exists(filename.parent):
    makedirs(filename.parent)
  if not Path.exists(filename):
    param = {
        'q': ticker, # Stock symbol (ex: "AAPL")
        'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
        'x': exchange, # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': "1Y" # Period (Ex: "1Y" = 1 year)
    }
    df = get_price_data(param)
    if df.empty:
      if exchange == 'NYSE':
        return fetch_df(ticker, start_date, exchange='NASDAQ')
      # raise Exception(f'no data found for ticker symbol {ticker} on {exchange}')
      LOGGER.error(f'no data found for ticker symbol {ticker} on {exchange}')
    df.to_csv(filename)
    return df
  else:
    return pd.read_csv(filename)
