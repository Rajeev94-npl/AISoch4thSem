#Source
#Claude 3.5 Sonnet, https://claude.ai

import pygame
import random
import math
from enum import Enum

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

class Snake:
    def __init__(self, x, y, color):
        self.body = [(x, y)]
        self.direction = Direction.RIGHT
        self.color = color

    def move(self):
        new_head = self.get_new_head()
        if 0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT:
            self.body.insert(0, new_head)
        else:
            # If the new head is out of bounds, don't move
            return False
        return True

    def get_new_head(self):
        x, y = self.body[0]
        if self.direction == Direction.UP:
            return (x, y - 1)
        elif self.direction == Direction.DOWN:
            return (x, y + 1)
        elif self.direction == Direction.LEFT:
            return (x - 1, y)
        elif self.direction == Direction.RIGHT:
            return (x + 1, y)

    def grow(self):
        self.body.append(self.body[-1])

class AISnake:
    def __init__(self, snake, opponent, food):
        self.snake = snake
        self.opponent = opponent
        self.food = food

    def get_best_move(self, depth):
        best_score = -math.inf
        best_moves = []
        alpha = -math.inf
        beta = math.inf

        for move in self.get_possible_moves():
            new_head = self.get_new_head(self.snake, move)
            if self.is_valid_move(new_head):
                new_snake_body = [new_head] + self.snake.body[:-1]
                score = self.minimax(depth - 1, False, alpha, beta, new_snake_body, self.opponent.body, self.food)
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        return random.choice(best_moves) if best_moves else random.choice(list(Direction))

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

    def is_valid_move(self, new_head, snake_body=None, opponent_body=None):
        if snake_body is None:
            snake_body = self.snake.body[1:]
        if opponent_body is None:
            opponent_body = self.opponent.body
        return (new_head not in snake_body and
                new_head not in opponent_body and
                0 <= new_head[0] < GRID_WIDTH and
                0 <= new_head[1] < GRID_HEIGHT)

    def is_game_over(self, head, snake_body, opponent_body):
        return (head in snake_body[1:] or
                head in opponent_body or
                head[0] < 0 or head[0] >= GRID_WIDTH or
                head[1] < 0 or head[1] >= GRID_HEIGHT)

    def evaluate(self, snake_body, opponent_body, food):
        head = snake_body[0]
        
        if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
            return -10000  # Heavily penalize moves that go out of bounds
        
        distance_to_food = self.manhattan_distance(head, food)
        
        if head == food:
            return 10000
        
        distance_to_opponent = min(self.manhattan_distance(head, pos) for pos in opponent_body)
        opponent_penalty = 50 if distance_to_opponent < 2 else 0
        
        self_penalty = 100 if head in snake_body[2:] else 0
        
        # Penalize being close to the boundaries
        boundary_penalty = 0
        if head[0] == 0 or head[0] == GRID_WIDTH - 1:
            boundary_penalty += 50
        if head[1] == 0 or head[1] == GRID_HEIGHT - 1:
            boundary_penalty += 50
        
        empty_space_score = sum(1 for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT) 
                                if (x, y) not in snake_body and (x, y) not in opponent_body)
        
        # Add a small random factor to break ties and prevent freezing
        random_factor = random.uniform(0, 1)
        
        return 1000 - distance_to_food + empty_space_score - opponent_penalty - self_penalty - boundary_penalty + random_factor

    def get_new_head(self, snake, direction):
        x, y = snake.body[0]
        if direction == Direction.UP:
            return (x, y - 1)
        elif direction == Direction.DOWN:
            return (x, y + 1)
        elif direction == Direction.LEFT:
            return (x - 1, y)
        elif direction == Direction.RIGHT:
            return (x + 1, y)

    def get_new_head_from_body(self, body, direction):
        x, y = body[0]
        if direction == Direction.UP:
            return (x, y - 1)
        elif direction == Direction.DOWN:
            return (x, y + 1)
        elif direction == Direction.LEFT:
            return (x - 1, y)
        elif direction == Direction.RIGHT:
            return (x + 1, y)

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game - AI vs AI")
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.move_count = 0
        self.max_moves = 1000

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake1.body and food not in self.snake2.body:
                return food

    def update(self):
        self.move_count += 1
        if self.move_count >= self.max_moves:
            self.reset_game()
            return

        # Get the best move for both AI snakes
        best_move1 = self.ai1.get_best_move(depth=2)
        best_move2 = self.ai2.get_best_move(depth=2)
        
        self.snake1.direction = best_move1
        self.snake2.direction = best_move2

        # Move both snakes
        moved1 = self.snake1.move()
        moved2 = self.snake2.move()

        # Check for collisions
        if (not moved1 or not moved2 or self.is_collision(self.snake1.body[0]) or self.is_collision(self.snake2.body[0])):
            self.reset_game()
            return

        # Check for food consumption
        if self.snake1.body[0] == self.food:
            self.snake1.grow()
            self.food = self.spawn_food()
        else:
            self.snake1.body.pop()

        if self.snake2.body[0] == self.food:
            self.snake2.grow()
            self.food = self.spawn_food()
        else:
            self.snake2.body.pop()

        # Update the AI's food position
        self.ai1.food = self.food
        self.ai2.food = self.food

    def is_collision(self, position):
        return (position in self.snake1.body[1:] or
                position in self.snake2.body[1:] or
                position[0] < 0 or position[0] >= GRID_WIDTH or
                position[1] < 0 or position[1] >= GRID_HEIGHT)

    def reset_game(self):
        self.snake1 = Snake(GRID_WIDTH // 4, GRID_HEIGHT // 2, GREEN)
        self.snake2 = Snake(3 * GRID_WIDTH // 4, GRID_HEIGHT // 2, BLUE)
        self.food = self.spawn_food()
        self.ai1 = AISnake(self.snake1, self.snake2, self.food)
        self.ai2 = AISnake(self.snake2, self.snake1, self.food)
        self.move_count = 0

    def draw(self):
        self.screen.fill(BLACK)
        for pos in self.snake1.body:
            pygame.draw.rect(self.screen, self.snake1.color, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for pos in self.snake2.body:
            pygame.draw.rect(self.screen, self.snake2.color, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, RED, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()