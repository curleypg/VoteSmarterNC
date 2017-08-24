# NC Legislature Bill scrapy

Use this scrapy to obtain bill data from the [NC Legislature website](http://www.ncleg.net).

The scrapy extracts each bill's data into an object. Use [scrapy](https://github.com/scrapy/scrapy) command to out put a JSON list of bill objects.

## How to parse that sweet, raw data

1. Requires python3.
1. Install scrapy, using pip for example: `pip install scrapy`
1. Navigate into repo
1. Tell scrapy to crawl "bills" via command line instruction. Pass "session" and "chamber" options. For example scrape bills Senate bills from 2017-2018 session to a json file: `scrapy crawl bills -a chamber=S -a session=2017 -o <filename>.json`

## More docs

[More documentation on extending scrapy functionality & output formats](https://doc.scrapy.org/en/latest/topics/commands.html).
