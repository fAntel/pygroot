#!/usr/bin/python
#
#  test_executor.py
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


class text_executor(unittest.TestCase):
	def setUp(self):
		self.e = pygroot.executor()
		self.e.conveyor = pygroot.conveyor(True)

	def test_inc(self):
		befor = self.e.memory[self.e.ptr]

		self.e.inc()
		after = self.e.memory[self.e.ptr]

		self.assertEqual(befor + 1, after)


	def test_dec(self):
		befor = self.e.memory[self.e.ptr]

		self.e.dec()
		after = self.e.memory[self.e.ptr]

		self.assertEqual(befor - 1, after)


	@patch('pygroot.print', create=True)
	def test_out(self, print_):
		char = chr(self.e.memory[self.e.ptr])

		self.e.out()

		print_.assert_called_with(char)


	def test_right(self):
		befor = self.e.ptr

		self.e.right()

		self.assertEqual(befor + 1, self.e.ptr)
		self.assertEqual(0, self.e.memory[self.e.ptr])


	@patch('pygroot.print_error')
	def test_left_from_start(self, print_):
		result = 0

		self.e.left()

		self.assertEqual(result, self.e.ptr)
		print_.assert_called_once_with(
			"warning: program is trying to move pointer in position befor beginning of memory",
			False)

	def test_left(self):
		self.e.right()
		befor = self.e.ptr

		self.e.left()

		self.assertEqual(befor - 1, self.e.ptr)


	@patch('sys.stdin')
	def test_inp(self, mock):
		mock.read.return_value = "1"

		self.e.inp()

		mock.read.assert_called_once_with(1)
		self.assertEqual(ord("1"), self.e.memory[self.e.ptr])


	@patch('pygroot.conveyor.next_jump_back')
	def test_jump(self, mock):
		self.e.jump()

		mock.assert_called_once_with()


	@patch('pygroot.conveyor.next_jump_back')
	def test_do_not_jump(self, mock):
		self.e.memory[self.e.ptr] = 1

		self.e.jump()

		self.assertFalse(mock.called)


	@patch('pygroot.conveyor.prev_jump')
	def test_jump_back(self, mock):
		self.e.memory[self.e.ptr] = 1

		self.e.jump_back()

		mock.assert_called_once_with()


	@patch('pygroot.conveyor.prev_jump')
	def test_do_not_jump_back(self, mock):
		self.e.jump_back()

		self.assertFalse(mock.called)


	def test_jump_back_without_conveyor(self):
		self.e.conveyor = None
		self.e.memory[self.e.ptr] = 1


		with self.assertRaises(SyntaxError):
			self.e.jump_back()


if __name__ == '__main__':
	unittest.main()
