from os import path, getenv
from pathlib import Path

HOME_DIR = Path.home()
DATA_DIR = Path.cwd().joinpath('data') \
  if getenv('PYTHON_DEV', False) \
  else Path.joinpath(HOME_DIR, '.go_broke')
SP500_TICKERS_FILENAME = DATA_DIR.joinpath('sp500_tickers.csv')
