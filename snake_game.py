
"""
A classic Snake game implementation using Pygame.

Features:
- Classic snake gameplay: move, eat, grow.
- Game over on collision with walls or self.
- Score and High Score tracking.
- Pause and Resume functionality (SPACEBAR).
- High score saved to `highscore.txt`.
- Speed boost power-up.
"""
import pygame
import random
import time

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SNAKE_HEAD_COLOR = (0, 175, 0)  # Darker green for the head
SNAKE_BODY_COLOR = (0, 225, 0)  # Lighter green for the body

# Snake properties
SNAKE_SPEED_NORMAL = 10
SNAKE_SPEED_BOOST = 20

# Power-up properties
POWERUP_DURATION = 5  # seconds
POWERUP_SPAWN_INTERVAL = 20  # seconds

# --- Game Setup ---
def initialize_game():
    """Initializes Pygame and sets up the game window."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    return screen

def load_high_score():
    """Loads the high score from highscore.txt."""
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except (IOError, ValueError):
        return 0

def save_high_score(score):
    """Saves the high score to highscore.txt."""
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# --- Game Components ---
def create_snake():
    """Initializes the snake's position and body."""
    return [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]

def create_food(snake_body):
    """Creates a food item at a random position."""
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food_pos not in snake_body:
            return food_pos

def create_powerup(snake_body):
    """Creates a power-up at a random position."""
    while True:
        powerup_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if powerup_pos not in snake_body:
            return powerup_pos

# --- Drawing Functions ---
def draw_grid(screen):
    """Draws the grid on the screen."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_snake(screen, snake_body):
    """Draws the snake on the screen with a distinct head."""
    # Draw the head
    if snake_body:
        head = snake_body[0]
        pygame.draw.rect(screen, SNAKE_HEAD_COLOR, (head[0] * GRID_SIZE, head[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the body
        for segment in snake_body[1:]:
            pygame.draw.rect(screen, SNAKE_BODY_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_food(screen, food_pos):
    """Draws the food on the screen."""
    pygame.draw.rect(screen, RED, (food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_powerup(screen, powerup_pos):
    """Draws the power-up on the screen."""
    pygame.draw.rect(screen, BLUE, (powerup_pos[0] * GRID_SIZE, powerup_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_score(screen, score, high_score):
    """Draws the score and high score on the screen."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 10, 10))

# --- Game Logic ---
def move_snake(snake_body, direction):
    """Moves the snake in the given direction."""
    head_x, head_y = snake_body[0]
    if direction == "UP":
        head_y -= 1
    elif direction == "DOWN":
        head_y += 1
    elif direction == "LEFT":
        head_x -= 1
    elif direction == "RIGHT":
        head_x += 1
    new_head = (head_x, head_y)
    snake_body.insert(0, new_head)
    return snake_body

def check_collision(snake_body):
    """Checks for collisions with walls or self."""
    head = snake_body[0]
    if (head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT):
        return True  # Wall collision
    if head in snake_body[1:]:
        return True  # Self collision
    return False

def game_over_screen(screen, score, high_score):
    """Displays the game over screen and waits for user input."""
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, RED)
    score_text = pygame.font.Font(None, 36).render(f"Your Score: {score}", True, WHITE)
    high_score_text = pygame.font.Font(None, 36).render(f"High Score: {high_score}", True, WHITE)
    restart_text = pygame.font.Font(None, 36).render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "RESTART"
                if event.key == pygame.K_q:
                    return "QUIT"

def pause_screen(screen):
    """Displays the pause screen."""
    font = pygame.font.Font(None, 72)
    pause_text = font.render("Game Paused", True, WHITE)
    resume_text = pygame.font.Font(None, 36).render("Press SPACEBAR to Resume", True, WHITE)
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    pygame.display.flip()

# --- Main Game Loop ---
def game_loop():
    """The main loop for the snake game."""
    screen = initialize_game()
    clock = pygame.time.Clock()

    while True:
        high_score = load_high_score()
        snake_body = create_snake()
        food_pos = create_food(snake_body)
        powerup_pos = None
        direction = "RIGHT"
        score = 0
        paused = False
        speed = SNAKE_SPEED_NORMAL
        powerup_active = False
        powerup_timer = 0
        last_powerup_spawn = time.time()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    elif not paused:
                        if event.key == pygame.K_UP and direction != "DOWN":
                            direction = "UP"
                        elif event.key == pygame.K_DOWN and direction != "UP":
                            direction = "DOWN"
                        elif event.key == pygame.K_LEFT and direction != "RIGHT":
                            direction = "LEFT"
                        elif event.key == pygame.K_RIGHT and direction != "LEFT":
                            direction = "RIGHT"

            if paused:
                pause_screen(screen)
                continue

            # Move snake
            snake_body = move_snake(snake_body, direction)

            # Check for food collision
            if snake_body[0] == food_pos:
                score += 1
                food_pos = create_food(snake_body)
            else:
                snake_body.pop()

            # Check for power-up collision
            if powerup_pos and snake_body[0] == powerup_pos:
                speed = SNAKE_SPEED_BOOST
                powerup_active = True
                powerup_timer = time.time()
                powerup_pos = None

            # Power-up timer
            if powerup_active and time.time() - powerup_timer > POWERUP_DURATION:
                speed = SNAKE_SPEED_NORMAL
                powerup_active = False

            # Spawn power-up
            if time.time() - last_powerup_spawn > POWERUP_SPAWN_INTERVAL and not powerup_pos:
                powerup_pos = create_powerup(snake_body)
                last_powerup_spawn = time.time()

            # Check for game over
            if check_collision(snake_body):
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                action = game_over_screen(screen, score, high_score)
                if action == "QUIT":
                    pygame.quit()
                    return
                elif action == "RESTART":
                    running = False

            # Drawing
            screen.fill(BLACK)
            # draw_grid(screen) # Optional: uncomment to see the grid
            draw_snake(screen, snake_body)
            draw_food(screen, food_pos)
            if powerup_pos:
                draw_powerup(screen, powerup_pos)
            draw_score(screen, score, high_score)
            pygame.display.flip()

            # Control game speed
            clock.tick(speed)

if __name__ == "__main__":
    print("--- Snake Game ---")
    print("Controls:")
    print("  - Arrow Keys: Move the snake")
    print("  - SPACEBAR: Pause/Resume the game")
    print("Power-ups:")
    print("  - Blue Square: Speed boost for 5 seconds")
    print("------------------")
    game_loop()
