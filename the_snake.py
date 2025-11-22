import pygame
import random
import sys


class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = (10, 0)

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def change_direction(self, new_direction):
        self.direction = new_direction

    def check_collision(self, screen_width, screen_height):
        head = self.body[0]
        return (head[0] < 0 or head[0] >= screen_width or
                head[1] < 0 or head[1] >= screen_height or
                head in self.body[1:])


class Food:
    def __init__(self, screen_width, screen_height):
        self.position = (0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.randomize_position()

    def randomize_position(self):
        x = random.randint(0, (self.screen_width - 10) // 10) * 10
        y = random.randint(0, (self.screen_height - 10) // 10) * 10
        self.position = (x, y)


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Змейка")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food(self.screen_width, self.screen_height)
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_UP and self.snake.direction != (0, 10):
                        self.snake.change_direction((0, -10))
                    elif event.key == pygame.K_DOWN and self.snake.direction != (0, -10):
                        self.snake.change_direction((0, 10))
                    elif event.key == pygame.K_LEFT and self.snake.direction != (10, 0):
                        self.snake.change_direction((-10, 0))
                    elif event.key == pygame.K_RIGHT and self.snake.direction != (-10, 0):
                        self.snake.change_direction((10, 0))
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()

    def update(self):
        if not self.game_over:
            self.snake.move()

            if self.snake.check_collision(self.screen_width, self.screen_height):
                self.game_over = True

            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.food.randomize_position()
                while self.food.position in self.snake.body:
                    self.food.randomize_position()
                self.score += 10

    def draw(self):
        self.screen.fill((0, 0, 0))

        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), 
                           (segment[0], segment[1], 10, 10))

        pygame.draw.rect(self.screen, (255, 0, 0),
                       (self.food.position[0], self.food.position[1], 10, 10))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("ИГРА ОКОНЧЕНА", True, (255, 0, 0))
            restart_text = font.render("Нажмите R для перезапуска", True, (255, 255, 255))
            self.screen.blit(game_over_text, 
                           (self.screen_width // 2 - 180, self.screen_height // 2 - 50))
            self.screen.blit(restart_text,
                           (self.screen_width // 2 - 150, self.screen_height // 2 + 50))

        pygame.display.flip()

    def restart_game(self):
        self.snake = Snake()
        self.food = Food(self.screen_width, self.screen_height)
        self.score = 0
        self.game_over = False

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(15)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
