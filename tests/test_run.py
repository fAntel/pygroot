#!/usr/bin/python
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
		mock.get_token.side_effect = ["inc", "inc", "inc", "jump", "right", "inc",
			"inc", "inc", "inc", "inc", "left", "dec", "jump_back",
			"right", "out", None]
		
		self.e.run()
		
		print_.assert_called_with(chr(15))


	@patch('pygroot.print_error')
	@patch('pygroot.lex')
	def test_run_jump_back_error(self, mock, print_):
		mock.get_token.side_effect = ["inc", "jump_back"]
		
		self.e.run()
		
		print_.assert_called_with("There is no 'I'm Groot' previously than 'We are Groot'", True)


if __name__ == '__main__':
	unittest.main()
