import scrapy
from urllib.parse import urlparse, parse_qs
from ncleg.items import Member, MemberVotes

class NcLegMemberVotesSpider(scrapy.Spider):
    name = "membersvotes"
    base = 'https://www.ncleg.net/'
    url = 'https://www.ncleg.net/gascripts/voteHistory/MemberVoteHistory.pl?sSession=%session%&sChamber=%chamber%'
    urlMember = 'https://www.ncleg.net/gascripts/voteHistory/MemberVoteHistory.pl?sSession=%session%&sChamber=%chamber%&nUserID=%member%'
    # Set the available chambers (House and Senate)
    chambers = ['H','S']

    def __init__(self, bill='', chamber='', member='', session='',*args, **kwargs):
        super(NcLegMemberVotesSpider, self).__init__(*args, **kwargs)
        self.bill = bill
        self.chamber = chamber
        self.member = member
        self.session = session

    def start_requests(self):
        # If a chamber is specified, scrape only it. Otherwise get both!
        if self.chamber in self.chambers:
            self.chambers = [self.chamber]
        for c in self.chambers:
            self.chamber = c
            yield scrapy.Request(url=self.url.replace('%chamber%',self.chamber).replace('%session%', str(self.session)), callback=self.parse_members)

    def parse_members(self, response):
        # Grab member data on their individual Roll Call votes
        for member in response.xpath('/html/body/div/table/tr/td/ul/li'):
            session = self.session
            info = MemberVotes()
            info['member'] = member.xpath('.//a/text()').extract_first().replace('\u00a0', ' ')
            href = member.xpath('.//a/@href').extract_first()
            info['href'] = href
            info['memberId'] = parse_qs(urlparse(href).query)['nUserID'][0]
            if len(self.member) == 0 or self.member == info['memberId']:
                yield scrapy.Request(url=self.base+href, callback=self.parse_vote, meta={'item':info})
            else:
                continue

    def parse_vote(self, response):
        # Grab the item from meta
        info = response.meta['item']
        info['session'] = response.css('.titleSub::text').extract_first()
        voteTable = response.xpath('/html/body/div/table/tr/td[1]/table/tr')
        # Skip the first table row of header information
        for vote in voteTable[1:]:
            info['bill'] = vote.xpath('td[2]/a/text()').re_first('\d+')
            if len(self.bill) > 0 and info['bill'] != self.bill:
                continue
            info['rcs'] = vote.xpath('td[1]/text()').extract_first()
            info['district'] = response.xpath('//div[@id="title"]/text()').re_first('\d+')
            # Get the bill motion
            motionData = vote.xpath('td[3]/text()').extract()
            if len(motionData) > 1:
                billTitle = motionData[0].strip() if len(motionData[0].strip()) > 1 else motionData[1].strip()
                motion = motionData[1].strip() if motionData[1].strip() != billTitle else ''
            else:
                billTitle = motionData[0].strip()
                motion = ''
            info['chamber'] = 'House' if self.chamber == 'S' else 'Senate'
            # Check the bill ID
            info['billTitle'] = billTitle
            info['motion'] = motion
            info['date'] = vote.xpath('td[4]/text()').extract_first()
            info['vote'] = vote.xpath('td[5]/text()').extract_first()
            info['aye'] = vote.xpath('td[6]/text()').extract_first()
            info['nay'] = vote.xpath('td[7]/text()').extract_first()
            info['nv'] = vote.xpath('td[8]/text()').extract_first()
            info['excabs'] = vote.xpath('td[9]/text()').extract_first()
            info['excvote'] = vote.xpath('td[10]/text()').extract_first()
            info['totalvote'] = vote.xpath('td[11]/text()').extract_first()
            info['result'] = vote.xpath('td[12]/text()').extract_first()

            yield info
