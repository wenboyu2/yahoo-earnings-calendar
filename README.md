# Yahoo! Earnings Calendar Scraper
Scrapes Yahoo! Finance earnings calendar to get data for a specific date or a date range.

## Installation
### Pip
```sh
pip install yahoo_earnings_calendar
```

## Useage
```python
import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
...
date_from = datetime.datetime.strptime(
    'Jun 6 2016  10:00AM', '%b %d %Y %I:%M%p')
date_to = datetime.datetime.strptime(
    'Jun 12 2016  1:00PM', '%b %d %Y %I:%M%p')
yec = YahooEarningsCalendar()
print yec.earnings_on(date_from)
print yec.earnings_between(date_from, date_to)
# [{'date': '20160606', 'symbol': 'ABIL', 'time': 'Before Market Open'}, ...]
```

## Data attributes
- date: Integer
  - e.g., 20160606
- symbol: String
  - e.g., AAPL
- time: String
  - e.g., 'Before Market Open', 'Time Not Supplied', '02:00 am ET' etc.
