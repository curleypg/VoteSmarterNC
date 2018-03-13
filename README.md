# NC Legislature Bill scrapy

Use this scrapy to obtain bill data from the [NC Legislature website](http://www.ncleg.net).

The scrapy extracts each bill's data into an object. Use [scrapy](https://github.com/scrapy/scrapy) command to out put a JSON list of bill objects.

## How to parse that sweet, raw data

1. Requires python3, scrapy, and related dependencies.
1. Install scrapy, using pip for example: `pip install scrapy`.
1. Navigate into repo and into ncleg scraper directory: `ncleg/`.
1. Copy file `example.settings.py` to `settings.py`. Adjust Scrapy configuration according to your needs.
1. Tell scrapy to crawl "bills" via command line instruction. Pass "session" and "chamber" options (chamber is optional, passing no param will scrape both chambers). For example scrape bills Senate bills from 2017-2018 session to a json file: `scrapy crawl <spider> -a chamber=S -a session=2017 -o <filename>.json`.

## Current spiders

So far, I've simply created a spider class for each individual page of information.

* `bills` - retrieves bill info
* `membersvotes` - retrieves basic member information along with every member vote from the request session

## AutoThrottle

In order to politely preserve this public resource, please manage your autothrottle settings appropriately in `settings.py` file.

## Exporting to MongoDB

If you want to seed a database with the data parsed by these spiders we can utilize the MongoPipeline. You will want to enable the pipeline in `settings.py`. You will also want to set the MONGO_URI and MONGO_DATABASE in the settings. Collections names will be the spider name by default.

## TO-DO

* Member scraping and better identification by unique ID rather than name (pre-2017 sessions).

## More docs

[More documentation on extending scrapy functionality & output formats](https://doc.scrapy.org/en/latest/topics/commands.html).
