from engine.ast import *
from engine.tokens import Token, TokenType


class Parser:
	def __init__(self, tokens: list[Token]):
		self.tokens: list[Token] = tokens
		self.token_index: int = -1
		self.current_token: Token | None = None

	def next_token(self) -> Token | None:
		self.token_index += 1
		self.current_token = self.tokens[self.token_index] if self.token_index < len(
			self.tokens) else None
		return self.current_token

	def parse(self) -> Node:
		self.next_token()
		result: Node = self.parse_expression()

		if self.current_token is not None:
			raise SyntaxError(
				"Invalid syntax: unexpected token after expression.")

		return result

	def parse_expression(self) -> Node:
		result: Node = self.parse_term()

		bool_ops = (TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS, TokenType.GREATER)

		while self.current_token is not None and self.current_token.type in (TokenType.OP_PLUS, TokenType.OP_MINUS, *bool_ops):
			operator_token: Token = self.current_token
			self.next_token()
			right: Node = self.parse_term()

			OperationNodeType: type = BooleanOperationNode if operator_token.type in bool_ops else ArithmeticOperationNode

			result = OperationNodeType(result, operator_token, right)

		return result

	def parse_term(self) -> Node:
		result: Node = self.parse_power()

		while self.current_token is not None and self.current_token.type in (
				TokenType.OP_MULT, TokenType.OP_DIV, TokenType.BIT_AND,
				TokenType.BIT_OR, TokenType.BIT_XOR):

			operator_token: Token = self.current_token
			self.next_token()
			right: Node = self.parse_power()

			OpType = BitwiseOperationNode if operator_token.type in (
				TokenType.BIT_AND, TokenType.BIT_OR, TokenType.BIT_XOR) else ArithmeticOperationNode
			result = OpType(result, operator_token, right)

		return result

	def parse_factor(self) -> Node:
		result: Node

		if self.current_token is not None and self.current_token.type in (TokenType.OP_PLUS, TokenType.OP_MINUS):
			op_token: Token = self.current_token
			self.next_token()
			right: Node = self.parse_factor()
			result = ArithmeticOperationNode(NumberNode(
				Token(TokenType.NUMBER, 0)), op_token, right)

		elif self.current_token is not None and self.current_token.type == TokenType.NUMBER:
			result = NumberNode(self.current_token)
			self.next_token()

		elif self.current_token is not None and self.current_token.type == TokenType.IDENTIFIER:
			name: str = self.current_token.val
			self.next_token()

			if self.current_token is not None and self.current_token.type == TokenType.L_PAREN:
				self.next_token()
				arg: Node = self.parse_expression()
				if self.current_token is None or self.current_token.type != TokenType.R_PAREN:
					raise SyntaxError("Expected ')' after function argument")
				self.next_token()
				result = FunctionNode(name, arg)
			else:
				result = VariableNode(name)

		elif self.current_token is not None and self.current_token.type == TokenType.L_PAREN:
			self.next_token()
			result = self.parse_expression()
			if self.current_token is None or self.current_token.type != TokenType.R_PAREN:
				raise SyntaxError("Expected ')'")
			self.next_token()

		else:
			raise SyntaxError(f"Unexpected token: {self.current_token}")

		return result

	def parse_power(self) -> Node:
		result: Node = self.parse_factor()

		while self.current_token is not None and self.current_token.type == TokenType.OP_POW:
			operator_token: Token = self.current_token
			self.next_token()
			right: Node = self.parse_power()
			result = ArithmeticOperationNode(result, operator_token, right)

		return result