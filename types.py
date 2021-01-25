import random
import pygame


class RGB():

    def __init__(self, color):
        self.rgb = color
        self.r = color[0]*255
        self.g = color[1]*255
        self.b = color[2]*255


class vec2():

    def __init__(self, vec):
        self.xy = vec
        self.x = vec[0]
        self.y = vec[1]


class GAME_WINDOW():

    def __init__(self, width, height, fps, window_name="New Window"):
        self.width = width
        self.height = height
        self.fps = fps
        self.running = True
        self.window_name = window_name

        pygame.init()
        pygame.mixer.init()
        self.field = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(window_name)
        self.clock = pygame.time.Clock()

    def update(self):
        self.clock.tick(self.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def stop(self):
        pygame.quit()


class KEYBOARD():
    def __init__(self, key):
        pass

    def is_pressed(self):
        pass

    def is_down(self):
        pass


class BLOCK():

    def __init__(self, window, pos, size, _id, fill):
        self.pos = pos
        self.size = size
        self.id = _id
        self.fill = fill
        self.window = window

    def draw(self):
        block = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        frame = True
        if self.fill == "EMPTY":
            color = (0, 0, 0)
            frame = False

        if self.fill == "SNAKE":
            color = (255, 255, 0)

        if self.fill == "FOOD":
            color = (255, 0, 0)

        if self.fill == "DEBUG":
            color = (0, 255, 255)

        pygame.draw.rect(self.window.field, color, block)
        if frame:
            pygame.draw.rect(self.window.field, (255, 255, 255), block, 1)
        pygame.draw.rect(self.window.field, (20, 20, 20), block, 1)

    def is_empty(self):
        if self.fill == "EMPTY":
            return True
        else:
            return False

    def is_snake(self):
        if self.fill == "SNAKE":
            return True
        else:
            return False

    def is_food(self):
        if self.fill == "FOOD":
            return True
        else:
            return False


class FIELD():
    def __init__(self, window, linecount):
        self.w = window.width
        self.h = window.height
        self.linecount = linecount
        self.blocks = []

        last_id = 0
        for iy in range(0, int(self.w/(self.w/linecount))):
            for ix in range(0, int(self.h/(self.h/linecount))):
                last_id += 1
                _id = last_id

                block_x = (self.w/linecount)*(ix)
                block_y = (self.h/linecount)*(iy)

                pos = vec2([block_x, block_y])
                size = vec2([self.w/linecount, self.h/linecount])

                block = BLOCK(window, pos, size, _id-1, "EMPTY")
                self.blocks.append(block)


class SNAKE():
    def __init__(self, field):
        self.live = True
        self.snake = []
        self.field = field
        self.direction = "UP"
        self.food = FOOD(self.field, self.snake)

    def check_next_step(self, head, direction):
        try:
            if direction == "DOWN":
                block = self.field.blocks[head.id + self.field.blocks[self.field.linecount].id]
        except:
            block = self.field.blocks[int(head.id/self.field.linecount)]

        if direction == "UP":
            block = self.field.blocks[head.id-self.field.blocks[self.field.linecount].id]
        if direction == "LEFT":
            block = self.field.blocks[head.id-1]

        try:
            if direction == "RIGHT":
                block = self.field.blocks[head.id+1]
        except:
            block = self.field.blocks[0]

        return block

    def move(self, direction):
        if direction != "MAIN":
            block = self.check_next_step(self.snake[0], direction)
            self.direction = direction
        else:
            block = self.check_next_step(self.snake[0], self.direction)

        if block.fill == "SNAKE":
            self.live = False
            return

        if block.fill == "EMPTY":
            self.snake[-1].fill = "EMPTY"
            self.snake.remove(self.snake[-1])

        if block.fill == "FOOD":
            block.fill = "SNAKE"
            FOOD(self.field, self.snake)

        self.snake[0] = block
        self.snake.insert(0, block)
        self.snake[0].fill = "SNAKE"

    def create(self):
        start = int(len(self.field.blocks)/2) - int(self.field.linecount/2)
        head = self.field.blocks[start]
        tail = self.check_next_step(head, "DOWN")

        self.snake = [head, tail]
        for block in self.snake:
            block.fill = "SNAKE"


class FOOD():

    def __init__(self, field, snake):
        self.spawn = False
        self.place = 0
        self.blocks = field.blocks.copy()

        for block in snake:
            try:
                self.blocks.remove(block)
            except(ValueError):
                pass

        self.place = random.choice(self.blocks)
        field.blocks[self.place.id].fill = "FOOD"
