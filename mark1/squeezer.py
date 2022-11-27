import math
from hyperoperation import second_tetration as tet2
from hyperoperation import super_sqrt as ssrt


def squeeze(target: int) -> list:
        """"""
        return frequency_vector(equation_vector(target))


def equation_vector(target: int) -> list:
    """ The compression algorithm. Find an equation equal to 'target'.

        Args:
            target: the target number for the equation (>= 0)

        Returns:
            An abbreviated equation equal to 'target'

        Raises:
            AssertionError: violates context

        >>> equation_vector(35)
        [3, 2, 2]
        # 3**3 + 2**2 + 2**2 = 35
    """

    assert target >= 0, "Cannot squeeze negative numbers: violates context."

    equation_abbr = []
    # homogeneous sums equation
    remaining_distance = target
    
    # sum 2nd tetration terms until they equal 'target'
    while remaining_distance:
        # find next largest term
        tet2_base = math.floor(ssrt(remaining_distance))
        tet2_value = tet2(tet2_base)

        # add term to the running sum
        equation_abbr.append(tet2_base)
        remaining_distance -= tet2_value

    return equation_abbr


def frequency_vector(equation: list) -> list:
    """"""
    largest_base = equation[0]                  # equation is already in decending order
    frequency_vector = [None] * largest_base

    # 
    for base in range(1, largest_base + 1):
        frequency_vector[base - 1] = equation.count(base)

    return frequency_vector