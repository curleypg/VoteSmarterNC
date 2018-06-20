import scrapy
from ncleg.items import Bill
from urllib.parse import urlparse, parse_qs

class NcLegBillsSpider(scrapy.Spider):
    # Spider name
    name = "bills"
    # Bills URL skeleton
    houseBills = 'https://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?BillID=%chamber%%num%&Session=%session%'
    # Track house and senate bills progression separately
    houseBillStart = 1
    senateBillStart = 1
    # Set the available chambers (House and Senate) for parsing
    chambers = ['H', 'S']

    def __init__(self, chamber='', session='', number='', *args, **kwargs):
        super(NcLegBillsSpider, self).__init__(*args, **kwargs)
        self.chamber = chamber
        self.session = session
        self.number = number

    def start_requests(self):
        # Check if parsing single chamber or both
        if self.chamber in self.chambers:
            self.chambers = [self.chamber]

        # Remove all whitespace in number parameter then split commas into array
        self.number = self.number.replace(" ", "")
        num_arr = self.number.split(",")

        # Bills are numbered predictably so increment bill number += 1
        for c in self.chambers:
            if (c == 'H' and self.number == ''):
                while self.houseBillStart > 0:
                    yield scrapy.Request(url=self.houseBills.replace('%num%',str(self.houseBillStart)).replace('%chamber%',c).replace('%session%', str(self.session)), callback=self.parse)
                    self.houseBillStart += 1

            elif (c == 'H'):
                for i in range(len(num_arr)):
                    yield scrapy.Request(url=self.houseBills.replace('%num%',str(num_arr[i])).replace('%chamber%',c).replace('%session%', str(self.session)), callback=self.parse)

            if (c == 'S' and self.number == ''):
                while self.senateBillStart > 0:
                    yield scrapy.Request(url=self.houseBills.replace('%num%',str(self.senateBillStart)).replace('%chamber%',c).replace('%session%', str(self.session)), callback=self.parse)
                    self.senateBillStart += 1

            elif (c == 'S'):
                for i in range(len(num_arr)):
                    yield scrapy.Request(url=self.houseBills.replace('%num%',str(num_arr[i])).replace('%chamber%',c).replace('%session%', str(self.session)), callback=self.parse)

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
        item['number'] = response.xpath('/html/body/div/table/tr/td/table/tr/td[2]').re('\d+')[1]
        item['chamber'] = response.xpath('/html/body/div/table/tr/td/table/tr/td[2]/text()').re('\w+')[0]
        item['session'] = response.css('.titleSub::text').extract_first()
        item['title'] = response.xpath('//div[@id = "title"]/a/text()').extract_first()
        item['counties'] = response.xpath('/html/body/div/table/tr/td[1]/table[2]/tr/td[3]/table/tr[4]/td/text()').re('[^,]+')
        item['statutes'] = response.xpath('/html/body/div/table/tr/td[1]/table[2]/tr/td[3]/table/tr[5]/td/div/text()').re('[^\n][^,]+')
        keywords = response.xpath('/html/body/div/table/tr/td[1]/table[2]/tr/td[3]/table/tr[6]/td/div/text()').extract_first().split(', ')
        item['keywords'] = keywords
        item['passed_House'] = False
        item['passed_Senate'] = False

        # This will loop through all possible xpaths in the detailed table, and will stop
        # if empty list is returned
        i = 3
        while (response.xpath('/html/body/div/table/tr/td[1]/center/table/tr[' + str(i) + ']/td[3]/text()').extract()):
            v = response.xpath('/html/body/div/table/tr/td[1]/center/table/tr[' + str(i) + ']/td[3]/text()').extract()
            if ('Passed 3rd Reading' in v[0] and 'House' in response.xpath('/html/body/div/table/tr/td[1]/center/table/tr[' + str(i) + ']/td[2]/text()').extract()[0]):
                item['passed_House'] = True
            if ('Passed 3rd Reading' in v[0] and 'Senate' in response.xpath('/html/body/div/table/tr/td[1]/center/table/tr[' + str(i) + ']/td[2]/text()').extract()[0]):
                item['passed_Senate'] = True
            i = i + 1


        # Check to see if bill had been ratified. This info is available in bill keywords
        item['is_ratified'] = self.isRatified(keywords)

        # Check to see if bill had been ratified and/or is law
        d_arr = response.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/table/tr//td[1]//a/text()').extract()
        item['is_law'] = self.isLaw(d_arr)

        # In 2017 member names are embedded in links
        if (self.session == '2017'):
            item['sponsors'] = response.xpath('/html/body/div/table/tr/td[1]/table[2]/tr/td[3]/table/tr[2]/td/a/text()').re('[^,]+')
            item['sponsors_ids'] = response.xpath('/html/body/div/table/tr/td[1]/table[2]/tr/td[3]/table/tr[2]/td/a/@href').re('\d+')
            item['primary_sponsors'] = response.xpath('/html/body/div/table/tr/td[1]/table[2]/tr/td[3]/table/tr[2]/td/br/preceding-sibling::a/text()').extract()
            item['primary_sponsors_ids'] = response.xpath('/html/body/div/table/tr/td[1]/table[2]/tr/td[3]/table/tr[2]/td/br/preceding-sibling::a/@href').re('\d+')
        else:
            sponsors = response.xpath('/html/body/div/table/tr/td[1]/table[2]/tr/td[3]/table/tr[2]/td/text()').re('(?!Primary$)\w+\.?\ ?\-?\'?\w+')
            primary = sponsors.index("Primary")
            if (primary > -1):
                item['primary_sponsors'] = sponsors[0:primary]
                del sponsors[primary]
            item['sponsors'] = sponsors
        yield item

    def isRatified(self, arr):
        if "RATIFIED" in arr:
            return True
        return False

    def isLaw(self, arr):
        for i in range(len(arr)):
            if "Law" in arr[i]:
                return True
        return False
