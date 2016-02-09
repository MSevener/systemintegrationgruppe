import unittest
import data.jsonReader as jsonReader

class GetAirportNameTest(unittest.TestCase):
	def test_id_insert(self):
		self.assertIs(jsonReader.getAirportName('blabla'), 0, msg=None)
