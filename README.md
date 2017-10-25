# NC Legislature Bill scrapy

Use this scrapy to obtain bill data from the [NC Legislature website](http://www.ncleg.net).

The scrapy extracts each bill's data into an object. Use [scrapy](https://github.com/scrapy/scrapy) command to out put a JSON list of bill objects.

## How to parse that sweet, raw data

1. Requires python3, scrapy, and related dependencies.
1. Install scrapy, using pip for example: `pip install scrapy`
1. Navigate into repo
1. Tell scrapy to crawl "bills" via command line instruction. Pass "session" and "chamber" options (chamber is optional, passing no param will scrape both chambers). For example scrape bills Senate bills from 2017-2018 session to a json file: `scrapy crawl <spider> -a chamber=S -a session=2017 -o <filename>.json`

## Current spiders

So far, I've simply created a spider class for each individual page of information.

* `bills` - retrieves bill info
* `membersvotes` - retrieves basic member information along with every member vote from the request session

## AutoThrottle

In order to politely preserve this public resource, please manage your autothrottle settings appropriately in `settings.py` file.

## TO-DO

* Better member scraping and find a unique numerical ID which may exist in the back-end.
* Prepare a single-file format for a universal export of bill and/or voting data.
* Get the primary sponsors from bills
* Get Bill counties data
* Get Bill statutes data

## More docs

[More documentation on extending scrapy functionality & output formats](https://doc.scrapy.org/en/latest/topics/commands.html).
