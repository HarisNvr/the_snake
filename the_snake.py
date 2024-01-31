from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (255, 255, 255)

APPLE_COLOR = (128, 0, 32)

SNAKE_COLOR = (0, 78, 56)

SPEED = 15

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Pythot by HarisNvr')

clock = pg.time.Clock()


def handle_keys(game_object):
    """Transform keys pushing into game action"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


class GameObject:
    """Base game object class"""

    def __init__(self, body_color=None, border_color=None):
        """Parent class constructor"""
        self.position = SCREEN_CENTER
        self.body_color = body_color
        self.border_color = border_color
        self.border_color = BORDER_COLOR

    def draw(self, surface):
        """Preform method for Snake and Apple cls"""
        raise NotImplementedError("this should never happen")


def generate_random_position():
    """Generates random tuple with (X, Y) cords"""
    return (
        randint(0, GRID_WIDTH - 1) * GRID_SIZE,
        randint(0, GRID_HEIGHT - 1) * GRID_SIZE
    )


class Apple(GameObject):
    """Game class of 'eatable' apples"""

    fill_apple_debug = 100

    def __init__(self, body_color=None, border_color=None):
        """Apple class constructor"""
        super().__init__(body_color, border_color)
        self.randomize_position([SCREEN_CENTER])

    def randomize_position(self, snake_position):
        """Change current object position into random value"""
        attempts = 0
        while attempts < Apple.fill_apple_debug:
            rand_position = generate_random_position()
            if (rand_position not in snake_position
                    and rand_position != SCREEN_CENTER):
                self.position = rand_position
                break
            attempts += 1

    def draw(self, surface):
        """Draw apple cls object"""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, self.border_color, rect, 1)


class Snake(GameObject):
    """Game class of sneaky Sssnake"""

    def __init__(self, body_color=None, border_color=None):
        """Snake class constructor"""
        super().__init__(body_color, border_color)
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
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, self.border_color, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, self.border_color, head_rect, 1)

    def get_head_position(self):
        """Return value of the first element in positions list"""
        return self.positions[0]

    def reset(self):
        """
        Soft game restart - snake length reduces to 1
        and reset its position to default value
        """
        self.length = 1
        self.positions = [self.position]
        self.next_direction = choice([LEFT, RIGHT, UP, DOWN])


def main():
    """Game body"""
    pg.init()
    clock.tick(SPEED)

    apple = Apple(APPLE_COLOR, BORDER_COLOR)
    snake = Snake(SNAKE_COLOR, BORDER_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        if apple.position == snake.positions[0]:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)

        pg.display.update()


if __name__ == '__main__':
    main()
