import scrapy
from urllib.parse import urlparse, parse_qs
from ncleg.items import Member

class NcLegMembersSpider(scrapy.Spider):
    name = "members"
    base = 'https://www.ncleg.net/'
    url = 'https://www.ncleg.net/gascripts/members/memberList.pl?sChamber=%chamber%'
    # Set the available chambers (House and Senate)
    chambers = ['house', 'senate']

    def __init__(self, chamber='', member='', *args, **kwargs):
        super(NcLegMembersSpider, self).__init__(*args, **kwargs)
        self.chamber = chamber
        self.member = member

    def start_requests(self):
        # If a chamber is specified, scrape only it. Otherwise get both!
        if self.chamber in self.chambers:
            self.chambers = [self.chamber]

        for c in self.chambers:
            yield scrapy.Request(url=self.url.replace('%chamber%',c), callback=self.parse_members, meta={'chamber':c})

    def parse_members(self, response):
        memberTable = response.xpath('/html/body/div/table/tr/td[1]/table/tr')
        for row in memberTable[1:]:
            columns = row.xpath('td')
            for column in columns[1::2]:
                item = Member()
                item['memberId'] = int(column.xpath('a[1]/@href').re('\d+')[0])
                if len(self.member) > 0 and item['memberId'] != int(self.member):
                    continue
                item['chamber'] = response.meta['chamber']
                item['district'] = int(column.xpath('a[2]/text()').re('\d+')[0])
                item['href'] = column.xpath('a[1]/@href').extract_first()
                item['member'] = column.xpath('a[1]/text()').extract_first()
                item['memberId'] = int(column.xpath('a[1]/@href').re('\d+')[0])
                item['party'] = column.xpath('text()').re('\((.*?)\)')[0]
                yield scrapy.Request(url=self.base+item['href'], callback=self.parse_member, meta={'item':item})

    def parse_member(self, response):
        item = response.meta['item']
        item['email'] = response.xpath('/html/body/div/table/tr/td[1]/table/tr[2]/td/div/table/tr[1]/td/table/tr[1]/td[2]/table/tr[4]/td/span/a/text()').extract_first()
        yield item
