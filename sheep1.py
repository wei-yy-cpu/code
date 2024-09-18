import pygame
import random
import sys

# ... (之前的代码保持不变)
# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 645
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
MAX_TIME = 30  # 游戏最大时间（秒）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (200, 200, 200)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("羊了个羊小游戏")

# 字体设置
font = pygame.font.Font(None, 36)

# 加载图案图片
patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 7)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 加载游戏画面图片
start_screen_img = pygame.image.load("start_screen.png")
start_screen_img = pygame.transform.scale(start_screen_img, (WIDTH, HEIGHT))
end_screen_img = pygame.image.load("end_screen.png")
end_screen_img = pygame.transform.scale(end_screen_img, (WIDTH, HEIGHT))

# 创建游戏板
board = [[random.choice(patterns) for _ in range(COLS)] for _ in range(ROWS)]
selected = []

# 记录游戏开始时间
start_time = 0


# 定义按钮的位置和大小
BUTTON_X, BUTTON_Y = WIDTH // 2 , HEIGHT // 2   # 按钮中心位置
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 100

# 按钮颜色
BUTTON_COLOR = (2, 255, 2)
BUTTON_TEXT = "Start"

# 初始化分数
score = 0
# 定义难度级别和对应的图案数量
DIFFICULTIES = {
    'easy': 2,
    'medium': 5,
    'hard': 7
}

# 初始化难度级别
difficulty = 'easy'  # 默认难度为easy


# 加载图案图片
def load_patterns(difficulty):
    num_patterns = DIFFICULTIES[difficulty]
    patterns = [pygame.image.load(f"pattern_{i + 1}.png") for i in range(num_patterns)]
    patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]
    return patterns


patterns = load_patterns(difficulty)

# ... (之前的代码保持不变，直到显示开始画面的函数)
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))


def draw_timer(time_left):
    timer_text = font.render(f"Time Left: {int(time_left):02d}", True, (255, 0, 0))
    timer_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT - timer_text.get_height() - 10))
    screen.blit(timer_text, timer_rect)


def game_over_screen(final_score):
    screen.blit(end_screen_img, (0, 0))
    final_score_text = font.render(f"Game Over\nScore: {final_score}", True, (255, 255, 255))
    final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(final_score_text, final_score_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def win_screen(final_score):
    screen.blit(end_screen_img, (0, 0))
    win_score_text = font.render(f"You Win!\nScore: {final_score}", True, (255, 255, 255))
    win_score_rect = win_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(win_score_text, win_score_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def check_match():
    global score  # 声明score为全局变量
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if board[r1][c1] == board[r2][c2]:
            board[r1][c1] = None
            board[r2][c2] = None
            score += 10  # 成功匹配，增加分数
        selected.clear()

    # ... (显示分数的函数)


def draw_score(score):
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    score_rect = score_text.get_rect(center=(WIDTH // 2, 10))  # 放置在窗口顶部中央
    screen.blit(score_text, score_rect)


def is_game_won():
    for row in board:
        for tile in row:
            if tile is not None:
                return False
    return True


font = pygame.font.Font(None, 36)  # 假设你已经定义了这个字体


def show_difficulty_screen():
    screen.fill(BG_COLOR)

    # 显示难度选择
    font_large = pygame.font.Font(None, 48)
    title_text = font_large.render("Choose Difficulty", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    # 绘制难度按钮
    y_offset = 200
    button_colors = [(0, 255, 0), (255, 255, 0), (255, 0, 0)]
    difficulties = ['easy', 'medium', 'hard']

    for diff, color in zip(difficulties, button_colors):
        pygame.draw.rect(screen, color,
                         (BUTTON_X - BUTTON_WIDTH // 2, y_offset - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT))
        button_text = font.render(diff, True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(BUTTON_X, y_offset))
        screen.blit(button_text, button_rect)
        y_offset += BUTTON_HEIGHT + 20

    pygame.display.flip()

    # 等待按钮点击
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                y_offset = 200  # 重置y_offset
                for diff, color in zip(difficulties, button_colors):
                    if BUTTON_X - BUTTON_WIDTH // 2 <= x <= BUTTON_X + BUTTON_WIDTH // 2:
                        if y_offset - BUTTON_HEIGHT // 2 <= y <= y_offset + BUTTON_HEIGHT // 2:
                            return diff  # 直接返回难度级别
                    y_offset += BUTTON_HEIGHT + 20

        pygame.display.flip()

def show_start_screen():
    screen.fill(BG_COLOR)
    screen.blit(start_screen_img, (0, 0))

    # 绘制开始按钮
    pygame.draw.rect(screen, BUTTON_COLOR,
                     (BUTTON_X - BUTTON_WIDTH // 2, BUTTON_Y - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT))
    button_text = font.render("Start", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(BUTTON_X, BUTTON_Y))
    screen.blit(button_text, button_rect)

    # 绘制退出按钮
    EXIT_BUTTON_Y = BUTTON_Y + BUTTON_HEIGHT + 20  # 位于开始按钮下方
    pygame.draw.rect(screen, (255, 0, 0),  # 使用红色作为退出按钮的颜色
                     (BUTTON_X - BUTTON_WIDTH // 2, EXIT_BUTTON_Y - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT))
    exit_button_text = font.render("Exit", True, (255, 255, 255))
    exit_button_rect = exit_button_text.get_rect(center=(BUTTON_X, EXIT_BUTTON_Y))
    screen.blit(exit_button_text, exit_button_rect)

    pygame.display.flip()

    # 等待按钮点击
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # 检查是否点击了开始按钮
                if BUTTON_X - BUTTON_WIDTH // 2 <= x <= BUTTON_X + BUTTON_WIDTH // 2 and \
                        BUTTON_Y - BUTTON_HEIGHT // 2 <= y <= BUTTON_Y + BUTTON_HEIGHT // 2:
                    return  # 返回表示开始按钮被点击
                # 检查是否点击了退出按钮
                elif BUTTON_X - BUTTON_WIDTH // 2 <= x <= BUTTON_X + BUTTON_WIDTH // 2 and \
                        EXIT_BUTTON_Y - BUTTON_HEIGHT // 2 <= y <= EXIT_BUTTON_Y + BUTTON_HEIGHT // 2:
                    pygame.quit()
                    sys.exit()  # 退出游戏

        pygame.display.flip()
    # ... (之后的代码保持不变)
running = True
clock = pygame.time.Clock()

# 显示开始画面并等待按钮点击
show_start_screen()
# 显示难度选择画面并等待选择
show_difficulty_screen()

# 重新加载图案以适应选择的难度
patterns = load_patterns(difficulty)

# 初始化游戏板
board = [[random.choice(patterns) for _ in range(COLS)] for _ in range(ROWS)]
# ... (之后的代码保持不变，游戏循环开始)
while running:
    clock.tick(FPS)

    if not start_time:
        start_time = pygame.time.get_ticks()

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000
    time_left = max(MAX_TIME - elapsed_time, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // TILE_SIZE, y // TILE_SIZE
            if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] is not None:
                if (row, col) not in [(s[0], s[1]) for s in selected]:
                    selected.append((row, col))
                if len(selected) == 2:
                    check_match()

    screen.fill(BG_COLOR)
    draw_board()
    draw_timer(time_left)
    draw_score(score)  # 在游戏界面上实时显示分数

    if time_left <= 0:
        running = False
        game_over_screen(score)  # 传递分数到游戏结束画面函数
    elif is_game_won():
        running = False
        win_screen(score)  # 传递分数到胜利画面函数

    pygame.display.flip()

pygame.quit()
sys.exit()


