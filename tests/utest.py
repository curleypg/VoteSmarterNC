import unittest
#import sys
import os
#sys.path.append('../database')
os.system('scrapy crawl bill -a chamber=s -a number=1 -a session=2017 -o test.json')

class TestStringMethods(unittest.TestCase):
    def testFirstRecord(self):
        self.assertEqual(db.getCustomerByID(str(1))[0], (1, u'Alice', u' Marcum', 270, u' Dale Jerry William'))


if __name__ == '__main__':
    unittest.main()

