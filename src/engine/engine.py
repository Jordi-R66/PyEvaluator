from typing import Dict, Union
from engine.lexer import Lexer
from engine.parser import Parser
from engine.evaluator import Evaluator


class MathEngine:
    def __init__(self) -> None:
        self.evaluator = Evaluator()

    def calculate(self, formula: str, context: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        lexer = Lexer(formula)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        result = self.evaluator.evaluate(ast, context or {})

        return result
