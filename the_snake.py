import pygame
import random
import sys

class GameObject:
    def _init_(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color
    
    def draw(self, surface):
        pass

class Apple(GameObject):
    def _init_(self, position=(0, 0)):
        super()._init_(position, (255, 0, 0))
        self.randomize_position()
    
    def randomize_position(self):
        x = random.randint(0, 31) * 20
        y = random.randint(0, 23) * 20
        self.position = (x, y)
    
    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], 20, 20)
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)

class Snake(GameObject):
    def _init_(self, position=(320, 240)):
        super()._init_(position, (0, 255, 0))
        self.positions = [position]
        self.direction = (20, 0)
        self.next_direction = None
        self.length = 1
    
    def update_direction(self):
        if self.next_direction:
            opposite_directions = {
                (20, 0): (-20, 0),
                (-20, 0): (20, 0),
                (0, 20): (0, -20),
                (0, -20): (0, 20)
            }
            
            current_opposite = opposite_directions.get(self.direction)
            if self.next_direction != current_opposite:
                self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        new_head = self._handle_wall_collision(new_head)
        
        self.positions.insert(0, new_head)
        
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def _handle_wall_collision(self, position):
        x, y = position
        
        if x >= 640:
            x = 0
        elif x < 0:
            x = 620
        if y >= 480:
            y = 0
        elif y < 0:
            y = 460
            
        return (x, y)
    
    def get_head_position(self):
        return self.positions[0]
    
    def grow(self):
        self.length += 1
    
    def reset(self):
        self.positions = [self.position]
        self.direction = (20, 0)
        self.next_direction = None
        self.length = 1
    
    def check_self_collision(self):
        head = self.get_head_position()
        return head in self.positions[1:]
    
    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], 20, 20)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)

def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -20)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, 20)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-20, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (20, 0)

def main():
    pygame.init()
    
    window_width = 640
    window_height = 480
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Изгиб Питона')
    
    snake = Snake()
    apple = Apple()
    
    clock = pygame.time.Clock()
    
    while True:
        handle_keys(snake)
        
        snake.update_direction()
        snake.move()
        
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
        
        if snake.check_self_collision():
            snake.reset()
        
        window.fill((0, 0, 0))
        
        snake.draw(window)
        apple.draw(window)
        
        pygame.display.update()
        
        clock.tick(10)

if _name_ == "_main_":
    main()
