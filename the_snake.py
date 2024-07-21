from random import choice

import pygame as pg

PLAYABLE_SCREEN_WIDTH, PLAYABLE_SCREEN_HEIGHT = 640, 480
PLAYABLE_SCREEN_CENTER = ((PLAYABLE_SCREEN_WIDTH // 2),
                          (PLAYABLE_SCREEN_HEIGHT // 2))
GRID_SIZE = 20
GRID_WIDTH = PLAYABLE_SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = PLAYABLE_SCREEN_HEIGHT // GRID_SIZE

ALL_POSITIONS = [
    (x * GRID_SIZE, y * GRID_SIZE) for x in range(GRID_WIDTH) for
    y in range(GRID_HEIGHT)
]

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (255, 255, 255)

APPLE_COLOR = (255, 0, 0)

SNAKE_BODY_COLOR = (0, 128, 0)
SNAKE_HEAD_COLOR = (50, 205, 50)

BASE_SPEED = 15
SPEED_MODIFIERS = {
    range(0, 6): 0,
    range(6, 11): 1,
    range(11, 21): 2,
    range(21, 31): 3,
    range(31, 41): 4,
    range(41, 56): 5,
    range(56, 76): 6,
    range(76, 101): 7,
    range(101, 131): 9,
    range(131, 171): 11,
    range(171, 221): 13,
    range(221, 251): 14,
    range(251, 301): 15
}

SCREEN = pg.display.set_mode((PLAYABLE_SCREEN_WIDTH,
                              PLAYABLE_SCREEN_HEIGHT + 100), depth=32)

SCREEN_FILLER = pg.image.load('screen_img.jpg').convert()
SCOREBOARD_FILLER = pg.image.load('scoreboard.png').convert()

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
        self.position = PLAYABLE_SCREEN_CENTER
        self.body_color = body_color
        self.border_color = border_color

    def draw_square(self, position, color, surface):
        """Draw 20x20 square object"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, color, rect)
        pg.draw.rect(surface, self.border_color, rect, 1)

    def draw(self, surface):
        """Preform method for Snake and Apple cls"""
        raise NotImplementedError("this should never happen")

    @staticmethod
    def display_win_message():
        """Displays 'YOU WIN' message"""
        font = pg.font.Font(None, 74)
        text = font.render("YOU WIN", True, (255, 255, 0))
        text_rect = text.get_rect(center=PLAYABLE_SCREEN_CENTER)
        SCREEN.blit(text, text_rect)
        pg.display.flip()

        end_time = pg.time.get_ticks() + 5 * 1000
        while pg.time.get_ticks() < end_time:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
        pg.quit()


class Apple(GameObject):
    """Game class of 'eatable' apples"""

    def __init__(self, body_color=APPLE_COLOR, border_color=BORDER_COLOR):
        """Apple class constructor"""
        super().__init__(body_color, border_color)
        self.randomize_position()

    @staticmethod
    def available_positions(occupied_positions):
        """Return available positions list"""
        return [pos for pos in ALL_POSITIONS if
                pos not in occupied_positions]

    def randomize_position(self, occupied_positions=None):
        """Change current object position into random non-occupied value"""
        if occupied_positions is None:
            occupied_positions = [PLAYABLE_SCREEN_CENTER]

        free_pos = self.available_positions(occupied_positions)

        if free_pos:
            self.position = choice(free_pos)

    def draw(self, surface):
        """Draw apple cls object"""
        self.draw_square(self.position, self.body_color, surface)


class Snake(GameObject):
    """Game class of sneaky Ss-snake"""

    def __init__(self, body_color=SNAKE_BODY_COLOR, border_color=BORDER_COLOR):
        """Snake class constructor"""
        super().__init__(body_color, border_color)
        self.head_color = SNAKE_HEAD_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
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
        new_snake_x = ((snake_x + self.direction[0] * GRID_SIZE) %
                       PLAYABLE_SCREEN_WIDTH)
        new_snake_y = ((snake_y + self.direction[1] * GRID_SIZE) %
                       PLAYABLE_SCREEN_HEIGHT)
        self.positions.insert(0, (new_snake_x, new_snake_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw_snake_head(self, surface):
        """Draw snake's head"""
        self.draw_square(self.positions[0], self.head_color, surface)

    def draw_full_snake(self, surface):
        """Draw body of the snake and add it's head to it"""
        if len(self.positions) != 1:
            for position in self.positions[1:]:
                self.draw_square(position, self.body_color, surface)
            self.draw_snake_head(surface)
        else:
            self.draw_snake_head(surface)

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
    pg.font.init()
    clock.tick(BASE_SPEED)

    apple = Apple()
    snake = Snake()

    score_font = pg.font.Font('Billabong Cyr.ttf', 40)

    while True:
        actual_speed = BASE_SPEED + SPEED_MODIFIERS[
            next(k for k in SPEED_MODIFIERS.keys() if snake.length in k)
        ]

        clock.tick(actual_speed)

        handle_keys(snake)
        snake.move()

        if apple.position == snake.positions[0]:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.update_direction()

        score = score_font.render(f'Length: {snake.length}', True,
                                  (255, 255, 255))
        speed = score_font.render(f'Speed: {actual_speed}', True,
                                  (255, 255, 255))

        SCREEN.blit(SCREEN_FILLER, (0, 0))
        SCREEN.blit(SCOREBOARD_FILLER, (0, 480))
        SCREEN.blit(score, (47, 512))
        SCREEN.blit(speed, (460, 512))

        snake.draw_full_snake(SCREEN)

        if not apple.available_positions(snake.positions):
            GameObject.display_win_message()

        apple.draw(SCREEN)

        pg.display.update()


if __name__ == '__main__':
    main()
