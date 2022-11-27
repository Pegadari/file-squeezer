""" A proof of concept to demonstrate that a file can be compressed into a mathematical equation.

    Using the unsigned integer representation of a file's binary, the file can be compressed by finding an equation with 
    as few (2nd tetration) terms as possible. To uncompress the file, evaluate the equation and convert it back to binary.
    Since this equation only features 2nd tetrations, the equation can be stored as a list of bases (similar to how you don't
    store the '1.' in a floating point number).

    While it is clear (from the output) that this implementation does not compress the number, it shows that this approach 
    has merit.

    This algorithm uses tetration. For an explanation, see https://en.wikipedia.org/wiki/Tetration.

    HOW THE ALGORITHM WORKS:
        Lorum ipsum...
"""

__author__ = "Darcy O'Brien (Pegadari)"
__copyright__ = "Copyright 2022, File Squeezer"
__license__ = "GPLv3.0"
__version__ = "1.4"
__status__ = "Complete"


import logging
import math
from scipy.special import lambertw
import scipy
from multimethod import multimethod


def main() -> None:
    """ Entry point. """

    # logging.basicConfig(level=logging.INFO)     # comment this line to supress logging.info()

    target = 4382028402103984520845380238045780234      # unsigned int of a file's binary (this file is 16 bytes)
    print(squeeze(target))


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

        >>> squeeze(35)
        [3, 2, 2]
    """

    assert target >= 0, "Cannot squeeze negative numbers: violates context."

    equation_abbr = []
    equation_full = ""  # for logging
    remaining_distance = target
    
    # sum 2nd tetration terms until they equal 'target'
    while remaining_distance:
        # find next largest term
        tet2_base = math.floor(ssrt(remaining_distance))
        tet2_value = tet2(tet2_base)

        # add term to the running sum
        equation_abbr.append(tet2_base)
        remaining_distance -= tet2_value

        # logging
        equation_full += f"{tet2_base}**{tet2_base}+"
        logging.info(remaining_distance)

    # logging
    equation_full = equation_full[:-1]    # remove the final "+"
    logging.info(equation_full)

    return equation_abbr


def equation_vector_to_frequency_vector(equation: list) -> list:
    """"""
    largest_base = equation[0]                  # equation is already in decending order
    frequency_vector = [None] * largest_base

    # 
    for base in range(largest_base, 0, -1):
        print(base)
        frequency_vector[base - 1] = equation.count(base)

    return frequency_vector


def expand(frequency_vector: list) -> int:
    return evaluate(equation_vector(frequency_vector))


def evaluate():
    pass

def frequency_vector_to_equation_vector():
    pass

def tet2(base: int) -> int:
    """ Return the 2nd tetration of the argument (base ** base).
        For an explanation, see https://en.wikipedia.org/wiki/Tetration.
    """

    return base ** base


def ssrt(radicand: int) -> float:
    """ Return the super square-root of the argument (reverse of 2nd tetration).
        For an explanation, see https://en.wikipedia.org/wiki/Tetration#Square_super-root.
    """

    return math.exp(lambertw(math.log(radicand)).real)


if __name__ == "__main__":
    main()
