from math import pi
from engine.engine import MathEngine


def test_engine():
	engine = MathEngine()

	# Contexte pour les tests
	context = {"x": 2, "y": 3, "z": 4}

	# Liste de tests : (Formule, Résultat attendu)
	tests = [
		# Associativité à droite (2**(3**2) = 2**9 = 512)
		("x ** y ** 2", 512),

		# Parenthèses forçant la gauche ((2**3)**2 = 8**2 = 64)
		("(x ** y) ** 2", 64),

		# Priorité : Puissance avant multiplication (2 * 3**2 = 2 * 9 = 18)
		("x * y ** 2", 18),

		# Priorité : Multiplication avant addition (2 + 3 * 4**2 = 2 + 3 * 16 = 50)
		("x + y * z ** 2", 50),

		# Mélange complexe
		("2 ** (3 + 1) * 5", 80),  # 2**4 * 5 = 16 * 5 = 80
		("z ** x ** x", 256),    # 4**(2**2) = 4**4 = 256
	]

	print("--- Test des priorités et associativités ---")
	for formula, expected in tests:
		result = engine.calculate(formula, context)
		status = "OK" if result == expected else f"ERREUR (attendu {expected})"
		print(f"{formula:18} = {result} | {status}")


def main():
	engine = MathEngine()

	context = {
		"x": 10,
		"y": 2,
		"PI": pi
	}

	formulas = [
		"x + y * 2",
		"x + (y * 5)",
		"SIN(0) + PI",
		"x & 1",
		"x > y",
		"x ** y"
	]

	print("--- Test du moteur mathématique ---")

	for formula in formulas:
		try:
			result = engine.calculate(formula, context)
			print(f"Expression : {formula:15} => Résultat : {result}")
		except Exception as e:
			print(f"Erreur sur '{formula}' : {e}")


if __name__ == "__main__":
	test_engine()
