import operator
import math
from typing import Union, Callable, Dict
from engine.ast import *
from engine.tokens import TokenType


class Evaluator:
	def __init__(self) -> None:
		self._visitors: Dict[type, Callable] = {
			NumberNode: self.visit_NumberNode,
			VariableNode: self.visit_VariableNode,
			FunctionNode: self.visit_FunctionNode,
			ArithmeticOperationNode: self.visit_ArithmeticOperationNode,
			BitwiseOperationNode: self.visit_BitwiseOperationNode,
			BooleanOperationNode: self.visit_BooleanOperationNode,
		}

		self._math_funcs: Dict[str, Callable[[float], float]] = {
			"SIN": math.sin,
			"COS": math.cos,
			"TAN": math.tan,
			"SQRT": math.sqrt,
			"LOG": math.log,
			"ABS": abs,
		}

		self._arithmetic_ops: Dict[TokenType, Callable[[float, float], float]] = {
			TokenType.OP_PLUS: operator.add,
			TokenType.OP_MINUS: operator.sub,
			TokenType.OP_MULT: operator.mul,
			TokenType.OP_DIV: operator.truediv,
			TokenType.OP_POW: pow,
		}

		self._bitwise_ops: Dict[TokenType, Callable[[int, int], int]] = {
			TokenType.BIT_AND: operator.and_,
			TokenType.BIT_OR: operator.or_,
			TokenType.BIT_XOR: operator.xor,
			TokenType.BIT_LSHIFT: operator.lshift,
			TokenType.BIT_RSHIFT: operator.rshift,
		}

		self._boolean_ops: Dict[TokenType, Callable[[float, float], bool]] = {
			TokenType.EQUAL: lambda a, b:		a == b,
			TokenType.NOT_EQUAL: lambda a, b:	a != b,
			TokenType.LESS: lambda a, b:		a < b,
			TokenType.GREATER: lambda a, b:		a > b,
		}

		self.context: Dict[str, Union[int, float]] = {}

	def evaluate(self, node: Node, context: Dict[str, Union[int, float]] = None) -> Union[int, float]:
		self.context = context or {}

		return self._dispatch(node)

	def _dispatch(self, node: Node) -> Union[int, float]:
		visitor = self._visitors.get(type(node))

		if visitor is None:
			raise ValueError(f"No visitor found for node type: {type(node)}")

		return visitor(node)

	def visit_NumberNode(self, node: NumberNode) -> Union[int, float]:
		val = node.token.val

		return int(val) if int(val) == float(val) else float(val)

	def visit_VariableNode(self, node: VariableNode) -> Union[int, float]:
		if node.name not in self.context:
			raise NameError(f"Variable '{node.name}' not defined.")

		return self.context[node.name]

	def visit_FunctionNode(self, node: FunctionNode) -> float:
		arg_val = float(self._dispatch(node.argument))
		func = self._math_funcs.get(node.name.upper())

		if func is None:
			raise ValueError(f"Unknown function: {node.name}")

		return func(arg_val)

	def visit_ArithmeticOperationNode(self, node: ArithmeticOperationNode) -> Union[int, float]:
		left = self._dispatch(node.left_node)
		right = self._dispatch(node.right_node)

		if node.operator_token.type == TokenType.OP_DIV and right == 0:
			raise ZeroDivisionError("Division by zero")

		op_func = self._arithmetic_ops.get(node.operator_token.type)
		if op_func is None:
			raise ValueError(
				f"Invalid arithmetic operator: {node.operator_token.type}")

		return op_func(left, right)

	def visit_BitwiseOperationNode(self, node: BitwiseOperationNode) -> int:
		left = self._dispatch(node.left_node)
		right = self._dispatch(node.right_node)

		if not (isinstance(left, int) and isinstance(right, int)):
			raise ValueError("Bitwise operations only support integers")

		op_func = self._bitwise_ops.get(node.operator_token.type)
		if op_func is None:
			raise ValueError(
				f"Invalid bitwise operator: {node.operator_token.type}")

		return op_func(left, right)

	def visit_BooleanOperationNode(self, node: BooleanOperationNode) -> float:
		left = self._dispatch(node.left_node)
		right = self._dispatch(node.right_node)

		op_func = self._boolean_ops.get(node.operator_token.type)
		if op_func is None:
			raise ValueError(
				f"Invalid boolean operator: {node.operator_token.type}")

		return op_func(left, right)
