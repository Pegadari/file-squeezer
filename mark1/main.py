""" A proof of concept to demonstrate that a file can be compressed into a mathematical equation.

    Using the unsigned integer representation of a file's binary, the file can be compressed by finding an equation with 
    as few (2nd tetration) terms as possible. To uncompress the file, evaluate the equation and convert it back to binary.
    Since this equation only features 2nd tetrations, the equation can be stored as a list of bases (similar to how you 
    don't store the '1.' in a floating point number).

    While it is clear (from the output) that this implementation does not compress the number, it shows that this approach 
    has merit... hopefully.

    This algorithm uses tetration. For an explanation, see https://en.wikipedia.org/wiki/Tetration.

    HOW THE ALGORITHM WORKS:
        Consider 73.
        The squeeze algorithm equates 73 to a sum of tetrations:
            73 = 3**3 + 3**3 + 2**2 + 2**2 + 2**2 + 2**2 + 1**1 + 1**1 + 1**1
        We could store this equation, but it would be very inefficient.
        Observe that this equation is 'homogeneous' in that it is a sum of the same type of operation.
        Thus, the squeeze algorithhm converts it to a list of 2nd tetrations:
            73 = [3, 3, 2, 2, 2, 2, 1, 1, 1]
        We will now reverse the list to continue the explanation.
            73 = [1, 1, 1, 2, 2, 2, 2, 3, 3]
        However, there are still a lot of repeated elements.
        The squeeze algorithm then converts this list into a frequency vector (similar to a frequency table),
        but where the index of the value corresponds to its base, specifically, index = base - 1:
            73 = [3, 4, 2]
        Observe that the previous list had 3 ones, 4 twos and 2 threes, which is represented by the vector.

        The main function represents this vector as a continuous binary string of fixed value width for 
        the purposes of evaluating the compression ratio.

        The expand algorithm takes the vector and calculates the sum but reversing the squeeze algorithm.
        It happens that this is a rather simple formula:
            ∑((index-1) ** (index-1) * value) = ∑(base ** base * frequency)
        With the previous example:
            73 = 1**1 * 3 + 2**2 * 4 + 3**3 * 2
               = 73
"""

__author__ = "Darcy O'Brien (Pegadari)"
__copyright__ = "Copyright 2022, File Squeezer"
__license__ = "GPLv3.0"
__version__ = "1.0"
__status__ = "Complete"


import math
import timeit
from squeezer import squeeze
from expander import expand
from target import TARGET_CUSTOM, TARGET_1B, TARGET_16B, TARGET_500B, TARGET_1KB, TARGET_2KB, TARGET_10KB, TARGET_50KB, TARGET_100KB


get_bits = lambda x: len(str(bin(x))) - 2   # -2 because formatted as "0b..."
get_bytes = lambda bits: math.ceil(bits / 8)


def main() -> None:
    """ Tests the effectiveness of the Mark 1 compression algorithm. """

    repetitions = 1

    # TARGET
    target = TARGET_1KB     # unsigned int of a file's binary
    target_bytes = get_bytes(get_bits(target))

    print(f"""Target: {target_bytes} bytes""")

    # VECTOR
    vector = squeeze(target)
    squeeze_time = timeit.timeit(lambda: squeeze(target), number=repetitions) / repetitions

    # 1 byte header for fixed number width, eg. [1, 3, 11] = 00000100 00010011 10110000 (3 bytes total)
    #                                                        <header> <01><03> <11><**> (** = padding)
    vector_bytes = 1 + get_bytes(len(vector) * get_bits(max(vector)))
    vector_bytes_min = get_bytes(sum(list(map(get_bits, vector))))

    print(f"Vector: {vector_bytes} bytes (minimum possible: {vector_bytes_min} bytes)\n")

    # STATISTICS
    constructor_result = expand(vector)     # should be the same as 'target'
    expand_time = timeit.timeit(lambda: expand(vector), number=repetitions) / repetitions

    compression_ratio = target_bytes / vector_bytes
    compression_grade = "bad"
    if 1 < compression_ratio <= 5:
        compression_grade = "moderate"
    elif 5 < compression_ratio:
        compression_grade = "good"

    print(f"""Statistics:
    compression ratio:  {compression_ratio} ({compression_grade})
    compression time:   {squeeze_time} s
    decompression time: {expand_time} s
    total time:         {squeeze_time + expand_time} s
    lossless:           {target == constructor_result}
    """)

    assert target == constructor_result     # after statistics to show timings


if __name__ == "__main__":
    main()
