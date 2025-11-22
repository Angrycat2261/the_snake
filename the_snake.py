import pygame
import random
import sys


class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"
        self.change_to = self.direction

    def change_direction(self, direction):
        self.change_to = direction

    def update_direction(self):
        if self.change_to == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if self.change_to == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if self.change_to == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if self.change_to == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"

    def move(self, food_position):
        self.update_direction()
        
        if self.direction == "RIGHT":
            self.position[0] += 10
        if self.direction == "LEFT":
            self.position[0] -= 10
        if self.direction == "UP":
            self.position[1] -= 10
        if self.direction == "DOWN":
            self.position[1] += 10

        self.body.insert(0, list(self.position))
        
        if (self.position[0] == food_position[0] 
                and self.position[1] == food_position[1]):
            return True
        else:
            self.body.pop()
            return False

    def check_collision(self, window_width, window_height):
        if (self.position[0] > window_width - 10 
                or self.position[0] < 0 
                or self.position[1] > window_height - 10 
                or self.position[1] < 0):
            return True
        
        for segment in self.body[1:]:
            if (self.position[0] == segment[0] 
                    and self.position[1] == segment[1]):
                return True
        
        return False

    def get_head_position(self):
        return self.position

    def get_body(self):
        return self.body


class Food:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.position = self.generate_position()

    def generate_position(self):
        return [
            random.randrange(1, (self.window_width // 10)) * 10,
            random.randrange(1, (self.window_height // 10)) * 10
        ]

    def respawn(self):
        self.position = self.generate_position()

    def get_position(self):
        return self.position


class Game:
    def __init__(self):
        pygame.init()
        
        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption('Snake Game')
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 35)
        
        self.snake = Snake()
        self.food = Food(self.window_width, self.window_height)
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction("RIGHT")
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    def update(self):
        if not self.game_over:
            food_eaten = self.snake.move(self.food.get_position())
            
            if food_eaten:
                self.score += 1
                self.food.respawn()
                while self.food.get_position() in self.snake.get_body():
                    self.food.respawn()
            
            if self.snake.check_collision(
                    self.window_width, self.window_height):
                self.game_over = True

    def render(self):
        self.window.fill((0, 0, 0))
        
        for segment in self.snake.get_body():
            pygame.draw.rect(
                self.window, 
                (0, 255, 0), 
                pygame.Rect(segment[0], segment[1], 10, 10)
            )
        
        pygame.draw.rect(
            self.window,
            (255, 0, 0),
            pygame.Rect(
                self.food.get_position()[0],
                self.food.get_position()[1],
                10,
                10
            )
        )
        
        score_text = self.font.render(
            f'Score: {self.score}', True, (255, 255, 255))
        self.window.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render(
                'Game Over! Press R to restart or Q to quit', 
                True, 
                (255, 255, 255)
            )
            text_rect = game_over_text.get_rect(
                center=(self.window_width // 2, self.window_height // 2)
            )
            self.window.blit(game_over_text, text_rect)
        
        pygame.display.update()

    def restart_game(self):
        self.snake = Snake()
        self.food = Food(self.window_width, self.window_height)
        self.score = 0
        self.game_over = False

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(15)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
