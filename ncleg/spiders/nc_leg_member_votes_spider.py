import scrapy
from ncleg.items import Member, MemberVotes

class NcLegMemberVotesSpider(scrapy.Spider):
    name = "membervotes"
    base = 'http://www.ncleg.net/'
    url = 'http://www.ncleg.net/gascripts/voteHistory/MemberVoteHistory.pl?sSession=%session%&sChamber=%chamber%'

    def __init__(self, chamber='', session='',*args, **kwargs):
        super(NcLegMemberVotesSpider, self).__init__(*args, **kwargs)
        self.chamber = chamber
        self.session = session

    def start_requests(self):
        yield scrapy.Request(url=self.url.replace('%chamber%',self.chamber).replace('%session%', str(self.session)), callback=self.parse_members)

    def parse_members(self, response):
        for member in response.xpath('//div[@id="mainBody"]/ul/li'):
            info = MemberVotes()
            info['member'] = member.xpath('.//a/text()').extract_first().replace('\u00a0', ' ')
            href = member.xpath('.//a/@href').extract_first()
            info['href'] = href
            yield scrapy.Request(url=self.base+href, callback=self.parse_vote, meta={'item':info})

    def parse_vote(self, response):
        info = response.meta['item']
        self.logger.info(info)
        for vote in response.xpath('//div[@id="mainBody"]/table/tr'):
            motionData = vote.xpath('.//td[3]/text()').extract()
            if len(motionData) > 1:
                motion = motionData[0].strip() if len(motionData[0].strip()) > 1 else motionData[1].strip()
                motionTwo = motionData[1].strip() if motionData[1].strip() != motion else ''
            else:
                motion = motionData[0].strip()
                motionTwo = ''
            info['chamber'] = 'House' if self.chamber == 'H' else 'Senate'
            info['rcs'] = vote.xpath('.//td[1]/text()').extract_first()
            info['bill'] = vote.xpath('.//td[2]/a/text()').extract_first()
            info['motion'] = motion
            info['motiontwo'] = motionTwo
            info['date'] = vote.xpath('.//td[4]/text()').extract_first()
            info['vote'] = vote.xpath('.//td[5]/text()').extract_first()
            info['aye'] = vote.xpath('.//td[6]/text()').extract_first()
            info['nay'] = vote.xpath('.//td[7]/text()').extract_first()
            info['nv'] = vote.xpath('.//td[8]/text()').extract_first()
            info['excabs'] = vote.xpath('.//td[9]/text()').extract_first()
            info['excvote'] = vote.xpath('.//td[10]/text()').extract_first()
            info['totalvote'] = vote.xpath('.//td[11]/text()').extract_first()
            info['result'] = vote.xpath('.//td[12]/text()').extract_first()
            yield info
