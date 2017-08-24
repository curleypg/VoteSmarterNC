import scrapy

class NcLegBillSpider(scrapy.Spider):
    name = "bills"
    houseBills = 'http://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?BillID=%chamber%%num%&Session=%session%'
    billStart = 1

    def __init__(self, chamber='', session='',*args, **kwargs):
        super(NcLegBillSpider, self).__init__(*args, **kwargs)
        self.chamber = chamber
        self.session = session

    def start_requests(self):
        while self.billStart > 0:
            yield scrapy.Request(url=self.houseBills.replace('%num%',str(self.billStart)).replace('%chamber%',self.chamber).replace('%session%', str(self.session)), callback=self.parse)
            self.billStart += 1

    def parse(self, response):
        if len(response.xpath('//div[@id = "title"]/text()').re('Not Found')) > 0:
            self.billStart = -1
            return

        yield {
            'number': response.xpath('//div[@id = "mainBody"]/table[1]/tr/td[2]/text()').re('\d+')[0],
            'chamberOrigin': response.xpath('//div[@id = "mainBody"]/table[1]/tr/td[2]/text()').re('\w+')[0],
            'session': response.xpath('//div[@id = "mainBody"]/div[3]/text()').extract_first(),
            'title': response.xpath('//div[@id = "title"]/a/text()').extract_first(),
            'sponsors': response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[2]/td/a/text()').extract(),
            'keywords': response.xpath('//div[@id = "mainBody"]/table[2]/tr/td[3]/table/tr[6]/td/div/text()').extract_first(),
        }
