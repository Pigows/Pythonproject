import pygame
import random

pygame.font.init()
# sử dụng font từ tệp

s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block   ,    chiều rộng khối 
play_height = 600  # meaning 600 // 20 = 30 height per block ,    chiều cao khối   10x20 pixel
block_size = 30
# thông số khối
top_left_x = (s_width - play_width)  // 2
top_left_y = s_height - play_height
# căn lề cho khung chơi 


# DÙng danh sách đa chiều để vẽ khối
# Những số 0 đại diện cho khối
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
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)] # Khai báo màu
# chỉ số từ 0 - 6 đại diện cho hình dạng 
# hệ màu RGB

class Piece(object):  
    def __init__(self, x, y, shape):                    
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
# Dùng hàm khởi tạo để tạo các thông số ban đầu cho khối
# Lưu trữ thông tin về mỗi hình dạng

def create_grid(locked_pos={}):  # *
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)] #Toàn bộ lưới 20 x 10 đều màu đen

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid
# Tạo danh sách lưới gồm 20 hàng và 10 cột 
# locked_pos sẽ giữ cái mảnh đã rơi và khóa vị trí của chúng để sửa màu ở ô lưới này thành màu của mảnh .

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions
# Chuyển đổi dữ liệu danh sách đa chiều thành một danh sách vị trí có thể trả về 
# Dịch danh sách đa chiều thành một dạng máy tính hiểu được

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)] # vị trí cho phép 
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape) # Đã định dạng 

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True
# Kiểm tra xem ô lưới đã có màu hay chưa , nếu có thì không đc rơi vào , còn ko thì tự do


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False
# Kiểm tra xem có phần tử nào trong danh sách ở vị trí chạm đỉnh hay không ( nghĩa là vị trí < 1 )

def get_shape():
    return Piece(5, 0, random.choice(shapes))
# Random.Choice giúp tạo một mảnh ngẫu nhiên rơi xuống màn hình


def draw_text_middle(surface, text, size, color): # Hỗ trợ tạo văn bản ở giữa màn hình
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))
# Hàm này dùng để vẽ các đường lưới bằng draw.line 

def clear_rows(grid, locked):   # Hàm dùng để xóa các hàng đã đầy vị trí

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            # Thêm vị trí cần xóa từ vị trí đã khóa
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)] # Xóa hàng
                except:
                    continue

# Khi xóa một hàng lưới , ta sẽ thêm một hàng lưới ở trên cùng và đẩy lưới xuống .
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc) # Thêm một hàng khóa mới phía trên
                locked[newKey] = locked.pop(key)

    return inc



def draw_next_shape(shape, surface):            # Hiển thị hình dạng rơi tiếp theo ở phía phải màn hình
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255)) # Hiển thị chữ Next Shape

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):    # Tạo các hình khối 
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

# Cập nhật file scores.txt mỗi khi kết thúc trò chơi để lưu lại điểm
def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score=0, last_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60) # Giúp gọi đc phương thức Render
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # ĐIểm hiện tại
    font = pygame.font.SysFont('comicsans', 25)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    
    # Điểm cao nhất 
    label = font.render('High Score: ' + last_score, 2, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 10, sy + 160))

    for i in range(len(grid)):       # Vẽ lưới 
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    #pygame.display.update()


def main(win):  # *
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
# Chạy vòng lặp trò chơi
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

# Tăng tốc độ rơi
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

# Điều khiển khối khi rơi
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)): # thiết lập để khối không bị ra khỏi khung chơi
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

#  Thêm màu của khối vô lưới để vẽ
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:     # Nếu ta không ở trên đỉnh màn hình
                grid[y][x] = current_piece.color

#  Khi khối hình chạm đất 
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10 # Tính điểm +10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):                           # Nếu thua thì hiện YOU LOST và chơi lại
            draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score) # Lưu lại điểm cao nhất vừa chơi


def main_menu(win):  # Màn hình bắt đầu , và giúp ngưới có thể bắt đầu trò chơi bằng bất kì phím nào
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()

# Thiết lập cửa sổ game
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)