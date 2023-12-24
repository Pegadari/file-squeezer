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

        The expand algorithm takes the vector and calculates the sum by reversing the squeeze algorithm.
        It happens that this is a rather simple formula:
            ∑((index-1) ** (index-1) * value) = ∑(base ** base * frequency)
        With the previous example:
            73 = 1**1 * 3 + 2**2 * 4 + 3**3 * 2
               = 73
"""


__author__ = "Darcy O'Brien (Pegadari)"
__copyright__ = "Copyright 2023, File Squeezer"
__credits__ = ["Darcy O'Brien (Pegadari)", "Riley O'Brien (5igmatic)"]
__license__ = "GPLv3.0"
__version__ = "1.1"
__status__ = "Complete"


# disable limit for integer literals
import sys
sys.set_int_max_str_digits(0)

import timeit
from targets import TARGET_CUSTOM, TARGET_1B, TARGET_16B, TARGET_500B, TARGET_1KB, TARGET_2KB, TARGET_10KB, TARGET_50KB, TARGET_100KB

# for squeezing and expanding
import math
from hyperoperation import second_tetration as tet2
from hyperoperation import super_sqrt as ssrt


int_to_bits = lambda x: len(str(bin(x))) - 2   # -2 because formatted as "0b..."
bits_to_bytes = lambda bits: math.ceil(bits / 8)


def main() -> None:
    """ Tests the effectiveness of the Mark 1 compression algorithm. """

    repetitions = 1


    # TARGET
    target = TARGET_50KB   # unsigned int of a file's binary
    target_bytes = bits_to_bytes(int_to_bits(target))

    print(f"""Target: {target_bytes} bytes""")


    # VECTOR
    vector = squeeze(target)
    # squeeze_time = timeit.timeit(lambda: squeeze(target), number=repetitions) / repetitions

    # 1 byte header for fixed number width.     eg. [1, 3, 11] = 00000100 00010011 10110000 (3 bytes total)
    # This is one representation of 'vector'.                    <header> <01><03> <11><**> (** = padding)
    vector_bytes = 1 + bits_to_bytes(len(vector) * int_to_bits(max(vector)))
    vector_bytes_min = bits_to_bytes(sum(list(map(int_to_bits, vector))))
    vector_size_2(vector)
    print(len(elias_delta_encode(vector)) / 8)
    print(len(elias_gamma_encode(vector)) / 8)
    print(len(elias_omega_encode(vector)) / 8)

    print(f"Vector: {vector_bytes} bytes (lower bound: {vector_bytes_min} bytes)\n")
    # print(vector)
    

    # STATISTICS
    # constructor_result = expand(vector)     # should be the same as 'target'
    # expand_time = timeit.timeit(lambda: expand(vector), number=repetitions) / repetitions

    compression_ratio = target_bytes / vector_bytes
    compression_grade = "bad"
    if 1 < compression_ratio <= 5:
        compression_grade = "moderate"
    elif 5 < compression_ratio:
        compression_grade = "good"

    # print(f"""Statistics:
    # compression ratio:  {compression_ratio} ({compression_grade})
    # compression time:   {squeeze_time} s
    # decompression time: {expand_time} s
    # total time:         {squeeze_time + expand_time} s
    # lossless:           {target == constructor_result}
    # """)

    # assert target == constructor_result, "Algorithm is not lossless."   # after statistics to show timings


def squeeze(target: int) -> list:
    """ Finds a (hopefully) smaller representation of the argument.

        >>> squeeze(73)
        [3, 4, 2]
    """

    def frequency_map(target: int) -> dict:
        """ Finds the frequency map (table) of the bases for the smallest sum of 2nd tetrations equal to the target.

            >>> frequency_map(73)
            {3: 2, 2: 4, 1: 3}
        """

        assert target >= 0, "Cannot squeeze negative numbers: violates context."

        frequency_map = {}
        remaining_distance = target
        
        # sum 2nd tetration until they equal 'target'
        while remaining_distance:
            # find next largest 2nd tetration
            tet2_base = math.floor(ssrt(remaining_distance))
            tet2_value = tet2(tet2_base)

            # find how many times the largest 2nd tetration goes into 'remaining_distance'
            frequency = math.floor(remaining_distance / tet2_value)

            frequency_map[tet2_base] = frequency
            remaining_distance -= tet2_value * frequency

        return frequency_map


    def frequency_vector(frequency_map: dict) -> list:
        """ Converts the frequency map (table) to a vector, where the index of the value corresponds to its base.
        
            >>> frequency_vector({3: 2, 2: 4, 1: 3})
            [3, 4, 2]
        """

        largest_base = max(frequency_map.keys())
        frequency_vector = [None] * largest_base

        for base in range(1, largest_base + 1):   # bases index from 1, not 0
            frequency_vector[base - 1] = frequency_map.get(base, 0)

        return frequency_vector

    return frequency_vector(frequency_map(target))

    
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


