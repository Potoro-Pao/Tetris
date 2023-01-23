import pygame
import random

pygame.init()

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]


class Block:
    def __init__(self, x, y):
        bricks = random.choice(shapes)
        self.x = x
        self.y = y
        self.rotation = 0
        self.bricks = bricks

    @staticmethod
    def output_shape():
        position = []
        for num1, first_layer in enumerate(block.bricks[block.rotation]):
            ripped = list(first_layer)
            for num2, new_brick in enumerate(ripped):
                if new_brick == ".":
                    pass
                    # print(" ", end="")
                else:
                    # print("0", end="")
                    position.append((num1, num2))
            # print(" ")
        return position


block = Block(5, 0)

window_width = 1000
window_height = 1020
block_size = 50
row_size_start = window_width // 3
row_size_end = window_width - (window_width // 3)
total_row = row_size_end // block_size
total_height = window_height // block_size

win_size = (window_width, window_height)
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Tetris")
game_over = False
bg = pygame.Surface(win.get_size())
bg = bg.convert()
bg.fill((0, 0, 0))


def display_score(score):
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render("Score", 1, (255, 255, 255))
    text2 = font.render(str(score), 1, (255, 255, 255))
    win.blit(text, (800 - (text.get_width() // 2), (200 - (text.get_height() // 2))))
    win.blit(text2, (850 - (text.get_width() // 2), (300 - (text.get_height() // 2))))


def display_game_over():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render('Game Over!', 1, (255, 255, 255))
    space = win.blit(text, (300 - (text.get_width() // 2), (win.get_height() // 2)))


def display_author():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Created by Potoro Pao', 1, (255, 255, 255))
    text2 = font.render('Special Thanks to Anfy Pao', 1, (255, 255, 255))
    win.blit(text, (win.get_width() - text.get_width() - 70, 550))
    win.blit(text2, (win.get_width() - text.get_width() - 60, 600))


def display_bricks(shape_location):
    blue_brick = dict()
    for i in shape_location:
        blue_brick[i] = (20, 123, 200)
        for brick_pos in blue_brick:
            pygame.draw.rect(win, blue_brick[brick_pos],
                             ((brick_pos[1] + block.x) * block_size - 37,
                              (brick_pos[0] + block.y) * block_size - 31,
                              block_size, block_size))

    return blue_brick


def collide(nx, ny):
    collision = False
    if (nx, ny) in block_position and game_board[(ny + block.x, nx + block.y + 1)] != (0, 0, 0):
        collision = True

    return collision


def drop():
    can_drop = True
    for y in range(5):
        for x in range(5):
            if (y, x) in block_position:
                if block.y + y >= total_height - 1 or collide(y, x):
                    can_drop = False
                    return False

    if can_drop:
        block.y += 1


def move(dx):
    can_move = True
    for y in range(5):
        for x in range(5):
            if (y, x) in block_position:
                if block.x + x >= total_row - 1 and dx == 1:
                    can_move = False
                elif block.x + x < 2 and dx == -1:
                    can_move = False
                    return False

    if can_move:
        block.x += dx


# initialize a background gameboard
game_board = {}

for i in range(total_row):
    for j in range(total_height):
        game_board[(i, j)] = (0, 0, 0)


def display_board(game_board):
    for (x, y) in game_board:
        if game_board[(x, y)] != (0, 0, 0):
            pygame.draw.rect(win, game_board[(x, y)],
                             (x * block_size - 37,
                              y * block_size - 31,
                              block_size, block_size))


score = 0


def clear_lines():
    s = 0
    color_pos = []
    backward = []
    backward_lbl = []
    # make sure the tuples in gameboard is read horizontally
    for (x, y) in game_board:
        color_pos.append((x, y))
    check_line = sorted(color_pos, key=lambda x: x[1])
    # make sure the tuples is read horizontally backward
    for (x, y) in check_line[::-1]:
        backward.append((x, y))
    # reconstruct the color position(tuples) "line by line" (list within in list) based on the y
    for items in range(19, -1, -1):
        game_board_reverse = [grids for grids in backward if grids[1] == items]
        backward_lbl.append(game_board_reverse)
        # check game board backward line by line
        # if the line is full then we will delete the whole line

    for lines_num, lines in enumerate(backward_lbl):
        count = 0
        for pos in lines:
            if game_board[pos] == (128, 128, 128):
                count += 1
        # at this point the loop runs the whole gameboard to check
        # print(f"{line_num} line has {count} filled")
        if count == len(lines) - 1:
            s += 1  # score
            for (x, y) in lines:
                game_board[(x, y)] = game_board[(x, y - 1)]
                for i in range(1, total_height - 2):
                    try:
                        game_board[(x, y - i)] = game_board[(x, y - i - 1)]
                    except:
                        continue
    return s


# --------------------------------------------------------
clock = pygame.time.Clock()
FPS = 10

#main game loop

while not game_over:
    win.blit(bg, (0, 0))
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                last_rotation = block.rotation
                block.rotation = (block.rotation + 1) % len(block.bricks)
                can_rotate = True

                for y in range(5):
                    for x in range(5):
                        # I want to prevent brick from going outside of grid during rotation
                        if (x, y) in block_position:
                            if block.y + y >= total_height - 2:
                                can_rotate = False
                            if block.y + y < 0:
                                can_rotate = False
                            if block.x + x >= total_row:
                                block.x -= 1
                            if block.x + x <= 1:
                                block.x += 1
                if can_rotate == False:
                    block.rotation = last_rotation
#speed up the block
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                while drop()!=False:
                    for y in range(5):
                        for x in range(5):
                            if (x, y) in block_position:
                                if block.y + y <= total_height - 1:
                                    break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move(-1)
            if event.key == pygame.K_RIGHT:
                move(1)
# produce the block
    block_position = block.output_shape()
    blue_brick = display_bricks(block_position)
    display_board(game_board)

# if you press arrow keys then the bricks won't move
    if event.type != pygame.KEYDOWN:
        if drop() == False:
            for (x, y) in blue_brick:  # the dictionary will record the color of stone once the block reach bottom.
                game_board[(y + block.x, x + block.y)] = (128, 128, 128)
                score += clear_lines()
            if block.y == 0:
                display_game_over()
                display_author()
                game_over = True

            new_block = Block(6, 0)
            block = new_block
    display_score(score)
 # display the grids
    for i in range(total_row):
        for j in range(total_height):
            pygame.draw.rect(win, (255, 255, 255), (total_row, total_height, block_size * i, block_size * j), 1)

    pygame.display.update()
pygame.quit()