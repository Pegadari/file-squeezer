""" This module is used for decompression. """

from hyperoperation import second_tetration as tet2

def expand(frequency_vector: list) -> int:
    """ Calculates the result of the frequency vector.
    
        >>> expand([3, 4, 2])
        73
    """

    result = 0
    largest_base = len(frequency_vector)

    # ∑(base ** base * frequency)
    for base in range(1, largest_base + 1):     # bases index from 1, not 0
        result += tet2(base) * frequency_vector[base -1]

    return result
