import unittest
import os
import json
os.system('scrapy crawl bills -a chamber=S -a number=1 -a session=2017 -o test.json')

class TestBills(unittest.TestCase):
    def testPrimarySponsorofSenateBill1(self):
        with open ('test.json') as f:
            data = json.load(f)
            os.system('rm test.json')
        self.assertEqual(data[0]['primary_sponsors'][0].encode('ascii',errors='ignore'),'Rabon')

if __name__ == '__main__':
    unittest.main()
