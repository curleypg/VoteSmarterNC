import unittest
import os
import json

class TestMembersBills(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.system('scrapy crawl members -a chamber=house -a member=579 -o test.json')

    @classmethod
    def tearDownClass(self):
        os.system('rm test.json')

    def testRecordCount(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)

    def testMemberId(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['memberId'],579)

    def testChamber(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['chamber'],'house')

    def testDistrict(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['district'],107)

    def testHref(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['href'],'/gascripts/members/viewMember.pl?sChamber=house&nUserID=579')

    def testMember(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['member'],'Kelly M. Alexander, Jr.')

    def testParty(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(data[0]['party'],'D')

if __name__ == '__main__':
    unittest.main()
