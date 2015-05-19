#!/usr/bin/python
#
#  test_lexer.py
#
#  Author:
#       keldzh <keldzh@gmail.com>
#
#  Copyright (c) 2015 Anton Kovalyov
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http:#www.gnu.org/licenses/>.

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
