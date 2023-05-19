from collections import deque
def a_star(start, goal, grid):
    # Initialize the open and closed sets
    open_set = {start}
    closed_set = set()

    # Create dictionaries to store the G and F scores of each node
    g_scores = {start: 0}
    f_scores = {start: heuristic(start, goal)}
    came_from = {}

    while open_set:
        # Get the node in the open set with the lowest F score
        current = min(open_set, key=lambda node: f_scores[node])

        if current == goal:
            # If we have reached the goal, reconstruct the path and return it
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        # Move current from open to closed set
        open_set.remove(current)
        closed_set.add(current)

        # Loop through the neighbors of the current node
        for neighbor in grid.get_neighbors(current[0], current[1]):
            # If the neighbor is in the closed set or occupied by an entity of the opposing team, skip it
            if neighbor in closed_set or is_opposing_team_entity(grid,neighbor):
                continue

            # Calculate the tentative G score for this neighbor
            tentative_g_score = g_scores[current] + 1

            # If the neighbor is not in the open set, add it
            if neighbor not in open_set:
                open_set.add(neighbor)

            # If this path to the neighbor is worse than any previous one, skip it
            elif tentative_g_score >= g_scores[neighbor]:
                continue

            # This path is the best until now. Record it!
            came_from[neighbor] = current
            g_scores[neighbor] = tentative_g_score
            f_scores[neighbor] = tentative_g_score + heuristic(neighbor, goal)

    # If we get here, there is no path to the goal
    return None

def is_opposing_team_entity(grid,cell):
    entity = grid.get_entity_at(cell[0], cell[1])
    if entity is not None:
        # Check if the entity belongs to the opposing team
        return not entity.pc
    return False

# def a_star(start, goal, grid):
#     # Initialize the open and closed sets
#     open_set = {start}
#     closed_set = set()

#     # Create dictionaries to store the G and F scores of each node
#     g_scores = {start: 0}
#     f_scores = {start: heuristic(start, goal)}
#     came_from={}
#     while open_set:
#         # Get the node in the open set with the lowest F score
#         current = min(open_set, key=lambda node: f_scores[node])

#         if current == goal:
#             # If we have reached the goal, reconstruct the path and return it
#             path = []
#             while current in came_from:
#                 path.append(current)
#                 current = came_from[current]
#             return path[::-1]

#         # Move current from open to closed set
#         open_set.remove(current)
#         closed_set.add(current)

#         # Loop through the neighbors of the current node
#         for neighbor in grid.get_neighbors(current[0], current[1]):
#             # If the neighbor is in the closed set, skip it
#             if neighbor in closed_set:
#                 continue

#             # Calculate the tentative G score for this neighbor
#             tentative_g_score = g_scores[current] + 1

#             # If the neighbor is not in the open set, add it
#             if neighbor not in open_set:
#                 open_set.add(neighbor)

#             # If this path to the neighbor is worse than any previous one, skip it
#             elif tentative_g_score >= g_scores[neighbor]:
#                 continue

#             # This path is the best until now. Record it!
#             came_from[neighbor] = current
#             g_scores[neighbor] = tentative_g_score
#             f_scores[neighbor] = tentative_g_score + heuristic(neighbor, goal)

#     # If we get here, there is no path to the goal
#     return None


# def a_star(entity, goal, grid):
#     start = (entity.x, entity.y)
#     start_cell = grid.get_cell(*start)
#     is_pc = entity.pc

#     open_list = []
#     closed_list = []
#     g_values = {}  # Dictionary to store g values
#     h_values = {}  # Dictionary to store h values
#     f_values = {}  # Dictionary to store f values

#     g_values[start_cell] = 0
#     h_values[start_cell] = heuristic(start_cell, goal)
#     f_values[start_cell] = g_values[start_cell] + h_values[start_cell]

#     open_list.append(start_cell)

#     while open_list:
#         current_cell = min(open_list, key=lambda cell: f_values[cell])

#         if current_cell == goal:
#             path = reconstruct_path(current_cell)
#             return path

#         open_list.remove(current_cell)
#         closed_list.append(current_cell)

#         neighbors = grid.get_neighbors(current_cell.x, current_cell.y)
#         for neighbor in neighbors:
#             neighbor_cell = grid.get_cell(*neighbor)

#             if is_pc:
#                 # Skip if the neighbor cell is occupied by an enemy
#                 if neighbor_cell.entity and not neighbor_cell.entity.pc:
#                     continue
#             else:
#                 # Skip if the neighbor cell is occupied by a PC character
#                 if neighbor_cell.entity and neighbor_cell.entity.pc:
#                     continue

#             if neighbor_cell in closed_list:
#                 continue

#             tentative_g = g_values[current_cell] + grid.get_move_cost(current_cell.x, current_cell.y, neighbor_cell.x, neighbor_cell.y)

#             if neighbor_cell not in open_list:
#                 open_list.append(neighbor_cell)
#             elif tentative_g >= g_values[neighbor_cell]:
#                 continue

#             neighbor_cell.parent = current_cell
#             g_values[neighbor_cell] = tentative_g
#             h_values[neighbor_cell] = heuristic(neighbor_cell, goal)
#             f_values[neighbor_cell] = g_values[neighbor_cell] + h_values[neighbor_cell]

#     return None



def bfs(grid, goal, character):
    is_pc = character.pc
    start = (character.x, character.y)
    queue = deque([(start, [start], 0)])
    visited = set()

    while queue:
        (node, path, dist) = queue.popleft()

        if node == goal:
            return path, dist

        if node in visited:
            continue

        visited.add(node)

        for neighbor in grid.get_neighbors(node[0], node[1]):
            if neighbor not in visited:
                neighbor_cell = grid.get_cell(*neighbor)
                if is_opposing_team_entity(grid, neighbor):
                    continue

                new_path = list(path)
                new_path.append(neighbor)
                new_dist = dist + grid.get_move_cost(neighbor[0], neighbor[1])
                queue.append((neighbor, new_path, new_dist))

    return None, None

def heuristic(a, b):
    # Calculate the Manhattan distance between two points
    return abs(a[0] - b[0]) + abs(a[1] - b[1])