# NC Legislature data Scraping

Use this scrapy application to obtain bill data from the [NC Legislature website](http://www.ncleg.net).

The scrapy extracts each bill's data into an object. Use [scrapy](https://github.com/scrapy/scrapy) command to out put a JSON list of bill objects.

The objective of this project is to export this data into a more usable format for its presentation by the citizens of North Carolina. The data can also be migrated into other apps or made available for further analysis.

## How to parse that sweet, raw data

Requires python3 and scrapy.

1. Install [python3](https://www.python.org/downloads/).
1. Install scrapy, using pip for example: `pip install scrapy`.
1. Clone this repository and navigate into ncleg scraper directory: `ncleg/`.
1. Copy file `example.settings.py` to `settings.py`. Adjust Scrapy configuration according to your needs.
1. Tell scrapy to crawl "bills" via command line instruction. Pass "session" and "chamber" options (chamber is optional, passing no param will scrape both chambers). For example scrape bills Senate bills from 2017-2018 session to a json file: `scrapy crawl <spider> -a chamber=S -a session=2017 -o <filename>.json`.

## Current spiders
* `bills` - retrieves individual bill information
* `membersvotes` - retrieves each member vote from the entire session specified along with some basic member info

## AutoThrottle

In order to politely preserve this public data resource please manage your autothrottle settings appropriately in `settings.py` file. For more information read [Scrapy's documentation](https://docs.scrapy.org/en/latest/topics/autothrottle.html).

## Exporting scrapped data to MongoDB

If you want to seed a database with the data parsed by these spiders we can utilize the MongoPipeline. You will want to enable the pipeline in `settings.py`. You will also want to set the MONGO_URI and MONGO_DATABASE in the settings. Collections names will be the spider name by default.

## TO-DO and how to help

Drop by the [Code For Charlotte Community Action Nights](https://www.meetup.com/code-for-charlotte/) held weekly. Code for Charlotte is where this project originates along with [many other wonderful civic, minded projects](http://codeforcharlotte.org/projects/).

Visit the [VoterSmarterNC JIRA Tracker](https://codeforcharlotte.atlassian.net/projects/VOTE/issues) for the list of desired features. Feel free to fork and use for your own project and needs!

## More docs

[More documentation on extending scrapy functionality & output formats](https://doc.scrapy.org/en/latest/topics/commands.html).
