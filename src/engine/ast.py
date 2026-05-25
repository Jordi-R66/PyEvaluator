from engine.tokens import Token


class Node:
	pass


class VariableNode(Node):
	def __init__(self, name: str):
		self.name = name


class NumberNode(Node):
	def __init__(self, token: Token) -> None:
		self.token: Token = token


class FunctionNode(Node):
	def __init__(self, name: str, argument: Node):
		self.name = name
		self.argument = argument


class OperationNode(Node):
	def __init__(self, operator_token: Token) -> None:
		self.operator_token: Token = operator_token


class BinaryOperationNode(OperationNode):
	def __init__(self, left_node: Node, operator_token: Token, right_node: Node) -> None:
		super().__init__(operator_token)
		self.left_node: Node = left_node
		self.right_node: Node = right_node


class ArithmeticOperationNode(BinaryOperationNode):
	pass


class BooleanOperationNode(BinaryOperationNode):
	pass


class BitwiseOperationNode(BinaryOperationNode):
	pass
