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
            date: A datetime.date instance representing the date of earnings data to be fetched.
        Returns:
            An array of earnigs calendar data on date given. E.g.,
            [
                {
                    'date': '20160606',
                    'symbol': 'ABIL',
                    'time': 'Before Market Open'
                },
                ...
            ]
        Raises:
            TypeError: When date is not a datetime.date object.
        """
        if not isinstance(date, datetime.date):
            raise TypeError(
                'Date should be a datetime.date object')
        date_str = date.strftime('%Y%m%d')
        logger.debug('Fetching earnings data for %s', date_str)
        dated_url = BASE_URL + date_str + '.html'
        page = requests.get(dated_url)
        tree = html.fromstring(page.content)
        symbols = tree.xpath('//tr/td[2]/a/text()')
        times_str = tree.xpath('//tr/td[3]/small/text()')[1:]
        if not len(times_str):
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
            from_date: A datetime.date instance representing the from-date (inclusive).
            to_date: A datetime.date instance representing the to-date (inclusive).
        Returns:
            An array of earnigs calendar data of date range. E.g.,
            [
                {
                    'date': '20160606',
                    'symbol': 'ABIL',
                    'time': 'Before Market Open'
                },
                ...
            ]
        Raises:
            ValueError: When from_date is after to_date.
            TypeError: When either from_date or to_date is not a datetime.date object.
        """
        if from_date > to_date:
            raise ValueError(
                'From-date should not be after to-date')
        if not (isinstance(from_date, datetime.date) and
                isinstance(to_date, datetime.date)):
            raise TypeError(
                'From-date and to-date should be datetime.date objects')
        earnings_data = []
        current_date = from_date
        delta = datetime.timedelta(days=1)
        while current_date <= to_date:
            earnings_data += self.earnings_on(current_date)
            current_date += delta
        return earnings_data

if __name__ == '__main__':
    date_from = datetime.datetime.strptime(
        'Jun 6 2016  10:00AM', '%b %d %Y %I:%M%p')
    date_to = datetime.datetime.strptime(
        'Jun 12 2016  1:00PM', '%b %d %Y %I:%M%p')
    yec = YahooEarningsCalendar()
    print yec.earnings_on(date_from)
    print yec.earnings_between(date_from, date_to)
