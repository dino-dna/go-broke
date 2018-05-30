import go_broke.aquisition as aq
from datetime import datetime
import time
import logging
logging.basicConfig()


df = aq.fetch_df('SPY', datetime.utcnow(), exchange='NYSEARCA')
for symbol in aq.get_constituents()['Symbol']:
    aq.fetch_df(symbol, datetime.utcnow(), exchange='NYSE')
    time.sleep(0.1)
