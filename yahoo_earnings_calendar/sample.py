import datetime
import logging
import requests
from lxml import html

BASE_URL = 'https://biz.yahoo.com/research/earncal/'

# Logging config
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


class YahooEarningsCalendar(object):
    """
    This is the class for fetching earnings data from Yahoo! Finance
    """

    def earnings_on(self, date):
        """Gets earnings calendar data from Yahoo! on a specific date.
        Args:
            date: the date of earnings data to be fetched.
        Returns:
            the earnigs calendar data of date given.
        """
        date_str = date.strftime('%Y%m%d')
        logger.debug('Fetching earnings data for %s', date_str)
        dated_url = BASE_URL + date_str + '.html'
        page = requests.get(dated_url)
        tree = html.fromstring(page.content)
        symbols = tree.xpath('//tr/td[2]/a/text()')
        times_str = tree.xpath('//tr/td[3]/small/text()')[1:]
        if len(times_str) == 0:
            times_str = tree.xpath('//tr/td[4]/small/text()')
        earnings_data = []
        for i in range(len(symbols)):
            earnings_data.append({
                'symbol': symbols[i],
                'time': times_str[i],
                'date': date_str,
            })
        return earnings_data

    def earnings_between(self, from_date, to_date):
        """Gets earnings calendar data from Yahoo! in a date range.
        Args:
            from_date: the from date (inclusive).
            to_date: the to date (inclusive).
        Returns:
            the earnigs calendar data of date range.
        Raises:
            ValueError: if from_date is after to_date.
        """
        if from_date > to_date:
            raise ValueError('From-date should not be after to-date')
        earnings_data = []
        current_date = from_date
        delta = datetime.timedelta(days=1)
        while current_date <= to_date:
            earnings_data += self.earnings_on(current_date)
            current_date += delta
        return earnings_data

if __name__ == '__main__':
    day = datetime.datetime.strptime('Jun 6 2016  1:33PM', '%b %d %Y %I:%M%p')
    yec = YahooEarningsCalendar()
    print yec.earnings_on(day)
