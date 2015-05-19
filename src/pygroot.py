#!/usr/bin/python
#
#  pygroot.py
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

import sys
import string
import argparse
from config import NAME
from config import VERSION

lex = None

def print_error(msg, is_exit):
	print(NAME + ": ", filename, "(", lineno, "): ", msg)
	if is_exit:
		sys.exit(1)


class lexer:
	def __init__(self, filename = None):
		self.tokens = {"iamgroot": "inc", "IamGroot": "dec", "IAMGROOOT": "out",
			"IAMGROOT": "right", "Iamgroot": "left", "Iamgrooot": "inp",
			"I'mGroot": "jump", "WeareGroot": "jump_back"}
		self.lineno = 0
		self.filename = filename
		if filename is not None:
			self.f = open(filename)

	def get_token(self):
		while True:
			lexema = self.f.readline()
			self.lineno += 1
			if lexema == '':
				return None
			lexema = lexema.split('#', 2)[0]
			if ''.join(lexema.split()) != '':
				break
		token = self.tokens[''.join(lexema.split())]
		if token is None:
			raise KeyError("unknown command '" + lexema + "'")
		return token


class executor:
	def __init__(self):
		self.ptr = int()
		self.memory = [0]
		self.conveyor = None

	def inc(self):
		self.memory[self.ptr] += 1

	def dec(self):
		self.memory[self.ptr] -= 1

	def out(self):
		print(chr(self.memory[self.ptr]))

	def right(self):
		self.ptr += 1
		if self.ptr >= len(self.memory):
			self.memory.append(int())

	def left(self):
		if self.ptr > 0:
			self.ptr -= 1
		else:
			print_error("warning: program is trying to move pointer in position befor beginning of memory", False)

	def inp(self):
		self.memory[self.ptr] = ord(sys.stdin.read(1))

	def jump(self):
		if self.memory[self.ptr] == 0:
			self.conveyor.next_jump_back()

	def jump_back(self):
		if self.memory[self.ptr] != 0:
			if self.conveyor is not None:
				self.conveyor.prev_jump()
			else:
				raise SyntaxError("There is no 'I'm Groot' previously than 'We are Groot'")

	def run(self):
		try:
			token = lex.get_token()
			while token is not None:
				if token == "jump":
					self.conveyor = conveyor()
					while not self.conveyor.is_end():
						(getattr(self, self.conveyor.get_command()))()
						self.conveyor.next()
					del self.conveyor
					self.conveyor = None
				else:
					(getattr(self, token))()
				token = lex.get_token()
		except SyntaxError as e:
			print_error(str(e), True)
		except KeyError as e:
			print_error(str(e), True)
		except BaseException as e:
			print_error(str(e), True)


class conveyor:
	def __init__(self, test = False):
		# for testing
		if test == True:
			self.cmds = None
			self.cmd_ptr = None
			return
		self.cmds = ["jump"]
		self.cmd_ptr = 0
		level = 0
		token = lex.get_token()
		while token is not None:
			self.cmds.append(token)
			if token == "jump":
				level += 1
			elif token == "jump_back":
				if level > 0:
					level -= 1
				else:
					break
			token = lex.get_token()
		if token is None:
			raise SyntaxError("there is no closing 'We are Groot'")

	def next(self):
		self.cmd_ptr += 1

	def get_command(self):
		return self.cmds[self.cmd_ptr]

	def is_end(self):
		return True if self.cmd_ptr >= len(self.cmds) else False

	def next_jump_back(self):
		self.cmd_ptr += 1
		level = 0
		while self.cmds[self.cmd_ptr] != "jump_back" or level != 0:
			if self.cmds[self.cmd_ptr] == "jump":
				level += 1
			elif self.cmds[self.cmd_ptr] == "jump_back":
				level -= 1
			self.cmd_ptr += 1

	def prev_jump(self):
		level = 0
		self.cmd_ptr -= 1
		while self.cmd_ptr >= 0:
			if self.cmds[self.cmd_ptr] == "jump_back":
				level += 1
			elif self.cmds[self.cmd_ptr] == "jump":
				if level == 0:
					return
				else:
					level -= 1
			self.cmd_ptr -= 1


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog = NAME,
		description = "The Groot Programming Language interpreter",
		epilog = "Report bugs to: keldzh@gmail.com",
		formatter_class = argparse.RawDescriptionHelpFormatter)
	parser.add_argument("FILE", help = "path to the file with program on Groot")
	parser.add_argument("--version", action = "version",
		version = NAME + " " + VERSION + """
Copyright (C) 2015 Anton Kovalyov
License GPLv3: GNU GPL version 3 or later <http://www.gnu.org/licenses/gpl-3.0.html>
This program comes with ABSOLUTELY NO WARRANTY, to the extent permitted by law.
This is free software, and you are welcome to redistribute it
under certain conditions.""")
	args = parser.parse_args()
	lex = lexer(args.FILE)
	e = executor()
	e.run()
