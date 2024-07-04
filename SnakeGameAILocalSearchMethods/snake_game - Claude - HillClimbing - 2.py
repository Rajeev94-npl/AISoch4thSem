'''This Hill Climbing approach will make the snake always choose the move that seems best in the immediate future (closest to the food), 
which can sometimes lead to the snake getting stuck in local optima or corners. 
However, it's generally more straightforward and deterministic compared to Simulated Annealing.'''

#Source
#Claude 3.5 Sonnet, https://claude.ai

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI - Hill Climbing")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake class
class Snake:
    def __init__(self):
        self.score = 0
        self.length = 1
        self.reset()

    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        while len(self.body) < self.length:
            self.grow(False)

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check if the new head is within bounds
        if 0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT:
            self.body.insert(0, new_head)
            if len(self.body) > self.length:
                self.body.pop()
        else:
            # If out of bounds, reset the snake
            self.reset()

    def grow(self, increase_score=True):
        self.length += 1
        if increase_score:
            self.score += 1

    def check_collision(self):
        return len(self.body) != len(set(self.body))

# Hill Climbing AI
def hill_climbing(snake, food):
    current_head = snake.body[0]
    best_direction = snake.direction
    best_distance = math.inf

    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_head = (current_head[0] + dx, current_head[1] + dy)
        
        # Check if the new head is within bounds and not colliding with the snake's body
        if (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT
                and new_head not in snake.body[:-1]):
            distance = math.sqrt((new_head[0] - food[0])**2 + (new_head[1] - food[1])**2)
            
            if distance < best_distance:
                best_distance = distance
                best_direction = (dx, dy)

    return best_direction

# Game setup
snake = Snake()
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
clock = pygame.time.Clock()

# Font for displaying score
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI move
    snake.direction = hill_climbing(snake, food)
    snake.move()

    # Check for food consumption
    if snake.body[0] == food:
        snake.grow()
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        while food in snake.body:  # Ensure food doesn't spawn on snake
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    # Check for collision
    if snake.check_collision():
        snake.reset()

    # Draw everything
    WINDOW.fill(BLACK)
    for segment in snake.body:
        pygame.draw.rect(WINDOW, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(WINDOW, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Display score and length
    score_text = font.render(f"Score: {snake.score} Length: {snake.length}", True, WHITE)
    WINDOW.blit(score_text, (10, 10))
    
    pygame.display.flip()

    # Control game speed
    clock.tick(10)

pygame.quit()