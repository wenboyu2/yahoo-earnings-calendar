# Yahoo! Earnings Calendar Scraper
Scrapes Yahoo! Finance earnings calendar to get data for a specific date or a date range.

## Installation
### Manual
```sh
cd yahoo_earnings_calendar
python setup.py install
pip install -r requirements.txt
```
### Pip
coming soon

## Useage
```python
from yahoo_earnings_calendar import YahooEarningsCalendar
...
day = datetime.datetime.strptime('Jun 6 2016  1:33PM', '%b %d %Y %I:%M%p')
yec = YahooEarningsCalendar()
print yec.earnings_on(day)
# [{'date': '20160606', 'symbol': 'ABIL', 'time': 'Before Market Open'}, ...]
```
