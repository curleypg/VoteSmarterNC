import scrapy
from ncleg.items import Member

class NcLegMemberVotesSpider(scrapy.Spider):
    name = "membervotes"
    base = 'http://www.ncleg.net'
    url = 'http://www.ncleg.net/gascripts/voteHistory/MemberVoteHistory.pl?sSession=%session%&sChamber=%chamber%&nUserID=916'
    membersUrl = 'http://www.ncleg.net/gascripts/voteHistory/MemberVoteHistory.pl?sSession=%session%&sChamber=%chamber%'

    def __init__(self, chamber='', session='',*args, **kwargs):
        super(NcLegMemberVotesSpider, self).__init__(*args, **kwargs)
        self.chamber = chamber
        self.session = session

    def start_requests(self):
        yield scrapy.Request(url=self.membersUrl.replace('%chamber%',self.chamber).replace('%session%', str(self.session)), callback=self.parse)

    def parse(self, response):
        for member in response.xpath('//div[@id="mainBody"]/ul/li'):
            info = Member()
            info['member'] = member.xpath('.//a/text()').extract_first().replace('\u00a0', ' ')
            info['href'] = member.xpath('.//a/@href').extract_first()
            yield info

    def parse_vote(self, response):
        for vote in response.xpath('//div[@id="mainBody"]/table/tr'):
            motionData = vote.xpath('.//td[3]/text()').extract()
            if len(motionData) > 1:
                motion = motionData[0].strip() if len(motionData[0].strip()) > 1 else motionData[1].strip()
                motionTwo = motionData[1].strip() if motionData[1].strip() != motion else ''
            else:
                motion = motionData[0].strip()
                motionTwo = ''
            yield {
                'Chamber': 'House' if self.chamber == 'H' else 'Senate',
                'RCS': vote.xpath('.//td[1]/text()').extract_first(),
                'Bill': vote.xpath('.//td[2]/a/text()').extract_first(),
                'Motion': motion,
                'MotionTwo': motionTwo,
                'Date': vote.xpath('.//td[4]/text()').extract_first(),
                'Vote': vote.xpath('.//td[5]/text()').extract_first(),
                'Aye': vote.xpath('.//td[6]/text()').extract_first(),
                'Nay': vote.xpath('.//td[7]/text()').extract_first(),
                'N/V': vote.xpath('.//td[8]/text()').extract_first(),
                'Exc. Abs.': vote.xpath('.//td[9]/text()').extract_first(),
                'Exc. Vote': vote.xpath('.//td[10]/text()').extract_first(),
                'Total Votes': vote.xpath('.//td[11]/text()').extract_first(),
                'Result': vote.xpath('.//td[12]/text()').extract_first()
            }
