#Source
#Claude 3.5 Sonnet, https://claude.ai

import pygame
import random
import sys
from enum import Enum
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Directions
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# Snake class
class Snake:
    def __init__(self, x, y, color):
        self.body = [(x, y)]
        self.direction = Direction.RIGHT
        self.color = color

    def move(self):
        self.body.insert(0, self.get_new_head())

    def get_new_head(self):
        x, y = self.body[0]
        if self.direction == Direction.UP:
            return (x, (y - 1) % GRID_HEIGHT)
        elif self.direction == Direction.DOWN:
            return (x, (y + 1) % GRID_HEIGHT)
        elif self.direction == Direction.LEFT:
            return ((x - 1) % GRID_WIDTH, y)
        elif self.direction == Direction.RIGHT:
            return ((x + 1) % GRID_WIDTH, y)

    def grow(self):
        # The tail is now added in the grow method
        self.body.append(self.body[-1])

    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:] or head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT
    

class AISnake:
    def __init__(self, snake, opponent, food):
        self.snake = snake
        self.opponent = opponent
        self.food = food

    def get_best_move(self, depth):
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf

        for move in self.get_possible_moves():
            new_head = self.get_new_head(self.snake, move)
            if self.is_valid_move(new_head):
                new_snake_body = [new_head] + self.snake.body[:-1]
                score = self.minimax(depth - 1, False, alpha, beta, new_snake_body, self.opponent.body, self.food)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        return best_move if best_move else random.choice(list(Direction))

    def minimax(self, depth, is_maximizing, alpha, beta, snake_body, opponent_body, food):
        if depth == 0 or self.is_game_over(snake_body[0], snake_body, opponent_body):
            return self.evaluate(snake_body, opponent_body, food)

        if is_maximizing:
            max_eval = -math.inf
            for move in self.get_possible_moves():
                new_head = self.get_new_head_from_body(snake_body, move)
                if self.is_valid_move(new_head, snake_body[1:], opponent_body):
                    new_snake_body = [new_head] + snake_body[:-1]
                    eval = self.minimax(depth - 1, False, alpha, beta, new_snake_body, opponent_body, food)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_possible_moves():
                new_head = self.get_new_head_from_body(opponent_body, move)
                if self.is_valid_move(new_head, opponent_body[1:], snake_body):
                    new_opponent_body = [new_head] + opponent_body[:-1]
                    eval = self.minimax(depth - 1, True, alpha, beta, snake_body, new_opponent_body, food)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def get_possible_moves(self):
        return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    def get_new_head(self, snake, direction):
        x, y = snake.body[0]
        if direction == Direction.UP:
            return (x, (y - 1) % GRID_HEIGHT)
        elif direction == Direction.DOWN:
            return (x, (y + 1) % GRID_HEIGHT)
        elif direction == Direction.LEFT:
            return ((x - 1) % GRID_WIDTH, y)
        elif direction == Direction.RIGHT:
            return ((x + 1) % GRID_WIDTH, y)

    def get_new_head_from_body(self, body, direction):
        x, y = body[0]
        if direction == Direction.UP:
            return (x, (y - 1) % GRID_HEIGHT)
        elif direction == Direction.DOWN:
            return (x, (y + 1) % GRID_HEIGHT)
        elif direction == Direction.LEFT:
            return ((x - 1) % GRID_WIDTH, y)
        elif direction == Direction.RIGHT:
            return ((x + 1) % GRID_WIDTH, y)

    def is_valid_move(self, new_head, snake_body=None, opponent_body=None):
        if snake_body is None:
            snake_body = self.snake.body[1:]
        if opponent_body is None:
            opponent_body = self.opponent.body
        return (new_head not in snake_body and
                new_head not in opponent_body)

    def is_game_over(self, head, snake_body, opponent_body):
        return (head in snake_body[1:] or
                head in opponent_body or
                head[0] < 0 or head[0] >= GRID_WIDTH or
                head[1] < 0 or head[1] >= GRID_HEIGHT)

    def evaluate(self, snake_body, opponent_body, food):
        head = snake_body[0]
        
        # Distance to food
        distance_to_food = self.manhattan_distance(head, food)
        
        # Check if move leads to food
        if head == food:
            return 1000
        
        # Penalty for getting too close to opponent
        distance_to_opponent = min(self.manhattan_distance(head, pos) for pos in opponent_body)
        opponent_penalty = 50 if distance_to_opponent < 2 else 0
        
        # Penalty for getting too close to self
        self_penalty = 100 if head in snake_body[2:] else 0
        
        # Encourage exploration of empty spaces
        empty_space_score = sum(1 for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT) 
                                if (x, y) not in snake_body and (x, y) not in opponent_body)
        
        return 100 - distance_to_food + empty_space_score - opponent_penalty - self_penalty

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.player_snake = Snake(GRID_WIDTH // 4, GRID_HEIGHT // 2, GREEN)
        self.ai_snake = Snake(3 * GRID_WIDTH // 4, GRID_HEIGHT // 2, BLUE)
        self.food = self.spawn_food()
        self.score = 0
        self.ai = AISnake(self.ai_snake, self.player_snake, self.food)

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.player_snake.body and food not in self.ai_snake.body:
                return food


    def draw(self):
        self.screen.fill(BLACK)
        for pos in self.player_snake.body:
            pygame.draw.rect(self.screen, self.player_snake.color, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for pos in self.ai_snake.body:
            pygame.draw.rect(self.screen, self.ai_snake.color, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, RED, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.player_snake.direction != Direction.DOWN:
                    self.player_snake.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.player_snake.direction != Direction.UP:
                    self.player_snake.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.player_snake.direction != Direction.RIGHT:
                    self.player_snake.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.player_snake.direction != Direction.LEFT:
                    self.player_snake.direction = Direction.RIGHT
        return True

    def update(self):
        # Get the best move for the AI snake
        best_move = self.ai.get_best_move(depth=3)  # You can adjust the depth for different levels of difficulty
        self.ai_snake.direction = best_move

        # Move both snakes
        new_player_head = self.player_snake.get_new_head()
        new_ai_head = self.ai_snake.get_new_head()

        # Check for collisions
        if (self.is_collision(new_player_head) or self.is_collision(new_ai_head)):
            self.reset_game()
            return

        # Move the snakes
        self.player_snake.move()
        self.ai_snake.move()

        # Check for food consumption
        if new_player_head == self.food:
            self.player_snake.grow()
            self.food = self.spawn_food()
            self.score += 1
        else:
            self.player_snake.body.pop()

        if new_ai_head == self.food:
            self.ai_snake.grow()
            self.food = self.spawn_food()
        else:
            self.ai_snake.body.pop()

        # Update the AI's food position
        self.ai.food = self.food

    def is_collision(self, position):
        return (position in self.player_snake.body[1:] or
                position in self.ai_snake.body[1:] or
                position[0] < 0 or position[0] >= GRID_WIDTH or
                position[1] < 0 or position[1] >= GRID_HEIGHT)
    
    def run(self):
        while True:
            if not self.handle_events():
                break
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = SnakeGame()
    game.run()