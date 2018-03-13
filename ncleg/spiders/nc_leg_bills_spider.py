import scrapy
from ncleg.items import Bill
from urllib.parse import urlparse, parse_qs

class NcLegBillsSpider(scrapy.Spider):
    # Spider name
    name = "bills"
    # Bills URL skeleton
    houseBills = 'http://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?BillID=%chamber%%num%&Session=%session%'
    # Track house and senate bills progression separately
    houseBillStart = 1
    senateBillStart = 1
    # Set the available chambers (House and Senate) for parsing
    chambers = ['H', 'S']

    def __init__(self, chamber='', session='', *args, **kwargs):
        super(NcLegBillsSpider, self).__init__(*args, **kwargs)
        self.chamber = chamber
        self.session = session

    def start_requests(self):
        # Check if parsing single chamber or both
        if self.chamber in self.chambers:
            self.chambers = [self.chamber]
        # Bills are numbered predictably so increment bill number += 1
        for c in self.chambers:
            if (c == 'H'):
                while self.houseBillStart > 0:
                    yield scrapy.Request(url=self.houseBills.replace('%num%',str(self.houseBillStart)).replace('%chamber%',c).replace('%session%', str(self.session)), callback=self.parse)
                    self.houseBillStart += 1

            if (c == 'S'):
                while self.senateBillStart > 0:
                    yield scrapy.Request(url=self.houseBills.replace('%num%',str(self.senateBillStart)).replace('%chamber%',c).replace('%session%', str(self.session)), callback=self.parse)
                    self.senateBillStart += 1

    def parse(self, response):
        # Return when we have incremented past the last known bill
        if len(response.xpath('//div[@id = "title"]/text()').re('Not Found')) > 0:
            chamber = parse_qs(urlparse(response.url).query)['BillID'][0][0]
            if (chamber == 'H'):
                self.houseBillStart = -1
            if (chamber == 'S'):
                self.senateBillStart = -1
            return

        # Use Bill Item to catch data
        item = Bill()
        item['number'] = response.xpath('//div[@id = "mainBody"]/table[1]/tr/td[2]/text()').re('\d+')[0]
        item['chamber'] = response.xpath('//div[@id = "mainBody"]/table[1]/tr/td[2]/text()').re('\w+')[0]
        item['session'] = response.xpath('//div[@id = "mainBody"]/div[3]/text()').extract_first()
        item['title'] = response.xpath('//div[@id = "title"]/a/text()').extract_first()
        item['keywords'] = response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[6]/td/div/text()').re('[^,]+')
        item['counties'] = response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[4]/td/text()').re('[^,]+')
        item['statutes'] = response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[5]/td/div/text()').re('[^,]+')

        # In 2017 member names are embedded in links
        if (self.session == '2017'):
            item['sponsors'] = response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[2]/td/a/text()').extract()
            item['primary_sponsors'] = response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[2]/td/br/preceding-sibling::a/text()').extract()
        else:
            sponsors = response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[2]/td/text()').re('(?!Primary$)\w+\.?\ ?\-?\'?\w+')
            primary = sponsors.index("Primary")
            if (primary > -1):
                item['primary_sponsors'] = sponsors[0:primary]
                del sponsors[primary]
            item['sponsors'] = sponsors
        yield item
