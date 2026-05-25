from typing import Any
from enum import Enum


class TokenType(Enum):
	NUMBER = 1

	OP_PLUS = 2
	OP_MINUS = 3
	OP_MULT = 4
	OP_DIV = 5
	OP_POW = 6

	BIT_AND = 7
	BIT_OR = 8
	BIT_XOR = 9
	BIT_LSHIFT = 10
	BIT_RSHIFT = 11

	EQUAL = 12
	NOT_EQUAL = 12
	LESS = 14
	GREATER = 15

	L_PAREN = 16
	R_PAREN = 17

	IDENTIFIER = 18


class Token:
	def __init__(self, type_: TokenType, val: Any | None = None):
		self.type: TokenType = type_
		self.val: Any | None = val

	def __repr__(self):
		return f"[{self.type}: {self.val}]"
