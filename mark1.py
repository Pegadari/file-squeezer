""" A proof of concept to demonstrate that a number can be compressed into a mathematical equation.
    While it is clear (from the output) that this implementation does not compress the number, it shows that this approach has merit.

    This algorithm uses tetration. For an explanation, see https://en.wikipedia.org/wiki/Tetration.
"""

__author__ = "Darcy O'Brien (Pegadari)"
__copyright__ = "Copyright 2022, File Squeezer"
__license__ = "GPLv3.0"
__version__ = "0.1.1"
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
            An equation equal to 'target'

        Raises:
            AssertionError: violates context
    """

    assert target >= 0, "Cannot squeeze negative numbers: violates context."

    equation = ""
    distance = target   # remaining distance to 'target'
    
    # sum 2nd tetration terms until they equal 'target'
    while distance:
        # find next largest term
        tet2_base = math.floor(ssrt(distance))
        tet2_value = tet2(tet2_base)

        # add term to the running sum
        equation += f"{tet2_base}**{tet2_base}+"
        distance -= tet2_value

        # logging
        logging.info(distance)

    equation = equation[:-1]    # remove the final "+"
    return equation


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