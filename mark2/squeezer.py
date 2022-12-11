""" This module is used for compression. """

import math
from hyperoperation import second_tetration as tet2
from hyperoperation import super_sqrt as ssrt
from hyperoperation import factorial, inv_factorial, fibonacci, inv_fibonacci

def squeeze(target: int) -> list:
        """ Finds a (hopefully) smaller representation of the argument.

            >>> squeeze(73)
            [3, 4, 2]
        """

        return frequency_vector(frequency_map(target))


def frequency_map(target: int) -> dict:
    """ Finds the frequency map (table) of the bases for the smallest sum of 2nd tetrations equal to the target.

        >>> frequency_map(73)
        {3: 2, 2: 4, 1: 3}
    """

    assert target >= 0, "Cannot squeeze negative numbers: violates context."

    frequency_map = {}
    remaining_distance = target
    
    # sum factorials until they equal 'target'
    largest_factorial_base = math.floor(inv_factorial(remaining_distance))

    for factorial_base in range(largest_factorial_base, 0, -1):        # not accurate, but an approximation for now
        factorial_value = math.factorial(factorial_base)

        # find how many times this factorial value goes into 'remaining_distance'
        frequency = math.floor(remaining_distance / factorial_value)

        # approximate this value with a fibonacci number
        fibonacci_num = math.floor(inv_fibonacci(frequency))
        fibonacci_value = fibonacci(fibonacci_num)

        # store this pair in 'frequency_map' and recalculate remaining distance
        frequency_map[factorial_base] = fibonacci_num
        remaining_distance -= factorial_value * fibonacci_value

        print("fac", factorial_value)
        print("fib", fibonacci_value)
        print("rem", remaining_distance)
        print(factorial_base, fibonacci_num)
    # due to fibonacci approximations, there will be some remaining distance. Use 0 as the factorial base for this.
    frequency_map[0] = remaining_distance
    # remaining_distance = 0

    print(f"fremap: {frequency_map}")
    print(remaining_distance)
    return frequency_map


def frequency_vector(frequency_map: dict) -> list:
    """ Converts the frequency map (table) to a vector, where the index of the value corresponds to its base.
    
        >>> frequency_vector({3: 2, 2: 4, 1: 3})
        [3, 4, 2]
    """

    # largest_base = max(frequency_map.keys())
    # largest_base = len(frequency_map) - 1
    frequency_vector = [None] * len(frequency_map)

    for base in range(0, len(frequency_map)):
        frequency_vector[base] = frequency_map.get(base, 0)

    return frequency_vector