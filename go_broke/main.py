import go_broke.aquisition as aq
from datetime import datetime
import time
import logging
import bollinger as bol
logging.basicConfig()

LOGGER = logging.getLogger(__file__)


def main():
    # LOGGER.info('weeee')
    # df = aq.fetch_df('SPY', datetime.utcnow(), exchange='NYSEARCA')
    # for symbol in aq.get_constituents()['Symbol']:
    #     aq.fetch_df(symbol, datetime.utcnow(), exchange='NYSE')
    #     time.sleep(0.1)
    df = aq.fetch_df('SPY', exchange='NYSEARCA')

    #df = df.rename(columns={'Close':'SPY'})
    bol.bollinger(df)


if __name__ == '__main__':
    main()
