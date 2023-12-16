# Copyright (c) 2023 @pedro1798
# This code is owned by @pedro1798.
# Unauthorized reproduction and distribution are prohibited.

import pygame
import sys
import random

def generate_random_color():
    return (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

# Pygame 초기화
pygame.init()

# 게임 설정
width, height = 600, 500
cell_size = 20
fps = 10
font_size = 40

# 색깔 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 폰트 설정
font = pygame.font.Font(None, font_size)

# 화면 생성
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
interface_height = 40
interface_colour = (152,151,152)

# 초기 설정
snake = [(100, 100), (90, 100), (80, 100)]
snake_corlour = black
snake_direction = (1, 0)
foods = list()

# 사과 랜덤 리스폰:
def respawn_apple(max):
    for _ in range(1, max + 1):
        while True:
            food = (random.randint(0, (width - cell_size) // cell_size) * cell_size,
            random.randint(interface_height // cell_size, (height - cell_size) // cell_size) * cell_size)
            if food not in snake:
                foods.append(food)
                break

respawn_apple(random.randint(2, 3))

max_score = 0
apple = 0

# 상태 설정
game_over = False
colour_change = False
main_page = True
# 시간 설정
clock = pygame.time.Clock()

# 게임 루프
running = True
while running:
    # 화면을 흰색으로 채우기
    screen.fill(white)
    pygame.draw.rect(screen, interface_colour, (0, 0, width, interface_height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if main_page:
            if event.type == pygame.KEYDOWN:
                main_page = False
        elif event.type == pygame.KEYDOWN:
            if not game_over and not main_page:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)
            else:
                # 게임 오버 상태에서 스페이스바를 누르면 재시작
                if event.key == pygame.K_SPACE:
                    apple = 0
                    fps = 10
                    snake = [(100, 100), (90, 100), (80, 100)]
                    snake_corlour = black
                    snake_direction = (1, 0)
                    food = (random.randint(0, (width - cell_size) // cell_size) * cell_size,
                            random.randint(0, (height - cell_size) // cell_size) * cell_size)
                    game_over = False

    if not game_over and not main_page:
        # Snake 이동
        x, y = snake[0]
        x += snake_direction[0] * cell_size
        y += snake_direction[1] * cell_size
        snake.insert(0, (x, y))

        # 사과를 먹었는지 확인
        if snake[0] in foods:
            apple += 1
            foods.remove(snake[0])
            if len(foods) <= 2:
                respawn_apple(2)
        else:
            snake.pop()

        # 충돌 검사
        if (x < 0 or x >= width or y < 0 or y >= height or
                any(segment == snake[0] for segment in snake[1:])):
            game_over = True

        # Snake 색 변경, 속도 증가
        if apple != 0 and apple % 10 == 0:
            fps *= 1.002
            if not colour_change:
                snake_corlour = generate_random_color()
            colour_change = True
        else:
            colour_change = False

        # Snake 그리기
        for segment in snake:
            pygame.draw.rect(screen, snake_corlour, (segment[0], segment[1], cell_size, cell_size))

        # 먹이 그리기
        for food in foods:
            pygame.draw.rect(screen, red, (food[0], food[1], cell_size, cell_size))

    elif game_over:
        # 게임 오버 화면 표시
        if apple <= 3:
            game_over_text = font.render("Maggot!", True, black)
        elif apple <= 15:
            game_over_text = font.render("You Just Smashed This Tiny Snake...", True, black)
        elif apple <= 25:
            game_over_text = font.render("One More Game?", True, black)
        elif apple <= 35:
            game_over_text = font.render("Ouch!", True, black)
        elif apple <= 40:
            game_over_text = font.render("Anaconda", True, black)
        else:
            game_over_text = font.render("Titanoboa cerrejonensis", True, black)
        screen.blit(game_over_text, ((width - game_over_text.get_width()) // 2, height // 2 - 25))

        max_score = max(max_score, apple)
        max_score_text = font.render(f"Max Score is.. {max_score}", True, black)
        screen.blit(max_score_text, ((width - max_score_text.get_width()) // 2, height // 2))

        restart_text = font.render("Press SPACE to Restart", True, black)
        screen.blit(restart_text, ((width - restart_text.get_width()) // 2, height // 2 + 25))

    else:
        game_start_text = font.render("Press Any Key to Start", True, black)
        screen.blit(game_start_text, ((width - game_start_text.get_width()) // 2, height // 2 - 25))

    # 인터페이스 그리기
    github_url = font.render(f"@pedro1798", True, (199,199,199))
    screen.blit(github_url, (width - github_url.get_width() - 20, interface_height / 4))

    if apple == 42:
        apple_interface = font.render(f"Answer to life the universe and everything: {str(apple)}", True, black)
    elif apple != 0 and apple % 10 == 0:
        apple_interface = font.render(f"Speed Up!: {str(apple)}", True, black)
    elif apple == 35:
        apple_interface = font.render(f"Wow, This snake must swallowed an  elephant!: {str(apple)}", True, black)
    elif apple != 0 and apple % 13 == 0:
        apple_interface = font.render(f"Snake on a Plane: {str(apple)}", True, black)
    elif 45 <= apple < 47:
        apple_interface = font.render(f"Did you know?: {str(apple)}", True, black)
    elif 47 <= apple <= 49:
        apple_interface = font.render(f"Snakes have two penises: {str(apple)}", True, black)
    else:
        apple_interface = font.render(f"Current Score: {str(apple)}", True, black)

    screen.blit(apple_interface, ((15, interface_height / 4)))

    # 화면 업데이트
    pygame.display.flip()

    # 초당 프레임 수 업데이트
    clock.tick(fps)

# Pygame 종료
pygame.quit()
sys.exit()