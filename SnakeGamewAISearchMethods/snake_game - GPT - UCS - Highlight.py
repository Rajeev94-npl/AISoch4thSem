# Source
# ChatGPT https://chatgpt.com/

import pygame
import random
import heapq

pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
light_blue = (173, 216, 230)

# Define display size
dis_width = 800
dis_height = 600

# Set up display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game with UCS AI by ChatGPT')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def ucs(snake_head, food, snake_list):
    queue = [(0, snake_head, [])]  # (cost, position, path)
    heapq.heapify(queue)
    visited = set()
    directions = [(-10, 0), (10, 0), (0, -10), (0, 10)]
    explored_nodes = []

    while queue:
        cost, current_pos, path = heapq.heappop(queue)
        explored_nodes.append(current_pos)

        if current_pos == food:
            return path, explored_nodes

        if current_pos not in visited:
            visited.add(current_pos)
            for direction in directions:
                next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if 0 <= next_pos[0] < dis_width and 0 <= next_pos[1] < dis_height and next_pos not in snake_list:
                    heapq.heappush(queue, (cost + 1, next_pos, path + [direction]))

    return [], explored_nodes

def gameLoop():
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

    while not game_over:

        while game_close:
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

        snake_head = (x1, y1)
        food = (foodx, foody)
        path, explored_nodes = ucs(snake_head, food, snake_List)

        if path:
            direction = path[0]
            x1_change, y1_change = direction
        else:
            game_close = True

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        for node in explored_nodes:
            pygame.draw.rect(dis, light_blue, [node[0], node[1], snake_block, snake_block])

        for step in path:
            pygame.draw.rect(dis, yellow, [snake_head[0], snake_head[1], snake_block, snake_block])
            snake_head = (snake_head[0] + step[0], snake_head[1] + step[1])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

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