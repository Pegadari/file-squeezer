""" A proof of concept to demonstrate that a number can be compressed into a mathematical equation.
    While it is clear (from the output) that this implementation does not compress the number, it shows that this approach has merit.

    This algorithm uses tetration. For an explanation, see https://en.wikipedia.org/wiki/Tetration.
"""

__author__ = "Darcy O'Brien"
__copyright__ = "Copyright 2022, File Squeezer"
__license__ = "GNU General Public License v3.0"
__version__ = "0.1.0"
__status__ = "Complete"

import logging
logging.basicConfig(level=logging.INFO)     # comment this line to hide the INFO logging

target = 4382028402103984520845380238045780234      # a random target number
equation = ""                                       # an equation that can be used to output the target number
distance = target                                   # the running target number ('target' - value of 'equation')

# append terms to 'equation' until it equals 'target'
while distance:
    base = 1    # base of the tetration
    tet2 = 1    # value for the 2nd tetration of 'base' ('base' ** 'base')

    # find the largest 2nd tetration that is less than the remaining distance
    while (base+1) ** (base+1) < distance:
        base += 1
        tet2 = base ** base

        logging.info(f"base, tet2: {base}, {tet2}")

    # add 'tet2' to 'equation' and adjust 'distance' to reflect this
    equation += f"{base}**{base}+"
    distance -= tet2

    logging.info(distance)

equation = equation[:-1]    # remove the final '+'
print(equation)
