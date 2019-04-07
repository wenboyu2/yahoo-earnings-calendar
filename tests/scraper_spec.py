from mamba import description, context, it
from expects import expect, equal
from mockito import when, mock, unstub, ANY, verify
import datetime

from yahoo_earnings_calendar import YahooEarningsCalendar

BASE_URL = 'https://finance.yahoo.com/calendar/earnings'
BASE_STOCK_URL = 'https://finance.yahoo.com/quote'

with description('YahooEarningsCalendar') as self:
    with before.each:
        self.yec = YahooEarningsCalendar()
        self.symbol = 'yo'

    with description('get_next_earnings_date') as self:
        with it('should get data with correct URL'):
            data = {
                'context': {
                    'dispatcher': {
                        'stores': {
                            'QuoteSummaryStore': {
                                'calendarEvents': {
                                    'earnings': {
                                        'earningsDate': [
                                            {
                                                'raw': 0
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            }

            expected_url = '{0}/{1}'.format(BASE_STOCK_URL, self.symbol)
            when(self.yec)._get_data_dict(expected_url).thenReturn(data)
            self.yec.get_next_earnings_date(self.symbol)

            verify(self.yec)._get_data_dict(expected_url)

        with it('should return the next earnings date'):
            expected_date = 321
            data = {
                'context': {
                    'dispatcher': {
                        'stores': {
                            'QuoteSummaryStore': {
                                'calendarEvents': {
                                    'earnings': {
                                        'earningsDate': [
                                            {
                                                'raw': expected_date
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            }

            when(self.yec)._get_data_dict(ANY(str)).thenReturn(data)

            expect(self.yec.get_next_earnings_date(
                self.symbol)).to(equal(expected_date))

    with description('earnings_on') as self:
        with it('should get data with correct URL'):
            date = datetime.datetime.strptime(
                'May 5 2017  10:00AM', '%b %d %Y %I:%M%p')
            data = {
                'context': {
                    'dispatcher': {
                        'stores': {
                            'ScreenerCriteriaStore': {
                                'meta': {
                                    'total': 50
                                }
                            },
                            'ScreenerResultsStore': {
                                'results': {
                                    'rows': []
                                }
                            }
                        }
                    }
                }
            }
            expected_url = '{0}?day={1}&offset=0&size=100'.format(
                BASE_URL, '2017-05-05')
            when(self.yec)._get_data_dict(expected_url).thenReturn(data)

            self.yec.earnings_on(date)

            verify(self.yec)._get_data_dict(expected_url)

        with it('should return earnings on date with less than 100 earnings'):
            date = datetime.datetime.strptime(
                'May 5 2017  10:00AM', '%b %d %Y %I:%M%p')
            expected_data = ['hi']
            data = {
                'context': {
                    'dispatcher': {
                        'stores': {
                            'ScreenerCriteriaStore': {
                                'meta': {
                                    'total': 90
                                }
                            },
                            'ScreenerResultsStore': {
                                'results': {
                                    'rows': expected_data
                                }
                            }
                        }
                    }
                }
            }
            when(self.yec)._get_data_dict(ANY(str)).thenReturn(data)

            self.yec.earnings_on(date)

            expect(self.yec.earnings_on(date)).to(equal(expected_data))

        with it('should return earnings on date with more than 100 earnings'):
            date = datetime.datetime.strptime(
                'May 5 2017  10:00AM', '%b %d %Y %I:%M%p')
            earnings1 = [1]
            earnings2 = [2]
            data1 = {
                'context': {
                    'dispatcher': {
                        'stores': {
                            'ScreenerCriteriaStore': {
                                'meta': {
                                    'total': 131
                                }
                            },
                            'ScreenerResultsStore': {
                                'results': {
                                    'rows': earnings1
                                }
                            }
                        }
                    }
                }
            }
            data2 = {
                'context': {
                    'dispatcher': {
                        'stores': {
                            'ScreenerCriteriaStore': {
                                'meta': {
                                    'total': 131
                                }
                            },
                            'ScreenerResultsStore': {
                                'results': {
                                    'rows': earnings2
                                }
                            }
                        }
                    }
                }
            }
            when(self.yec)._get_data_dict('{0}?day={1}&offset=0&size=100'.format(
                BASE_URL, '2017-05-05')).thenReturn(data1)
            when(self.yec)._get_data_dict('{0}?day={1}&offset=100&size=100'.format(
                BASE_URL, '2017-05-05')).thenReturn(data2)

            self.yec.earnings_on(date)

            expect(self.yec.earnings_on(date)).to(equal(earnings1 + earnings2))

    with description('earnings_between') as self:
        with it('should return all earnings between start and end date'):
            start_date = datetime.datetime.strptime(
                'May 5 2017  10:00AM', '%b %d %Y %I:%M%p')
            end_date = datetime.datetime.strptime(
                'May 7 2017  10:00AM', '%b %d %Y %I:%M%p')
            expected_data = [1, 2, 3]

            when(self.yec).earnings_on(ANY).thenReturn(
                [1]).thenReturn([2]).thenReturn([3])

            expect(self.yec.earnings_between(start_date, end_date)).to(
                equal(expected_data))
