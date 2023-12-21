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
    valid_values = [block_type.value for block_type in BLOCK]
    if not np.isin(block_matrix, valid_values).all():
        raise FarmError("All of a farm's block values must be within 0-3")

def has_single_closed_loop(farm):
    # Convert the farm matrix to a graph
    graph = farm_to_graph(farm)

    # Keep track of visited nodes
    visited = set()

    # Keep track of the number of closed loops found
    closed_loop_count = 0

    # Check for a closed loop starting from each unvisited BORDER node
    for node in graph.keys():
        if node not in visited and farm[node] == BLOCK.BORDER:
            closed_loop_count += dfs_has_single_closed_loop(graph, node, visited, start_node=node)

            # If more than one closed loop is found, return False
            if closed_loop_count > 1:
                return False

    # If exactly one closed loop is found, return True
    return closed_loop_count == 1

def dfs_has_single_closed_loop(graph, current_node, visited, start_node):
    # Visit the current node
    visited.add(current_node)

    # Recursively visit neighbors
    for neighbor in graph[current_node]:
        if neighbor not in visited:
            return dfs_has_single_closed_loop(graph, neighbor, visited, start_node)
        elif neighbor == start_node:
            # If the neighbor is the starting node, a closed loop is found
            return 1

    return 0

def farm_to_graph(farm):
    graph = {}

    for i in range(farm.shape[0]):
        for j in range(farm.shape[1]):
            current_node = (i, j)

            if farm[current_node] == BLOCK.BORDER:
                neighbors = get_border_neighbors(farm, current_node)
                graph[current_node] = neighbors

    return graph

def get_border_neighbors(farm, node):
    neighbors = []

    for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbor_node = (node[0] + i, node[1] + j)
        if 0 <= neighbor_node[0] < farm.shape[0] and 0 <= neighbor_node[1] < farm.shape[1]:
            if farm[neighbor_node] == BLOCK.BORDER:
                neighbors.append(neighbor_node)

    return neighbors

def valid_farm_mask(farm):
    # Convert the farm matrix to a graph
    graph = farm_to_graph(farm)

    # Keep track of visited nodes
    visited = set()

    # List to store nodes within the closed loop
    closed_loop_nodes = []

    # Check for a closed loop starting from each unvisited BORDER node
    for node in graph.keys():
        if node not in visited and farm[node] == BLOCK.BORDER:
            closed_loop_nodes.extend(dfs_get_closed_loop_nodes(graph, node, visited, start_node=node))

    # Create a mask for valid farm spaces within the closed loop
    valid_farm_mask = np.zeros_like(farm, dtype=bool)
    for node in closed_loop_nodes:
        valid_farm_mask[node] = True

    return valid_farm_mask

def dfs_get_closed_loop_nodes(graph, current_node, visited, start_node):
    # List to store nodes within the closed loop
    closed_loop_nodes = []

    # Visit the current node
    visited.add(current_node)
    closed_loop_nodes.append(current_node)

    # Recursively visit neighbors
    for neighbor in graph[current_node]:
        if neighbor not in visited:
            closed_loop_nodes.extend(dfs_get_closed_loop_nodes(graph, neighbor, visited, start_node))

    return closed_loop_nodes