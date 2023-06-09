import pygame
from settings import *
from pathfinding import *
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Combat Map")
clock = pygame.time.Clock()
# Define the size of the grid and the size of each cell
grid_size = 10
cell_size = 64
overlay_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
overlay_surface.fill((RED[0], RED[1], RED[2], 75))



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
        self.strength= 5
        self.defense= 0
        self.hp=20
        self.alive=True
        self.mp = 5
        self.pc = pc
        self.color = WHITE
        self.def_color=WHITE
        self.image=None
        if self.pc:
            self.image=pygame.image.load("knight.png").convert_alpha()
        else:
            self.image=pygame.image.load("satan.png").convert_alpha()
        Entity.all_entities.append(self)
    def attack(self, enemy):
        """
        Initiates an attack against the given enemy character.
        """
        damage = self.strength - enemy.defense
        if damage > 0:
            enemy.hp -= damage
            print(f"{self.name} attacks {enemy.name} for {damage} damage!")
            if enemy.hp <= 0:
                print(f"{enemy.name} is defeated!")
                grid.get_cell(enemy.x,enemy.y).entity=None
                pygame.display.update()
                Entity.all_entities.remove(enemy)
                grid.entities.remove(enemy)
                enemy.alive = False
                
        else:
            print(f"{self.name}'s attack is ineffective against {enemy.name}!")

    def move(self, dx, dy):
        self.x = dx
        self.y = dy

    def draw_entity(self, screen, rect):
        x, y = self.x, self.y
        rect = rect
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, self.color)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(self.image, (self.x*grid.cell_size,self.y*grid.cell_size))
        screen.blit(text, (self.x*grid.cell_size,self.y*grid.cell_size + grid.cell_size * 0.66))
        


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
        self.cells = [[Grid.Cell(x, y,) for y in range(height)] for x in range(width)]
        self.entities = []
        self.cursor = Cursor(0, 0)
        self.selected_entity = None
        self.highlighted_cells=[]
        
    class Cell:
        def __init__(self, x, y, entity=None, terrain_cost=1):
            self.x=x
            self.y=y
            self.entity=entity
            self.terrain_cost= terrain_cost
            self.color = WHITE
            self.def_color=WHITE
            self.terrain_cost = random.choice([1,1,1,2,3])
            self.image=None
            if self.terrain_cost ==1:
                self.def_color=WHITE
                self.image=pygame.image.load(random.choice(["grasstile.png","grasstile1.png", "grasstile.png"])).convert_alpha()
            elif self.terrain_cost==2:
                self.def_color=BLUE
                self.image=pygame.image.load(random.choice(["forest_tile.png","forest_tile1.png"])).convert_alpha()
            elif self.terrain_cost==3:
                self.def_color=RED
                self.image=pygame.image.load(random.choice(["mtn_tile.png","mtn_tile1.png"])).convert_alpha()
            self.color=self.def_color
        def __str__(self):
            return f"cell at {self.x},{self.y}, move cost: {self.terrain_cost}"

    def print_cells(self):
        for row in self.cells:
            for cell in row:
                print(cell)
    def get_cell(self, x, y):
        for row in self.cells:
            for cell in row:
                if cell.x ==x and cell.y == y:
                    return cell

    def add_entity(self, entity):
        self.entities.append(entity)

    def get_entity_at(self, x, y):
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return entity
        return None
    def get_move_cost(self,x,y):
        for row in self.cells:
            for cell in row:
                if cell.x ==x and cell.y==y:
                    return cell.terrain_cost

    def set_selected_entity(self, entity):
        self.selected_entity = entity
    def highlight_cell(self, x,y, color):
        grid.highlighted_cells.append(grid.get_cell(x,y))
    def draw(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                color = cell.color
                screen.blit(cell.image, (x * self.cell_size, y * self.cell_size))
                pygame.draw.rect(surface, color, rect, 1)
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

    # def bfs(grid, start, goal):
    #     queue = [(start, [start], 0)]
    #     visited = set()

    #     while queue:
    #         (node, path, dist) = queue.pop(0)

    #         if node == goal:
    #             return path, dist

    #         if node in visited:
    #             continue

    #         visited.add(node)

    #         for neighbor in grid.get_neighbors(node[0], node[1]):
    #             if neighbor not in visited:
    #                 new_path = list(path)
    #                 new_path.append(neighbor)
    #                 new_dist = dist + grid.get_move_cost(neighbor[0],neighbor[1])  # add 1 to the distance for each move
    #                 queue.append((neighbor, new_path, new_dist))

    #     return None, None
    
    def confirm_action(self, message):
        font = pygame.font.SysFont(None, 30)
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        pygame.draw.rect(screen, BLACK, text_rect, border_radius=10)
        draw_overlay()
        screen.blit(text, text_rect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        return True
                    elif event.key == pygame.K_z:
                        return False


def confirm_move(grid, path):
    for move_index in range(1, len(path)):
        next_cell = grid.get_cell(*path[move_index])

        # Update character position
        grid.selected_entity.x = next_cell.x
        grid.selected_entity.y = next_cell.y

        # Decrease movement points
        grid.selected_entity.mp -= next_cell.terrain_cost

        # Draw the grid and entities
        grid.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return  # Exit the function if X is pressed

        # Wait for 1 second
        pygame.time.wait(1000)

    grid.selected_entity.color = RED
    grid.selected_entity.mp = 0
    grid.selected_entity.moved = True
    grid.selected_entity = None

def check_move(grid,):
    new_x, new_y = grid.cursor.x, grid.cursor.y
    path, dist = bfs(grid,
        (new_x, new_y), grid.selected_entity
    )

    if grid.get_entity_at(new_x, new_y) is None:
        cost = dist
        unhighlight_cells()

        # Highlight the movement range
        for cell in path:
            cell = grid.get_cell(*cell)
            grid.highlighted_cells.append(cell)
            

        # Draw the grid and entities
        grid.draw(screen)
        pygame.display.flip()

        message = "Move %s to (%d, %d)?" % (grid.selected_entity.name, new_x, new_y)

        if grid.confirm_action(message):
            if grid.selected_entity.mp >= cost:
                confirm_move(grid, path)

    # Remove the highlighted cells
    unhighlight_cells()

def highlight_enemy_cells(character):
    # Get neighboring cells
    neighbors = grid.get_neighbors(character.x, character.y)
    enemy_cells = []  # Cells with enemies

    # Find all cells with enemy entities in neighboring cells
    for neighbor in neighbors:
        entity = grid.get_entity_at(*neighbor)
        if entity is not None and not entity.pc:
            enemy_cells.append(grid.get_cell(entity.x, entity.y))

    # Highlight cells with enemies
    for cell in enemy_cells:
        grid.highlighted_cells.append(cell)
def select_enemy(grid, character):
        cursor_x = character.x
        cursor_y = character.y
        if len(grid.highlighted_cells)==0:
            highlight_enemy_cells(character)
        # Use the cursor to select an enemy to attack
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        cursor_x = max(cursor_x - 1, 0)
                    elif event.key == pygame.K_RIGHT:
                        cursor_x = min(cursor_x + 1, grid.width - 1)
                    elif event.key == pygame.K_UP:
                        cursor_y = max(cursor_y - 1, 0)
                    elif event.key == pygame.K_DOWN:
                        cursor_y = min(cursor_y + 1, grid.height - 1)
                    elif event.key == pygame.K_x:
                        selected_cell = grid.get_cell(cursor_x, cursor_y)
                        if selected_cell in grid.highlighted_cells:
                            entity = grid.get_entity_at(selected_cell.x, selected_cell.y)
                            character.attack(entity)
                            grid.highlighted_cells=[]
                            character.mp = 0
                            character.color = RED
                            character.moved = True
                            grid.selected_entity=None
                        return
                    elif event.key == pygame.K_z:
                        return

            # Update the cursor position
            grid.cursor.x = cursor_x
            grid.cursor.y = cursor_y

            # Redraw the grid with the updated cursor position
            grid.draw(screen)
            draw_overlay()
            pygame.display.flip()
def attack_if_possible(character):
    # Highlight enemy cells
    neighbors = grid.get_neighbors(character.x, character.y)
    enemy_cells = []  # Cells with enemies
    
    # Find all cells with enemy entities in neighboring cells
    for neighbor in neighbors:
        entity = grid.get_entity_at(*neighbor)
        if entity is not None and not entity.pc:
            enemy_cells.append(grid.get_cell(entity.x, entity.y))
    if not enemy_cells:
        return
    highlight_enemy_cells(character)

    # Draw the grid with highlighted cells
    grid.draw(screen)
    draw_overlay()
    pygame.display.flip()

    # Prompt for attack or wait
    message = "Attack or wait?"
    options = ["Attack", "Wait"]
    choice = prompt(message, options)

    if choice == "Attack":
        # Highlight enemy cells again
        # highlight_enemy_cells(character)
        # Draw the grid with highlighted cells
        grid.draw(screen)
        # draw_overlay()
        pygame.display.flip()
        # Select the enemy to attack
        select_enemy(grid, character)
    


def highlight_reachable_cells(grid, character):
    max_cost = character.mp
    reachable_cells = []

    for row in grid.cells:
        for cell in row:
            path, dist = bfs(grid, (cell.x, cell.y), character)
            if dist is not None and dist <= max_cost:
                reachable_cells.append(cell)

    # Highlight all reachable cells
    for cell in reachable_cells:
        grid.highlighted_cells.append(cell)

def unhighlight_cells():
    grid.highlighted_cells=[]
       
def prompt(message, options):
    """Display a prompt with the given options and return the selected option."""
    selected = 0
    font = pygame.font.SysFont(None, 30)
    
    
    while True:
        # Display the prompt message
        text = font.render(message, True, WHITE)
        screen.blit(text, (300, 200))

        # Display the prompt options and highlight the selected option
        for i, option in enumerate(options):
            color = RED if i == selected else WHITE
            text = font.render(option, True, color)
            screen.blit(text, (300, 240 + i * 20))
        pygame.display.update()

        # Wait for user input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = max(0, selected - 1)
                elif event.key == pygame.K_DOWN:
                    selected = min(len(options) - 1, selected + 1)
                elif event.key == pygame.K_x:
                    return options[selected]
                elif event.key == pygame.K_z:
                    return None
      

# Define a list of entities on the grid

grid = Grid(10, 10, 64)
for i in range(3):

    city= (random.randint(1,8),random.randint(1,8))
    for row in grid.cells:
        for cell in row:
            if cell.x==city[0] and cell.y==city[1]:
                cell.image=pygame.image.load("city_tile.png")

grid.add_entity(Entity("Player 1", 5, 0, True))
grid.add_entity(Entity("Player 2", 5, 2, True))
grid.add_entity(Entity("Enemy 1", 5, 6, False))
grid.add_entity(Entity("Enemy 2", 6, 6, False))



running = True
timer=0
enemy_phase=False
def draw_overlay():
    overlay = pygame.Surface((grid.cell_size, grid.cell_size), pygame.SRCALPHA)
    overlay.fill((RED[0], RED[1], RED[2], 75))
    for cell in grid.highlighted_cells:
        screen.blit(overlay, (cell.x * grid.cell_size, cell.y * grid.cell_size))
while running:
    clock.tick(60)
    timer+=1
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the grid, the entities, and the cursor
    grid.draw(screen)
    if grid.highlighted_cells is not None:
        draw_overlay()


    # Handle player's turn
    for entity in [e for e in grid.entities if e.pc]:
        if not entity.moved:
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
                                e= grid.selected_entity
                                check_move(grid)
                                attack_if_possible(e)
                            

                        else:
                            if not grid.selected_entity:
                                spot = grid.get_entity_at(grid.cursor.x, grid.cursor.y)
                                if not spot:
                                    # no entity at the selected spot
                                    pass
                                elif spot.pc:
                                    # player unit selected
                                    if spot.moved:
                                        print("Unit has already moved this turn.")
                                    else:
                                        selected_entity = spot
                                        grid.set_selected_entity(selected_entity)
                                        # highlight_reachable_cells(selected_entity)
                                        prompt_options = ["Move", "Wait Here"]
                                        neighbors = grid.get_neighbors(grid.cursor.x, grid.cursor.y)
                                        enemy_adjacent = any(
                                            grid.get_entity_at(neighbor[0], neighbor[1]) and not grid.get_entity_at(neighbor[0], neighbor[1]).pc
                                            for neighbor in neighbors
                                        )
                                        if enemy_adjacent:
                                            prompt_options.append("Attack")
                                        selected_option = prompt(f"{selected_entity.name}",prompt_options,)
                                        if selected_option == "Wait Here":
                                            selected_entity.mp=0
                                            selected_entity.moved=True
                                            grid.selected_entity.color = RED
                                            grid.selected_entity=None
                                            unhighlight_cells()
                                        elif selected_option == "Attack":
                                            select_enemy(grid,selected_entity)
                                        else:
                                            highlight_reachable_cells(grid,selected_entity)
                                            
                                            

                                else:
                                    # enemy unit selected
                                    print("Cannot select enemy units!")

                    elif event.key == pygame.K_z and grid.selected_entity:
                        grid.set_selected_entity(None)
                        unhighlight_cells()
    player_finished=all(entity.moved for entity in grid.entities if entity.pc)
    if player_finished:
            enemy_phase=True
            tomove = [e for e in grid.entities if e.pc == False and e.moved == False]
            paths={}
            for e in tomove.copy():
                e.color=RED
                target = random.choice([e for e in grid.entities if e.pc == True])
                path = a_star((e.x, e.y), (target.x, target.y), grid)
                paths[e]=path
    if timer >50 and enemy_phase==True:
        timer=0
        for e in tomove:
            step=(paths[e][0][0],paths[e][0][1])
            if grid.get_entity_at(*step):
                t = grid.get_entity_at(*step)
                if t.pc:
                    e.attack(t)
                    e.mp=0
                    e.moved=True
                else:
                    e.mp=0
                    e.moved=True
                break
            if e.mp>=grid.get_move_cost(*step):
                e.move(*step)
                e.mp-=grid.get_move_cost(*step)
            else: e.mp=0
            if e.mp==0:
                e.moved=True
                e.color=e.def_color
        
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
            enemy_phase = False
        print("Next turn!")        
        

    pygame.display.update()
pygame.quit()