""" A proof of concept to demonstrate that a file can be compressed into a mathematical equation.

    Using the unsigned integer representation of a file's binary, the file can be compressed by finding an equation with 
    as few (2nd tetration) terms as possible. To uncompress the file, evaluate the equation and convert it back to binary.
    Since this equation only features 2nd tetrations, the equation can be stored as a list of bases (similar to how you don't
    store the '1.' in a floating point number).

    While it is clear (from the output) that this implementation does not compress the number, it shows that this approach 
    has merit.

    This algorithm uses tetration. For an explanation, see https://en.wikipedia.org/wiki/Tetration.
"""

__author__ = "Darcy O'Brien (Pegadari)"
__copyright__ = "Copyright 2022, File Squeezer"
__license__ = "GPLv3.0"
__version__ = "0.1.3"
__status__ = "Complete"


import logging
import math
from scipy.special import lambertw


def main() -> None:
    """ Entry point. """
    # logging.basicConfig(level=logging.INFO)     # comment this line to supress logging.info()

    target = 4382028402103984520845380238045780234      # a random target number
    print(squeeze(target))


def squeeze(target: int) -> str:
    """ The compression algorithm. Find an equation equal to 'target'.

        Args:
            target: the target number for the equation (>= 0)

        Returns:
            An abbreviated equation equal to 'target'

        Raises:
            AssertionError: violates context
    """

    assert target >= 0, "Cannot squeeze negative numbers: violates context."

    equation_abbr = []
    equation_full = ""  # for logging
    distance = target   # remaining distance to 'target'
    
    # sum 2nd tetration terms until they equal 'target'
    while distance:
        # find next largest term
        tet2_base = math.floor(ssrt(distance))
        tet2_value = tet2(tet2_base)

        # add term to the running sum
        equation_abbr.append(tet2_base)
        distance -= tet2_value

        # logging
        equation_full += f"{tet2_base}**{tet2_base}+"
        logging.info(distance)

    # logging
    equation_full = equation_full[:-1]    # remove the final "+"
    logging.info(equation_full)

    return equation_abbr


def tet2(base: int) -> int:
    """ Return the 2nd tetration of the argument (base ** base).
        For an explanation of tetration, see https://en.wikipedia.org/wiki/Tetration.
    """

    return base ** base


def ssrt(x: int) -> float:
    """ Return the super square-root of the argument (reverse of 2nd tetration).
        For an explanation, see https://en.wikipedia.org/wiki/Tetration#Square_super-root.
    """

    return math.exp(lambertw(math.log(x)).real)


if __name__ == "__main__":
    main()
