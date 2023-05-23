import pygame
import random

# Game dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 80
BALL_SIZE = 15

# Speeds
PADDLE_SPEED = 5
BALL_SPEED = 4
BALL_SPEED_INCREMENT = 0.05

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Create paddles
paddle1 = pygame.Rect(0, SCREEN_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create initial ball
balls = [{
    'rect': pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_SIZE, BALL_SIZE),
    'dx': BALL_SPEED * random.choice((-1, 1)),
    'dy': BALL_SPEED * random.choice((-1, 1)),
    'original': True,  # Flag to identify the original ball
}]

# Scoring
score1 = 0
score2 = 0
high_score = 0

# Game mode (True = multiplayer, False = single player)
multiplayer = True

# Game states
game_over = False
pause = False
in_menu = True

def reset_ball(ball):
    ball['rect'].center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ball['dx'] = BALL_SPEED * random.choice((-1, 1))
    ball['dy'] = BALL_SPEED * random.choice((-1, 1))
    ball['original'] = True  # Set original flag for the reset ball

def split_ball(ball):
    if ball['original']:
        ball['original'] = False  # Reset the original flag for the original ball
        for _ in range(2):  # add two new balls
            new_ball = {
                'rect': pygame.Rect(ball['rect'].centerx, ball['rect'].centery, BALL_SIZE, BALL_SIZE),
                'dx': BALL_SPEED * random.choice((-1, 1)),
                'dy': BALL_SPEED * random.choice((-1, 1)),
                'original': False,  # Set original flag for the new balls
            }
            balls.append(new_ball)

def draw_objects():
    screen.fill(BLACK)

    if in_menu:
        font = pygame.font.Font(None, 36)
        title_text = font.render("Pong Game", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, SCREEN_HEIGHT / 2 - title_text.get_height() / 2))

        start_text = font.render("Press Enter to Start", True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH / 2 - start_text.get_width() / 2, SCREEN_HEIGHT / 2 + 50))

        mode_text = font.render("Press 1 for Single Player, 2 for Multiplayer", True, WHITE)
        screen.blit(mode_text, (SCREEN_WIDTH / 2 - mode_text.get_width() / 2, SCREEN_HEIGHT / 2 + 100))
    else:
        pygame.draw.rect(screen, WHITE, paddle1)
        pygame.draw.rect(screen, WHITE, paddle2)

        if not game_over:  # Draw balls only when the game is not over
            for ball in balls:
                pygame.draw.rect(screen, WHITE, ball['rect'])

        font = pygame.font.Font(None, 36)
        text = font.render(f"Player 1 Score: {score1}", True, WHITE)
        screen.blit(text, (20, 10))
        text = font.render(f"Player 2 Score: {score2}", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - 200, 10))

    if game_over:
        # Display game over text
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2))

        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH / 2 - high_score_text.get_width() / 2, SCREEN_HEIGHT / 2 + 50))

        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH / 2 - restart_text.get_width() / 2, SCREEN_HEIGHT / 2 + 100))

    elif pause:
        font = pygame.font.Font(None, 36)
        pause_text = font.render("Pause", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH / 2 - pause_text.get_width() / 2, SCREEN_HEIGHT / 2 - pause_text.get_height() / 2))

def move_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.move_ip(0, -PADDLE_SPEED)
    if keys[pygame.K_s]:
        paddle1.move_ip(0, PADDLE_SPEED)

    if multiplayer:
        if keys[pygame.K_UP]:
            paddle2.move_ip(0, -PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            paddle2.move_ip(0, PADDLE_SPEED)
    else:
        if balls[0]['rect'].centery < paddle2.centery:
            paddle2.move_ip(0, -PADDLE_SPEED)
        else:
            paddle2.move_ip(0, PADDLE_SPEED)

    # Restrict paddles from moving out of the screen
    if paddle1.top < 0:
        paddle1.top = 0
    if paddle1.bottom > SCREEN_HEIGHT:
        paddle1.bottom = SCREEN_HEIGHT
    if paddle2.top < 0:
        paddle2.top = 0
    if paddle2.bottom > SCREEN_HEIGHT:
        paddle2.bottom = SCREEN_HEIGHT

def move_ball():
    global score1, score2, high_score, game_over

    for ball in balls:
        ball['rect'].move_ip(ball['dx'], ball['dy'])

        if ball['rect'].left < 0:
            score2 += 1
            reset_ball(ball)
        if ball['rect'].right > SCREEN_WIDTH:
            score1 += 1
            reset_ball(ball)
        if ball['rect'].top < 0 or ball['rect'].bottom > SCREEN_HEIGHT:
            ball['dy'] *= -1
        if ball['rect'].colliderect(paddle1) or ball['rect'].colliderect(paddle2):
            ball['dx'] *= -1
            increase_ball_speed(ball)
            split_chance = random.random()
            if split_chance < 0.1 and ball['original']:  # 0.1% chance to split if it's the original ball
                split_ball(ball)

        if score1 >= 10 or score2 >= 10:
            game_over = True

def increase_ball_speed(ball):
    if ball['dx'] > 0:
        ball['dx'] += BALL_SPEED_INCREMENT
    else:
        ball['dx'] -= BALL_SPEED_INCREMENT

    if ball['dy'] > 0:
        ball['dy'] += BALL_SPEED_INCREMENT
    else:
        ball['dy'] -= BALL_SPEED_INCREMENT

def check_high_score():
    global high_score
    if score1 > high_score:
        high_score = score1
    elif score2 > high_score:
        high_score = score2

def restart_game():
    global score1, score2, balls, game_over, pause
    score1 = 0
    score2 = 0
    balls = [{
        'rect': pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_SIZE, BALL_SIZE),
        'dx': BALL_SPEED * random.choice((-1, 1)),
        'dy': BALL_SPEED * random.choice((-1, 1)),
        'original': True,  # Set original flag for the reset ball
    }]
    game_over = False
    pause = False

def handle_menu():
    global in_menu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        in_menu = False
    elif keys[pygame.K_1]:
        multiplayer = False
    elif keys[pygame.K_2]:
        multiplayer = True

def main():
    global multiplayer, balls, score1, score2, high_score, game_over, pause, in_menu
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if in_menu:
            handle_menu()
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r] and (game_over or pause):
                restart_game()
            elif keys[pygame.K_p] and not game_over:
                pause = not pause

            if not game_over and not pause:
                move_paddle()
                move_ball()

            check_high_score()

        draw_objects()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()





