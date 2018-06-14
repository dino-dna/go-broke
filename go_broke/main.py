import go_broke.aquisition as aq
import data_formatter
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
    input, label = data_formatter.format_attributes(df['Close'], 30, 3)
    # Split data into training and test set. Allow for the possilbity that the test set is 0 length
    # Normilize the dats
    # Do ML
    #df = df.rename(columns={'Close':'SPY'})
    bol.bollinger(df)


if __name__ == '__main__':
    main()
