#!/usr/bin/python
#
#  test_conveyor.py
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


class text_conveyor_constructor(unittest.TestCase):
	@patch('pygroot.lex')
	def test_create_full_cmds(self, mock):
		mock.get_token.side_effect = ["inc", "jump_back"]

		c = pygroot.conveyor()

		self.assertEqual(["jump", "inc", "jump_back"], c.cmds)


	@patch('pygroot.lex')
	def test_create_nested_cmds(self, mock):
		mock.get_token.side_effect = ["inc", "jump", "right",
			"jump_back", "jump_back"]

		c = pygroot.conveyor()

		self.assertEqual(
			["jump", "inc", "jump", "right", "jump_back",
				"jump_back"],
			c.cmds)



	@patch('pygroot.lex')
	def test_wrong(self, mock):
		mock.get_token.return_value = None

		with self.assertRaises(SyntaxError):
			pygroot.conveyor()


class text_conveyor_functions(unittest.TestCase):

	def setUp(self):
		self.c = pygroot.conveyor(True)


	def test_next(self):
		self.c.cmd_ptr = 0

		self.c.next()

		self.assertEqual(1, self.c.cmd_ptr)


	def test_is_end_true(self):
		self.c.cmds = ["jump", "jump_back"]
		self.c.cmd_ptr = 2

		result = self.c.is_end()

		self.assertTrue(result)


	def test_is_end_false(self):
		self.c.cmds = ["jump", "jump_back"]
		self.c.cmd_ptr = 1

		result = self.c.is_end()

		self.assertFalse(result)


	def test_get_next_jump_back(self):
		self.c.cmds = ["jump", "jump", "inc", "inc", "jump_back", "dec", "jump_back"]
		self.c.cmd_ptr = 1

		self.c.next_jump_back()

		self.assertEqual(4, self.c.cmd_ptr)


	def test_get_next_jump_back_nested(self):
		self.c.cmds = ["jump", "jump", "inc", "inc", "jump_back", "dec", "jump_back"]
		self.c.cmd_ptr = 0

		self.c.next_jump_back()

		self.assertEqual(6, self.c.cmd_ptr)


	def test_get_prev_jump(self):
		self.c.cmds = ["jump", "jump", "inc", "inc", "jump_back", "dec", "jump_back"]
		self.c.cmd_ptr = 4

		self.c.prev_jump()

		self.assertEqual(1, self.c.cmd_ptr)


	def test_get_next_jump_back_nested_outside(self):
		self.c.cmds = ["jump", "jump", "inc", "inc", "jump_back", "dec", "jump_back"]
		self.c.cmd_ptr = 6

		self.c.prev_jump()

		self.assertEqual(0, self.c.cmd_ptr)


	def test_get_next_jump_back_nested_within(self):
		self.c.cmds = ["jump", "jump", "inc", "inc", "jump_back", "dec", "jump_back"]
		self.c.cmd_ptr = 4

		self.c.prev_jump()

		self.assertEqual(1, self.c.cmd_ptr)


	def test_get_command(self):
		self.c.cmds = ["jump", "jump_back"]
		self.c.cmd_ptr = 0

		result = self.c.get_command()

		self.assertEqual("jump", result)

if __name__ == '__main__':
	unittest.main()
