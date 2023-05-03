import pygame
from settings import *
# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Combat Map")

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
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        Entity.all_entities.append(self)
    
    def move(self, dx, dy):
        self.x = dx
        self.y = dy
    def draw_entity(e, screen, rect):
        x, y = e.x, e.y
        rect=rect
        #  rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        # pygame.draw.rect(screen, selected_color if e == selected_entity else grid_color, rect, 1)
        font = pygame.font.Font(None, 20)
        text = font.render(e.name, True, (255, 255, 255))
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
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(surface, WHITE, rect, 1)
                entity = self.get_entity_at(x, y)
                if entity is not None:
                    Entity.draw_entity(entity, surface, rect)

        cursor_rect = pygame.Rect(self.cursor.x * self.cell_size, self.cursor.y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(surface, GREEN, cursor_rect, 3)

        if self.selected_entity is not None:
            selected_rect = pygame.Rect(self.selected_entity.x * self.cell_size, self.selected_entity.y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(surface, RED, selected_rect, 3)

# Define a list of entities on the grid

grid = Grid(10, 10, 48)
grid.add_entity(Entity("Player 1", 2, 2))
grid.add_entity(Entity("Player 2", 7, 7))
grid.add_entity(Entity("Enemy 1", 1, 8))
grid.add_entity(Entity("Enemy 2", 9, 1))

# Define a function to draw the grid


# Define a function to draw an entity


# Define a function to draw the cursor
# def draw_cursor():
#     rect = pygame.Rect(cursor_x * cell_size, cursor_y * cell_size, cell_size, cell_size)
#     pygame.draw.rect(screen, cursor_color, rect, 1)


running = True

while running:
    # Handle events
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
                if grid.selected_entity==None:
                        
                    selected_entity = grid.get_entity_at(grid.cursor.x, grid.cursor.y)
                    grid.set_selected_entity(selected_entity)
                
                else:
                    entity = grid.selected_entity
                    new_x, new_y = grid.cursor.x, grid.cursor.y
                    if grid.get_entity_at(new_x, new_y) is None:
                        entity.move(new_x, new_y)
                        grid.set_selected_entity(None)
                    else:
                        print("Can't move to a square that is already occupied!")


    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the grid, the entities, and the cursor
    grid.draw(screen)
    
    

    pygame.display.update()
pygame.quit()

