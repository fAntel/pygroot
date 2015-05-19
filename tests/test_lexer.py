#!/usr/bin/python
import unittest
from unittest.mock import MagicMock
import pygroot

class test_lexer(unittest.TestCase):
	def setUp(self):
		self.l = pygroot.lexer()
		self.l.f = MagicMock()


	def test_lexer_simple(self):
		values = ["i am groot", "I am Groot", "I AM GROOOT", "I AM GROOT",
			"I am groot", "I am grooot", "I'm Groot", "We are Groot"]
		results = ["inc", "dec", "out", "right", "left", "inp", "jump",
			"jump_back"]
		self.l.f.readline = MagicMock(side_effect = values)

		for i in results:
			result = self.l.get_token()

			self.assertEqual(i, result)


	def test_lexer_with_whitespaces(self):
		values = [" i am groot", "I  am Groot", "I AM  GROOOT", "I AM GROOT ",
			" I  am  groot ", "	I am grooot", "I'm	 Groot", "We  are Groot	"]
		results = ["inc", "dec", "out", "right", "left", "inp", "jump",
			"jump_back"]
		self.l.f.readline = MagicMock(side_effect = values)
		for i in results:
			result = self.l.get_token()

			self.assertEqual(i, result)


	def test_lexer_none(self):
		self.l.f.readline.return_value = ''
		
		result = self.l.get_token()
		
		self.assertIsNone(result)


	def test_lexer_empty_string(self):
		values = ["\n", " ", " \n", "	", "i am groot"]
		self.l.f.readline = MagicMock(side_effect = values)
		
		result = self.l.get_token()

		self.assertEqual("inc", result)


	def test_lexer_comment_whole_string(self):
		values = ["#   ", "	#   dsds", "i am groot"]
		self.l.f.readline = MagicMock(side_effect = values)
		
		result = self.l.get_token()

		self.assertEqual("inc", result)


	def test_lexer_comment_in_string(self):
		self.l.f.readline.return_value = 'i am groot # ssds'
		
		result = self.l.get_token()
		
		self.assertEqual("inc", result)


	def test_lexer_unknown_command(self):
		self.l.f.readline.return_value = 'i are groot'

		with self.assertRaises(KeyError):
			self.l.get_token()


if __name__ == '__main__':
	unittest.main()
