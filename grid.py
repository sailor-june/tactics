import pygame
from settings import *
from astar import *
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Combat Map")
clock = pygame.time.Clock()
# Define the size of the grid and the size of each cell
grid_size = 10
cell_size = 64


# Define the colors to use for the grid, the cursor, and the selected entity
grid_color = (255, 255, 255)
cursor_color = (255, 0, 0)
selected_color = (0, 255, 0)

# Initialize the cursor position and the selected entity
cursor_x, cursor_y = 0, 0
selected_entity = None


class Entity:
    all_entities = []

    def __init__(self, name, x, y, pc):
        self.name = name
        self.moved = False
        self.x = x
        self.y = y
        self.mp = 5
        self.pc = pc
        self.color = WHITE
        Entity.all_entities.append(self)

    def move(self, dx, dy):
        self.x = dx
        self.y = dy

    def draw_entity(self, screen, rect):
        x, y = self.x, self.y
        rect = rect
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, self.color)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


class Cursor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.entities = []
        self.cursor = Cursor(0, 0)
        self.selected_entity = None

    def add_entity(self, entity):
        self.entities.append(entity)

    def get_entity_at(self, x, y):
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return entity
        return None

    def set_selected_entity(self, entity):
        self.selected_entity = entity

    def draw(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(surface, WHITE, rect, 1)
                entity = self.get_entity_at(x, y)
                if entity is not None:
                    Entity.draw_entity(entity, surface, rect)

        cursor_rect = pygame.Rect(
            self.cursor.x * self.cell_size,
            self.cursor.y * self.cell_size,
            self.cell_size,
            self.cell_size,
        )
        pygame.draw.rect(surface, GREEN, cursor_rect, 3)

        if self.selected_entity is not None:
            selected_rect = pygame.Rect(
                self.selected_entity.x * self.cell_size,
                self.selected_entity.y * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(surface, RED, selected_rect, 3)

    def get_neighbors(self, x, y):
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if x < self.width - 1:
            neighbors.append((x + 1, y))
        if y < self.height - 1:
            neighbors.append((x, y + 1))
        return neighbors
        # THIS CODE RETURNS ALL 8 ORTHOGONAL NEIGHBORS. MIGHT BE USEFUL LATER.
        # neighbors = []
        # for dx in range(-1, 2):
        #     for dy in range(-1, 2):
        #         if dx == 0 and dy == 0:
        #             continue
        #         nx, ny = x + dx, y + dy
        #         if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height:
        #             neighbors.append((nx, ny))
        # return neighbors

    def bfs(grid, start, goal):
        queue = [(start, [start], 0)]
        visited = set()

        while queue:
            (node, path, dist) = queue.pop(0)

            if node == goal:
                return path, dist

            if node in visited:
                continue

            visited.add(node)

            for neighbor in grid.get_neighbors(node[0], node[1]):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    new_dist = dist + 1  # add 1 to the distance for each move
                    queue.append((neighbor, new_path, new_dist))

        return None, None


# Define a list of entities on the grid

grid = Grid(10, 10, 48)
grid.add_entity(Entity("Player 1", 5, 0, True))
grid.add_entity(Entity("Player 2", 5, 2, True))
grid.add_entity(Entity("Enemy 1", 0, 9, False))
grid.add_entity(Entity("Enemy 2", 9, 9, False))

# Define a function to draw the grid


# Define a function to draw an entity


# Define a function to draw the cursor
# def draw_cursor():
#     rect = pygame.Rect(cursor_x * cell_size, cursor_y * cell_size, cell_size, cell_size)
#     pygame.draw.rect(screen, cursor_color, rect, 1)


running = True
timer=0
enemy_phase=False
while running:
    clock.tick(60)
    timer+=1
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the grid, the entities, and the cursor
    grid.draw(screen)

    # Handle player's turn
    if any([e.mp > 0 for e in grid.entities if e.pc == True]):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    grid.cursor.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    grid.cursor.move(1, 0)
                elif event.key == pygame.K_UP:
                    grid.cursor.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    grid.cursor.move(0, 1)
                elif event.key == pygame.K_x:
                    if grid.get_entity_at(grid.cursor.x, grid.cursor.y) is None:
                        if grid.selected_entity:
                            new_x, new_y = grid.cursor.x, grid.cursor.y
                            path, dist = grid.bfs(
                                (selected_entity.x, selected_entity.y), (new_x, new_y)
                            )
                            if grid.get_entity_at(new_x, new_y) is None:
                                cost = dist
                                if selected_entity.mp >= cost:
                                    selected_entity.move(new_x, new_y)
                                    selected_entity.mp -= cost
                                    if selected_entity.mp == 0:
                                        selected_entity.moved = True
                                        selected_entity.color = RED
                                    grid.set_selected_entity(None)

                            else:
                                print("not enough movement points!")

                    else:
                        if not grid.selected_entity:
                            spot = grid.get_entity_at(grid.cursor.x, grid.cursor.y)
                            if not spot.pc:
                                print("Cannot select enemy units!")
                                continue
                            if spot.moved == False:
                                selected_entity = grid.get_entity_at(
                                    grid.cursor.x, grid.cursor.y
                                )
                                grid.set_selected_entity(selected_entity)
                                continue
                            else:
                                print("Unit has already moved this turn.")
                        else:
                            print("Can't move to a square that is already occupied!")
                elif event.key == pygame.K_z and grid.selected_entity:
                    grid.set_selected_entity(None)
    
    else:
        enemy_phase=True
        tomove = [e for e in grid.entities if e.pc == False and e.moved == False]
        paths={}
        for e in tomove.copy():
            target = random.choice([e for e in grid.entities if e.pc == True])
            path = a_star((e.x, e.y), (target.x, target.y), grid)
            paths[e]=path
    if timer >60 and enemy_phase==True:
        timer=0
        for e in tomove:
            e.move(paths[e][0][0],paths[e][0][1])
            e.mp-=1

            if e.mp==0:
                e.moved=True
        
    #check if all units have moved
    all_moved = True
    for entity in grid.entities:
        if not entity.moved:
            all_moved = False

    if all_moved:
        #reset movement
        for entity in grid.entities:
            entity.mp = 5
            entity.moved = False
            entity.color = WHITE
            enemy_phase=False
        print("Next turn!")

    pygame.display.update()
pygame.quit()