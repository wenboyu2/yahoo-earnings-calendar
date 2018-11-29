try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='yahoo_earnings_calendar',
    packages=['yahoo_earnings_calendar'],
    install_requires=[
        'requests'
    ],
    version='0.4.0',
    description='Scrapes data from Yahoo! Finance earnings calendar',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Wenbo Yu',
    author_email='wenboyu2@gmail.com',
    url='https://github.com/wenboyu2/yahoo-earnings-calendar',
    keywords=['stock', 'earnings', 'yahoo', 'scrape', 'finance'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
