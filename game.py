import pygame
import random

# 初始化游戏
pygame.init()

# 设置游戏窗口的大小
screen_width = 800
screen_height = 600
play_width = 300
play_height = 600
block_size = 30

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height

# 定义方块形状和颜色
S = [['.....',
      '.....',
      '..00.',
      '.00..',
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

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
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
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# 定义方块类
class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


# 创建游戏区域
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(Piece.columns)] for _ in range(Piece.rows)]

    for row in range(len(grid)):

        for col in range(len(grid[row])):
            if (col, row) in locked_positions:
                color = locked_positions[(col, row)]
                grid[row][col] = color

    return grid


# 将方块的形状转换为坐标
def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# 检查是否可以在给定位置放置方块
def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(Piece.columns) if grid[i][j] == (0, 0, 0)] for i in range(Piece.rows)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


# 检查游戏是否结束
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# 从给定位置消除行
def clear_rows(grid, locked):
    full_rows = [i for i, row in enumerate(grid) if (0, 0, 0) not in row]

    for row in full_rows:
        del grid[row]
        grid.insert(0, [(0, 0, 0) for _ in range(Piece.columns)])

    for row in full_rows:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < row:
                new_key = (x, y + 1)
                locked[new_key] = locked.pop(key)

    return len(full_rows)


# 绘制游戏区域
def draw_grid(surface, grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(surface, grid[row][col], (top_left_x + col * block_size,
                                                       top_left_y + row * block_size,
                                                       block_size, block_size))
            pygame.draw.rect(surface, (0, 0, 0), (top_left_x + col * block_size,
                                                  top_left_y + row * block_size,
                                                  block_size, block_size), 1)


# 绘制方块
def draw_piece(surface, piece):
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (top_left_x + (piece.x + j) * block_size,
                                                        top_left_y + (piece.y + i) * block_size,
                                                        block_size, block_size))
                pygame.draw.rect(surface, (0, 0, 0), (top_left_x + (piece.x + j) * block_size,
                                                      top_left_y + (piece.y + i) * block_size,
                                                      block_size, block_size), 1)


# 绘制游戏界面
def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width + 50, 100))

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(surface, grid[row][col], (top_left_x + col * block_size,
                                                       top_left_y + row * block_size,
                                                       block_size, block_size))
            pygame.draw.rect(surface, (0, 0, 0), (top_left_x + col * block_size,
                                                  top_left_y + row * block_size,
                                                  block_size, block_size), 1)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


# 主函数
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Piece(5, 0, random.choice(shapes))
    next_piece = Piece(5, 0, random.choice(shapes))
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1

                ])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = Piece(5, 0, random.choice(shapes))
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)
        draw_piece(win, current_piece)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_window(win, grid, score)
    pygame.time.delay(2000)


win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

main()