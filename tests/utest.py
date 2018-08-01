import unittest
import os
import json

class TestBills(unittest.TestCase):
    hundred = 1
    oneohone = 0

    @classmethod
    def setUpClass(self):
        os.system('scrapy crawl bills -a chamber=S -a number=100,101 -a session=2017 -o test.json')

    def setUp(self):
        with open ('test.json') as f:
            data = json.load(f)
        if data[0]['number'] == '100':
            self.hundred = 0
            self.oneohone = 1
        else:
            self.hundred = 1
            self.oneohone = 0

    @classmethod
    def tearDownClass(self):
        os.system('rm test.json')

    def testRecordCount(self):
        with open ('test.json') as f:
            data = json.load(f)
        self.assertEqual(len(data), 2)

    def testSenateBillNumber(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[self.oneohone]['number'], '101')
        self.assertEqual(records[self.hundred]['number'], '100')

    def testSenateChamber(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[self.oneohone]['chamber'], 'Senate')
        self.assertEqual(records[self.hundred]['chamber'], 'Senate')

    def testSenateSession(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[self.oneohone]['session'], '2017-2018 Session')
        self.assertEqual(records[self.oneohone]['session_id'], '2017')
        self.assertEqual(records[self.hundred]['session'], '2017-2018 Session')
        self.assertEqual(records[self.hundred]['session_id'], '2017')

    def testSenateTitle(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[self.oneohone]['title'], 'School Calendar Flex./Person County.')
        self.assertEqual(records[self.hundred]['title'], 'Aerial Adventure Financial Responsibility.')

    def testSenateCounties(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[self.oneohone]['counties'], ['PERSON'])
        self.assertEqual(records[self.hundred]['counties'], [])

    def testSenateStatutes(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[self.oneohone]['statutes'], '115C-84.2 (Sections)')
        self.assertEqual(records[self.hundred]['statutes'], '66 (Chapters); 66-450, 66-451, 66-452, 66-453 (Sections)')

    def testSenateKeywords(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[self.oneohone]['keywords'], ['BOARDS', 'CALENDAR', 'COUNTIES', 'EDUCATION', 'EDUCATION BOARDS', 'ELEMENTARY EDUCATION', 'KINDERGARTEN', 'LOCAL', 'LOCAL GOVERNMENT', 'SECONDARY EDUCATION', 'PERSON COUNTY'])
        self.assertEqual(records[self.hundred]['keywords'], ['COMMERCE', 'INSURANCE', 'INSURANCE', 'LIABILITY', 'PRESENTED', 'PUBLIC', 'RATIFIED', 'RECREATION & LEISURE', 'LIABILITY', 'CHAPTERED'])

    def testSenatePassedHouse(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertFalse(records[self.oneohone]['passed_House'])
        self.assertTrue(records[self.hundred]['passed_House'])

    def testSenatePassedSenate(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertFalse(records[self.oneohone]['passed_Senate'])
        self.assertTrue(records[self.hundred]['passed_Senate'])

    def testSenateIsRatified(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertFalse(records[self.oneohone]['is_ratified'])
        self.assertTrue(records[self.hundred]['is_ratified'])

    def testSenateIsLaw(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertFalse(records[self.oneohone]['is_law'])
        self.assertTrue(records[self.hundred]['is_law'])

    def testSenateSponsors(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[self.oneohone]['sponsors'], ['Woodard'])
        self.assertEqual(records[self.oneohone]['sponsors_ids'], ['379'])
        self.assertEqual(records[self.hundred]['sponsors'], ['Lee', 'Meredith', 'Ford', 'Britt'])
        self.assertEqual(records[self.hundred]['sponsors_ids'], ['387', '305', '370', '399'])

    def testSenatePrimarySponsors(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[self.oneohone]['primary_sponsors'], ['Woodard'])
        self.assertEqual(records[self.oneohone]['primary_sponsors_ids'], ['379'])
        self.assertEqual(records[self.hundred]['primary_sponsors'], ['Lee', 'Meredith', 'Ford'])
        self.assertEqual(records[self.hundred]['primary_sponsors_ids'], ['387', '305', '370'])

if __name__ == '__main__':
    unittest.main()
