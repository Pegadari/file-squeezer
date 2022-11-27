from hyperoperation import second_tetration as tet2

def expand(frequency_vector: list) -> int:
    """"""
    return evaluate(equation_vector(frequency_vector))


def equation_vector(frequency_vector: list) -> list:
    """"""
    largest_base = len(frequency_vector)
    equation_vector = []

    for base in range(1, largest_base + 1):
        equation_vector += [base] * frequency_vector[base - 1]

    return equation_vector


def evaluate(equation_vector):
    """"""
    return sum(list(map(tet2, equation_vector)))
