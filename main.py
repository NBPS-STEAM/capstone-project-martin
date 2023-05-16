import pygame
import sys

# Game setup
width, height = 640, 480
ball_size = paddle_width = 15
paddle_height = 80
ball_dx = ball_dy = 2
paddle_speed = 2
colors = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0)
}
keys = {
    "UP": 273,
    "DOWN": 274,
    "W": 119,
    "S": 115
}

# Initialize game
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Define the paddles and the ball
paddle1 = pygame.Rect(paddle_width, height / 2, paddle_width, paddle_height)
paddle2 = pygame.Rect(width - paddle_width * 2, height / 2, paddle_width, paddle_height)
ball = pygame.Rect(width / 2, height / 2, ball_size, ball_size)

while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get current key presses
    pressed = pygame.key.get_pressed()

    if pressed[keys["UP"]]:
        paddle2.move_ip(0, -paddle_speed)
    if pressed[keys["DOWN"]]:
        paddle2.move_ip(0, paddle_speed)
    if pressed[keys["W"]]:
        paddle1.move_ip(0, -paddle_speed)
    if pressed[keys["S"]]:
        paddle1.move_ip(0, paddle_speed)

    # Ensure paddles don't go off screen
    if paddle1.top < 0:
        paddle1.top = 0
    if paddle1.bottom > height:
        paddle1.bottom = height
    if paddle2.top < 0:
        paddle2.top = 0
    if paddle2.bottom > height:
        paddle2.bottom = height

    # Update ball position
    ball.move_ip(ball_dx, ball_dy)

    # Ball collision with paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_dx *= -1
    # Ball collision with top and bottom
    elif ball.top < 0 or ball.bottom > height:
        ball_dy *= -1
    # Ball hit left or right side (a player scored a point)
    elif ball.left < 0 or ball.right > width:
        print("Game over!")
        pygame.quit()
        sys.exit()

    # Draw everything
    screen.fill(colors["BLACK"])
    pygame.draw.rect(screen, colors["WHITE"], paddle1)
    pygame.draw.rect(screen, colors["WHITE"], paddle2)
    pygame.draw.rect(screen, colors["WHITE"], ball)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
