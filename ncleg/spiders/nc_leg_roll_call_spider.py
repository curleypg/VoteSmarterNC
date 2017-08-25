import scrapy

class NcLegRollCallSpider(scrapy.Spider):
    name = "rollcall"
    url = 'http://www.ncleg.net/gascripts/voteHistory/RollCallVoteHistory.pl?sSession=%session%&sChamber=%chamber%'

    def __init__(self, chamber='', session='',*args, **kwargs):
        super(NcLegRollCallSpider, self).__init__(*args, **kwargs)
        self.chamber = chamber
        self.session = session

    def start_requests(self):
        yield scrapy.Request(url=self.url.replace('%chamber%',self.chamber).replace('%session%', str(self.session)), callback=self.parse)

    def parse(self, response):
        for vote in response.xpath('//div[@id="mainBody"]/table/tr'):
            yield {
                'Chamber': 'House' if self.chamber == 'H' else 'Senate',
                'RCS': vote.xpath('.//td[1]/text()').extract_first(),
                'Bill': vote.xpath('.//td[2]/a/text()').extract_first(),
                'Motion': vote.xpath('.//td[3]/text()').extract_first(),
                'Date': vote.xpath('.//td[4]/text()').extract_first(),
                'Aye': vote.xpath('.//td[5]/text()').extract_first(),
                'Nay': vote.xpath('.//td[6]/text()').extract_first(),
                'N/V': vote.xpath('.//td[7]/text()').extract_first(),
                'Exc. Abs.': vote.xpath('.//td[8]/text()').extract_first(),
                'Exc. Vote': vote.xpath('.//td[9]/text()').extract_first(),
                'Total Votes': vote.xpath('.//td[10]/text()').extract_first(),
                'Result': vote.xpath('.//td[11]/text()').extract_first()
            }
