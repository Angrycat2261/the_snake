import pygame
import random
import sys
from typing import List, Tuple, Optional

CELL_SIZE = 20
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
FPS = 20

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    def _init_(self, position: Tuple[int, int]):
        self.position = position
        self.body_color = (255, 255, 255)

    def draw(self, surface: pygame.Surface) -> None:
        pass


class Apple(GameObject):
    def _init_(self, forbidden: Optional[List[Tuple[int, int]]] = None):
        super()._init_((0, 0))
        self.body_color = RED
        self.randomize_position(forbidden)

    def randomize_position(self, forbidden: Optional[List[Tuple[int, int]]] = None):
        if forbidden is None:
            forbidden = []
        while True:
            x = random.randrange(0, GRID_WIDTH) * CELL_SIZE
            y = random.randrange(0, GRID_HEIGHT) * CELL_SIZE
            if (x, y) not in forbidden:
                self.position = (x, y)
                return

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.body_color, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


class Snake(GameObject):
    def _init_(self):
        cx = GRID_WIDTH // 2 * CELL_SIZE
        cy = GRID_HEIGHT // 2 * CELL_SIZE
        super()._init_((cx, cy))
        self.body_color = GREEN
        self.length = 1
        self.positions = [(cx, cy)]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None

    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]

    def update_direction(self) -> None:
        if self.next_direction is None:
            return
        ndx, ndy = self.next_direction
        dx, dy = self.direction
        if ndx == -dx and ndy == -dy:
            self.next_direction = None
            return
        self.direction = (ndx, ndy)
        self.next_direction = None

    def move(self) -> Optional[Tuple[int, int]]:
        dx, dy = self.direction
        head_x, head_y = self.get_head_position()
        new_x = (head_x + dx) % SCREEN_WIDTH
        new_y = (head_y + dy) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        removed = None
        if len(self.positions) > self.length:
            removed = self.positions.pop()
        return removed

    def draw(self, surface: pygame.Surface) -> None:
        for pos in self.positions:
            pygame.draw.rect(surface, self.body_color, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    def reset(self) -> None:
        cx = GRID_WIDTH // 2 * CELL_SIZE
        cy = GRID_HEIGHT // 2 * CELL_SIZE
        self.length = 1
        self.positions = [(cx, cy)]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None


def handle_keys(snake: Snake) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key in (pygame.K_UP, pygame.K_w):
                snake.next_direction = (0, -CELL_SIZE)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                snake.next_direction = (0, CELL_SIZE)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                snake.next_direction = (-CELL_SIZE, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                snake.next_direction = (CELL_SIZE, 0)
    return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(snake.positions)

    running = True
    while running:
        running = handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if _name_ == "_main_":
    main()
