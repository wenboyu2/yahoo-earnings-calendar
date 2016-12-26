try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
  name='yahoo_earnings_calendar',
  packages=['yahoo_earnings_calendar'],
  install_requires=[
      'lxml',
      'requests'
  ],
  version='0.1',
  description='Scrapes data from Yahoo! Finane earnings calendar',
  author='Wenbo Yu',
  author_email='wenboyu2@gmail.com',
  url='https://github.com/wenboyu2/yahoo-earnings-calendar',
  download_url='https://github.com/wenboyu2/yahoo-earnings-calendar/tarball/0.1',
  keywords=['stock', 'earnings', 'yahoo', 'scrape', 'finance'],
  classifiers=[],
)
