import unittest
import data.jsonReader as jsonReader

class GetAdressTest(unittest.TestCase):
	def test_issue_lat_lng(self):
		self.assertIsNot(self, 1, 0)

		self.assertIsNot(self, jsonReader.getAddress(52.52689, 13.385281), 0)
		self.assertIsNot(self, jsonReader.getAddress(10000, 13.385281), 0)
		#self.assertIs(self, jsonReader.getAddress(52.52689,'a'), 0, msg='Fehler, es sollte 0 zurueckgegeben werden')
		#self.assertIs(self, jsonReader.getAddress('a','a'), 0, msg='Fehler, es sollte 0 zurueckgegeben werden')
		
		
