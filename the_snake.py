from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 720
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (255, 255, 255)

# Цвет яблока
APPLE_COLOR = (128, 0, 32)

# Цвет змейки
SNAKE_COLOR = (0, 78, 56)

# Скорость движения змейки:
SPEED = 17

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Pythot by HarisNvr')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Transform keys pushing into game action"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Тут опишите все классы игры.ю
class GameObject:
    """Base game object class"""

    def __init__(self, body_color=None):
        """Parent class constructor"""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self, surface):
        """Preform method for Snake and Apple cls"""
        pass


class Apple(GameObject):
    """Game class of 'eatable' apples"""

    def __init__(self, body_color=APPLE_COLOR):
        """Apple class constructor"""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Change current object position into random value"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Draw apple cls object"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Game class of sneaky Sssnake"""

    def __init__(self, body_color=SNAKE_COLOR):
        """Snake class constructor"""
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Replace current direction value with new direction value"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Insert tuple with X,Y cords into positions list
        and pop the last value
        """
        snake_x, snake_y = self.get_head_position()
        new_snake_x = (snake_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_snake_y = (snake_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_snake_x, new_snake_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Draw head and body of the snake cls object"""
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Return value of the first element in positions list"""
        return self.positions[0]

    def reset(self):
        """
        'Soft' game restart - snake length reduces to 1
        and reset its position to default value
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])


def main():
    """Game body"""
    running = True
    clock.tick(SPEED)

    apple = Apple()
    snake = Snake()

    while running:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        # Основная логика игры.
        if apple.position == snake.positions[0]:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