# def vector_size(frequency_vector: list) -> int:
#     """
#     Previously, all blocks were a fixed length, which was an inefficient use of space.
#     Now, the top _alpha_ of frequencies will be a lesser fixed length and the remaining frequencies are higher fixed length.
#     One bit will be used to denote whether the frequency is lesser or higher.
#     """
#     alpha = 0.6     # tweak this
#     threshold = sorted(frequency_vector)[round(len(frequency_vector) * alpha)]
#     lower_size = round(math.log2(threshold))
#     upper_size = int_to_bits(max(frequency_vector))

#     size_vector = [None] * len(frequency_vector)
#     for i, frequency in enumerate(frequency_vector):
#         if frequency >= 2**lower_size:
#             size = upper_size
#         else:
#             size = lower_size
#         size_vector[i] = 1 + size
    
#     print(math.ceil(sum(size_vector) / 8) + 2)



def vector_size_2(frequency_vector: list) -> int:
    smallest_size = 99999999
    best_lower_size = 0
    upper_size = int_to_bits(max(frequency_vector))
    for lower_size in range(1, upper_size):
        size_vector = [None] * len(frequency_vector)
        for i, frequency in enumerate(frequency_vector):
            if frequency >= 2**lower_size:
                size = upper_size
            else:
                size = lower_size
            size_vector[i] = 1 + size
        size = math.ceil(sum(size_vector) / 8) + 2
        smallest_size = min(smallest_size, size)
        if smallest_size == size:
            best_lower_size = lower_size
    
    print(smallest_size)


def vector_size_4(frequency_vector: list) -> int:
    smallest_size = 99999999
    best_sizes = []
    size3 = int_to_bits(max(frequency_vector))
    for size0 in range(1, size3):
        for size1 in range(1, size3):
            for size2 in range(1, size3):

                size_vector = [None] * len(frequency_vector)
                for i, frequency in enumerate(frequency_vector):
                    if frequency < 2**size0:
                        size = size0
                    elif frequency < 2**size1:
                        size = size1
                    elif frequency < 2**size2:
                        size = size2
                    else:
                        size = size3

                    size_vector[i] = 2 + size

                size = math.ceil(sum(size_vector) / 8) + 4
                smallest_size = min(smallest_size, size)
                if smallest_size == size:
                    best_sizes = [size0, size1, size2, size3]
    
    print(smallest_size, int_to_bits(max(frequency_vector)))
    print(best_sizes)

def vector_size(frequency_vector: list) -> int:
    delta = 0
    for i in frequency_vector:
        if i == 0:
            delta += 1
        else:
            delta += math.floor(math.log2(i)) + 2 * math.floor(math.log2(math.floor(math.log2(i)) + 1)) + 1

    gamma = 0
    for i in frequency_vector:
        if i == 0:
            gamma += 1
        else:
            gamma += 2 * math.floor(math.log2(i)) + 1

    print(delta, gamma)
    # use Elias-Delta encoding for ~0.9 compression ratio


def int_to_bin_str(i: int):
    return str(bin(i))[2:]



def elias_gamma_encode(vector: list[int]):
    string = ""
    for element in vector:
        e = element + 1
        N = math.floor(math.log2(e))
        e_binary = int_to_bin_str(e)
        string += N * '0' + e_binary
    return string

    



def elias_delta_encode(vector: list):
    string = ""
    for element in vector:
        e = element + 1
        N = math.floor(math.log2(e))
        L = math.floor(math.log2(N + 1))
        string += L * '0' + int_to_bin_str(N + 1) + int_to_bin_str(e)[1:]
    return string


def elias_delta_decode(string: str):
    vector = []
    L = 0
    while string:
        while L < len(string) and string[L] == '0':
            L += 1
        split = 2 * L + 1
        exponent = int(string[:split], 2) - 1
        remainder = int('0' + string[split:split + exponent], 2)
        x = 2 ** exponent + remainder
        frequency = x - 1
        vector.append(frequency)
        string = string[split + exponent:]
        L = 0
        
    return vector   

def elias_omega_encode(vector: list[int]):
    string = ""
    for element in vector:
        N = element + 1
        element_string = "0"
        while N != 1:
            N_binary = int_to_bin_str(N)
            element_string = N_binary + element_string
            N = len(N_binary) - 1
        string += element_string
    return string

if __name__ == "__main__":
    main()
