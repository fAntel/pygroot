#!/usr/bin/python
#
#  test_run.py
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
from unittest.mock import patch
import pygroot


class text_run(unittest.TestCase):
	def setUp(self):
		self.e = pygroot.executor()


	@patch('pygroot.print', create=True)
	@patch('pygroot.lex')
	def test_simple_run(self, mock, print_):
		mock.get_token.side_effect = ["inc", "inc", "inc", "out", None]

		self.e.run()

		print_.assert_called_with(chr(3))


	@patch('pygroot.print', create=True)
	@patch('pygroot.lex')
	def test_run_with_jump(self, mock, print_):
		mock.get_token.side_effect = [
			"inc", "inc", "inc", "jump", "right", "inc",
			"inc", "inc", "inc", "inc", "left", "dec",
			"jump_back", "right", "out", None]

		self.e.run()

		print_.assert_called_with(chr(15))


	@patch('pygroot.print_error')
	@patch('pygroot.lex')
	def test_run_jump_back_error(self, mock, print_):
		mock.get_token.side_effect = ["inc", "jump_back"]

		self.e.run()

		print_.assert_called_with(
			"There is no 'I'm Groot' previously than 'We are Groot'",
			True)


if __name__ == '__main__':
	unittest.main()
