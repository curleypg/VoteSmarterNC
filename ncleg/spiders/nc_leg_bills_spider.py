import scrapy
from ncleg.items import Bill
import logging

class NcLegBillsSpider(scrapy.Spider):
    name = "bills"
    houseBills = 'http://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?BillID=%chamber%%num%&Session=%session%'
    billStart = 1
    # Set the available chambers (House and Senate)
    chambers = ['H','S']

    def __init__(self, chamber='', session='',*args, **kwargs):
        super(NcLegBillsSpider, self).__init__(*args, **kwargs)
        self.chamber = chamber
        self.session = session

    def start_requests(self):
        # Check if getting single chamber or both
        if self.chamber in self.chambers:
            self.chambers = [self.chamber]
        for c in self.chambers:
            # Bills are numbered predictably so increment bill number += 1
            while self.billStart > 0:
                yield scrapy.Request(url=self.houseBills.replace('%num%',str(self.billStart)).replace('%chamber%',c).replace('%session%', str(self.session)), callback=self.parse)
                self.billStart += 1
            self.billStart = 1

    def parse(self, response):
        # Return when we have incremented past the last known bill
        if len(response.xpath('//div[@id = "title"]/text()').re('Not Found')) > 0:
            self.billStart = -1
            return

        # Use Bill item to catch data
        item = Bill()
        item['number'] = response.xpath('//div[@id = "mainBody"]/table[1]/tr/td[2]/text()').re('\d+')[0]
        item['chamber'] = response.xpath('//div[@id = "mainBody"]/table[1]/tr/td[2]/text()').re('\w+')[0]
        item['session'] = response.xpath('//div[@id = "mainBody"]/div[3]/text()').extract_first()
        item['title'] = response.xpath('//div[@id = "title"]/a/text()').extract_first()

        # In 2017 member names are embedded in links
        if (self.session == '2017'):
            item['sponsors'] = response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[2]/td/a/text()').extract()
        else:
            item['sponsors'] = response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[2]/td/text()').re('(?!Primary$)\w+\.?\ ?\-?\'?\w+')


        item['keywords'] = response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[6]/td/div/text()').re('[^,]+')

        yield item
