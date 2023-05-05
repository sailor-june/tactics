
# # ASTAR PATHFINDING
# from settings import *
# def astar(start, goal, grid):

# # Create two lists: open and closed
#     OPEN = {start}  
#     CLOSED = set()
#     g_scores={start:0}
#     f_scores = {start:heu(start,goal)}
# # Add the start node to open
    

#     while OPEN:
#         current = min(OPEN, key=lambda node: f_scores[node])
#         OPEN.remove(current)
#         CLOSED.append(current)

#         if current == goal:
#         # Path has been found
#             path=[]
#             while current in came_from:
#                 [current]

#     # Iterate over neighbors of current node
#         for neighbor in current.neighbors:
#             if neighbor in CLOSED:
#             # Skip to next neighbor
#                 continue

#         # Calculate the cost of reaching the neighbor
#         new_cost = current.g_cost + distance(current, neighbor)

#         if new_cost < neighbor.g_cost or neighbor not in OPEN:
#             # Update neighbor's cost and parent
#             neighbor.g_cost = new_cost
#             neighbor.h_cost = heuristic(neighbor, target)
#             neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
#             neighbor.parent = current

#             if neighbor not in OPEN:
#                 # Add neighbor to OPEN
#                 OPEN.append(neighbor)




def a_star(start, goal, grid):
    # Initialize the open and closed sets
    open_set = {start}
    closed_set = set()

    # Create dictionaries to store the G and F scores of each node
    g_scores = {start: 0}
    f_scores = {start: heuristic(start, goal)}
    came_from={}
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
            # If the neighbor is in the closed set, skip it
            if neighbor in closed_set:
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

def heuristic(a, b):
    # Calculate the Manhattan distance between two points
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


