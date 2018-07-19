import unittest
import os
import json

class TestBills(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        os.system('scrapy crawl bills -a chamber=S -a number=100,101 -a session=2017 -o test.json')

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
        self.assertEqual(records[0]['number'], '101')
        self.assertEqual(records[1]['number'], '100')

    def testSenateChamber(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[0]['chamber'], 'Senate')
        self.assertEqual(records[1]['chamber'], 'Senate')

    def testSenateSession(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[0]['session'], '2017-2018 Session')
        self.assertEqual(records[1]['session'], '2017-2018 Session')

    def testSenateTitle(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[0]['title'], 'School Calendar Flex./Person County.')
        self.assertEqual(records[1]['title'], 'Aerial Adventure Financial Responsibility.')

    def testSenateCounties(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[0]['counties'], ['PERSON'])
        self.assertEqual(records[1]['counties'], [])

    def testSenateStatutes(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[0]['statutes'], ['115C-84.2 (Section)'])
        self.assertEqual(records[1]['statutes'], ['66 (Chapter); 66-450', ', 66-451', ', 66-452', ', 66-453 (Sections)'])

    def testSenateKeywords(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[0]['keywords'], ['BOARDS', 'CALENDAR', 'COUNTIES', 'EDUCATION', 'EDUCATION BOARDS', 'ELEMENTARY EDUCATION', 'KINDERGARTEN', 'LOCAL', 'LOCAL GOVERNMENT', 'PERSON COUNTY', 'SECONDARY EDUCATION'])
        self.assertEqual(records[1]['keywords'], ['CHAPTERED', 'COMMERCE', 'INSURANCE', 'INSURANCE', 'LIABILITY', 'LIABILITY', 'PRESENTED', 'PUBLIC', 'RATIFIED', 'RECREATION & LEISURE'])

    def testSenatePassedHouse(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertFalse(records[0]['passed_House'])
        self.assertTrue(records[1]['passed_House'])

    def testSenatePassedSenate(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertFalse(records[0]['passed_Senate'])
        self.assertTrue(records[1]['passed_Senate'])

    def testSenateIsRatified(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertFalse(records[0]['is_ratified'])
        self.assertTrue(records[1]['is_ratified'])

    def testSenateIsLaw(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertFalse(records[0]['is_law'])
        self.assertTrue(records[1]['is_law'])

    def testSenateSponsors(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[0]['sponsors'], ['Woodard'])
        self.assertEqual(records[0]['sponsors_ids'], ['379'])
        self.assertEqual(records[1]['sponsors'], ['Lee', 'Meredith', 'Ford', 'Britt'])
        self.assertEqual(records[1]['sponsors_ids'], ['387', '305', '370', '399'])

    def testSenatePrimarySponsors(self):
        with open ('test.json') as f:
            records = json.load(f)
        self.assertEqual(records[0]['primary_sponsors'], ['Woodard'])
        self.assertEqual(records[0]['primary_sponsors_ids'], ['379'])
        self.assertEqual(records[1]['primary_sponsors'], ['Lee', 'Meredith', 'Ford'])
        self.assertEqual(records[1]['primary_sponsors_ids'], ['387', '305', '370'])

if __name__ == '__main__':
    unittest.main()
