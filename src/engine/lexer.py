from typing import Any, Dict, Callable
from engine.tokens import TokenType, Token


class Lexer:
	def __init__(self, formula: str):
		self.formula: str = formula
		self.pos: int = -1
		self.current_char: str | None = None
		self.next_char()

		# Lookup table pour opérateurs simples
		self._simple_ops: Dict[str, TokenType] = {
			'+': TokenType.OP_PLUS, '-': TokenType.OP_MINUS,
			'*': TokenType.OP_MULT, '/': TokenType.OP_DIV,
			'&': TokenType.BIT_AND, '|': TokenType.BIT_OR,
			'^': TokenType.BIT_XOR, '(': TokenType.L_PAREN,
			')': TokenType.R_PAREN, '=': TokenType.EQUAL,
			'<': TokenType.LESS, '>': TokenType.GREATER,
		}

	def next_char(self):
		self.pos += 1
		self.current_char = self.formula[self.pos] if self.pos < len(
			self.formula) else None

	def peek(self) -> str | None:
		peek_pos = self.pos + 1
		return self.formula[peek_pos] if peek_pos < len(self.formula) else None

	def make_number(self) -> Token:
		num_str: str = ""
		has_dot: bool = False
		while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
			if self.current_char == '.':
				if has_dot:
					raise ValueError("Invalid number format")
				has_dot = True
			num_str += self.current_char
			self.next_char()
		return Token(TokenType.NUMBER, float(num_str) if has_dot else int(num_str))

	def make_identifier(self) -> Token:
		id_str: str = ""
		while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
			id_str += self.current_char
			self.next_char()
		return Token(TokenType.IDENTIFIER, id_str)

	def tokenize(self) -> list[Token]:
		tokens: list[Token] = []

		# Dispatch table pour les cas complexes (2 caractères)
		complex_ops: Dict[str, tuple[str, TokenType]] = {
			'!': ('=', TokenType.NOT_EQUAL),
			'<': ('<', TokenType.BIT_LSHIFT),
			'>': ('>', TokenType.BIT_RSHIFT),
			'*': ('*', TokenType.OP_POW),
		}

		while self.current_char is not None:
			char = self.current_char

			if char.isspace():
				self.next_char()
			elif char.isdigit() or char == '.':
				tokens.append(self.make_number())
			elif char.isalpha() or char == '_':
				tokens.append(self.make_identifier())
			elif char in complex_ops and self.peek() == complex_ops[char][0]:
				tokens.append(Token(complex_ops[char][1]))
				self.next_char()
				self.next_char()
			elif char in self._simple_ops:
				tokens.append(Token(self._simple_ops[char]))
				self.next_char()
			else:
				raise ValueError(f"Unknown character '{char}' at {self.pos}")

		return tokens
