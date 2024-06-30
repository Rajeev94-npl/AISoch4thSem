# Source
# ChatGPT https://chatgpt.com/

import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Display dimensions
dis_width = 800
dis_height = 600

# Create the display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game with AI by ChatGPT')

# Clock object to control the game speed
clock = pygame.time.Clock()

# Snake block size
snake_block = 10
snake_speed = 45

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    """Draws the snake on the display."""
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    """Displays a message on the screen."""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def dfs_path(snake_head, food_pos, snake_body):
    """Performs a depth-first search to find a path from snake's head to food."""
    stack = [snake_head]
    parent = {snake_head: None}
    visited = set()
    
    while stack:
        position = stack.pop()
        
        if position == food_pos:
            # Found the path to the food
            path = []
            while position:
                path.append(position)
                position = parent[position]
            path.reverse()
            return path
        
        if position in visited:
            continue
        visited.add(position)
        
        x, y = position
        for dx, dy in [(-snake_block, 0), (snake_block, 0), (0, -snake_block), (0, snake_block)]:
            next_pos = (x + dx, y + dy)
            if (0 <= next_pos[0] < dis_width and 0 <= next_pos[1] < dis_height and 
                next_pos not in snake_body and next_pos not in visited):
                stack.append(next_pos)
                parent[next_pos] = position
    
    return []  # Return an empty path if no path is found

def draw_path(path):
    """Draws the search path on the display."""
    for position in path:
        pygame.draw.rect(dis, yellow, [position[0], position[1], snake_block, snake_block])

def gameLoop():
    """Main game loop."""
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    path = []

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if not path:
            path = dfs_path((x1, y1), (foodx, foody), snake_List)

        if path:
            next_pos = path.pop(0)
            x1, y1 = next_pos

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_path(path)  # Draw the search path
        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
