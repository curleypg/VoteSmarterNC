import unittest
import os
import json

class TestMembersBills(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.system('scrapy crawl membersvotes -a chamber=house -a session=2017 -a member=906 -a bill=110 -o test.json')

    @classmethod
    def tearDownClass(self):
        os.system('rm test.json')

    def testRecordCount(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(len(data), 2)

    def testMember(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['member'], 'Rep. Adcock')

    def testHref(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['href'],'/gascripts/voteHistory/MemberVoteHistory.pl?sSession=2017&sChamber=H&nUserID=906')
        self.assertEqual(data[1]['href'],'/gascripts/voteHistory/MemberVoteHistory.pl?sSession=2017&sChamber=H&nUserID=906')

    def testMemberId(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['memberId'],'906')
        self.assertEqual(data[1]['memberId'],'906')

    def testSession(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['session'],'2017-2018 Session')
        self.assertEqual(data[1]['session'],'2017-2018 Session')

    def testBill(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['bill'],'110')
        self.assertEqual(data[1]['bill'],'110')

    def testRcs(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['rcs'],'251')
        self.assertEqual(data[1]['rcs'],'252')

    def testDistrict(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['district'],'41')
        self.assertEqual(data[1]['district'],'41')

    def testChamber(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['chamber'],'House')
        self.assertEqual(data[1]['chamber'],'House')

    def testBillTitle(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['billTitle'],'DOT/DMV Changes - Megaproject Funding.')
        self.assertEqual(data[1]['billTitle'],'DOT/DMV Changes - Megaproject Funding.')

    def testMotion(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['motion'],'A1 Beasley   Second Reading')
        self.assertEqual(data[1]['motion'],'Second Reading')

    def testDate(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['date'],'04/20/2017  3:19PM')
        self.assertEqual(data[1]['date'],'04/20/2017  3:32PM')

    def testVote(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['vote'],'Aye')
        self.assertEqual(data[1]['vote'],'Aye')

    def testAye(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['aye'],'57')
        self.assertEqual(data[1]['aye'],'65')

    def testNay(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['nay'],'58')
        self.assertEqual(data[1]['nay'],'50')

    def testNv(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['nv'],'2')
        self.assertEqual(data[1]['nv'],'2')

    def testExcabs(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['excabs'],'3')
        self.assertEqual(data[1]['excabs'],'3')

    def testExcvote(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['excvote'],'0')
        self.assertEqual(data[1]['excvote'],'0')

    def testTotalVote(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['totalvote'],'115')
        self.assertEqual(data[1]['totalvote'],'115')

    def testResult(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['result'],'FAIL')
        self.assertEqual(data[1]['result'],'PASS')

if __name__ == '__main__':
    unittest.main()
