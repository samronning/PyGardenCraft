from enum import Enum
import numpy as np


# A block in a plot of a field can be any of these values
# A border block is an element of the border which encircles the available farm area
class BLOCK(Enum):
    NULL = 0
    BORDER = 1
    GRASS = 2
    WATER = 3

class FarmError(Exception):
    pass

class Farm:
    def __init__(self, width, height, block_matrix=None):
        # Makes an empty farm
        if (block_matrix == None):
            self.block_matrix = np.full((width, height), BLOCK.NULL.value, dtype=BLOCK)
            print(self.block_matrix)
        # Farm based on existing farm
        else:
            self.block_matrix = np.asmatrix(block_matrix)
            validate_block_matrix(self.block_matrix)
            print(self.block_matrix)

def validate_block_matrix(block_matrix):
    if (block_matrix.size == 0):
        raise FarmError("A farm's block matrix can't have a width or height of zero")
    for el in np.array(block_matrix):
        if (el != 0 and el != 1 and el != 2 and el != 3):
            raise FarmError("All of a farm's block values must be within 0-3")
