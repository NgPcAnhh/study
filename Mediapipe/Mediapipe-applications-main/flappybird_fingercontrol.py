import pygame
import random
import mediapipe as mp
import cv2
import numpy as np

# Khởi tạo pygame
pygame.init()

# Cài đặt màn hình
GAME_WIDTH = 400
GAME_HEIGHT = 700
WEBCAM_WIDTH = 650
WIDTH = GAME_WIDTH + WEBCAM_WIDTH
HEIGHT = GAME_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Chim
bird_img = pygame.Surface((40, 30))
bird_img.fill((255, 255, 0))  # Màu vàng
bird_rect = bird_img.get_rect()
bird_rect.center = (GAME_WIDTH // 4, HEIGHT // 2)

# Ống
PIPE_WIDTH = 70
PIPE_HEIGHT = random.randint(150, 400)
PIPE_GAP = 150
pipe_x = GAME_WIDTH

# Font
font = pygame.font.Font(None, 36)

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)

# Tốc độ game và mức độ khó
DIFFICULTY_LEVELS = [
    {"name": "Easy", "speed": 3},
    {"name": "Medium", "speed": 5},
    {"name": "Hard", "speed": 7},
    {"name": "Extreme Hard", "speed": 8},
    {"name": "VIP ProMax", "speed": 10}
]
game_speed = DIFFICULTY_LEVELS[0]["speed"]

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_pipe(x, height):
    pygame.draw.rect(screen, GREEN, (x, 0, PIPE_WIDTH, height))
    pygame.draw.rect(screen, GREEN, (x, height + PIPE_GAP, PIPE_WIDTH, HEIGHT - height - PIPE_GAP))

def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(score):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

    play_again_button = Button(WIDTH // 2 - 150, HEIGHT * 3 // 4, 300, 50, "Play Again", GREEN, BLACK)
    change_mode_button = Button(WIDTH // 2 - 150, HEIGHT * 3 // 4 + 60, 300, 50, "Change Mode", GRAY, BLACK)
    quit_button = Button(WIDTH // 2 - 150, HEIGHT * 3 // 4 + 120, 300, 50, "Quit", RED, WHITE)

    play_again_button.draw(screen)
    change_mode_button.draw(screen)
    quit_button.draw(screen)
    
    pygame.display.update()
    return play_again_button, change_mode_button, quit_button

def reset_game():
    global bird_rect, pipe_x, PIPE_HEIGHT
    bird_rect.center = (GAME_WIDTH // 4, HEIGHT // 2)
    pipe_x = GAME_WIDTH
    PIPE_HEIGHT = random.randint(150, 400)

def draw_difficulty_selection():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    title_text = font.render("Select Difficulty", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    buttons = []
    for i, level in enumerate(DIFFICULTY_LEVELS):
        button = Button(WIDTH // 2 - 150, HEIGHT // 3 + i * 60, 300, 50, f"{level['name']} (Speed: {level['speed']})", GRAY, BLACK)
        button.draw(screen)
        buttons.append(button)

    pygame.display.update()
    return buttons

def get_difficulty_selection(buttons):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(buttons):
                    if button.is_clicked(mouse_pos):
                        return DIFFICULTY_LEVELS[i]["speed"]

def main():
    global game_speed, pipe_x, PIPE_HEIGHT
    clock = pygame.time.Clock()
    score = 0

    difficulty_buttons = draw_difficulty_selection()
    selected_speed = get_difficulty_selection(difficulty_buttons)
    if selected_speed is None:
        return
    game_speed = selected_speed

    running = True
    while running:
        # Xử lý hình ảnh từ webcam và nhận diện bàn tay
        success, image = cap.read()
        if success:
            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Lấy tọa độ của đầu ngón trỏ (landmark số 8)
                    finger_y = hand_landmarks.landmark[8].y
                    bird_rect.centery = int(finger_y * HEIGHT)

            # Chuyển đổi hình ảnh OpenCV sang định dạng Pygame
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = np.rot90(image)
            image = pygame.surfarray.make_surface(image)
            image = pygame.transform.scale(image, (WEBCAM_WIDTH, HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Di chuyển ống
        pipe_x -= game_speed * 1.1
        if pipe_x <= -PIPE_WIDTH:
            pipe_x = GAME_WIDTH
            PIPE_HEIGHT = random.randint(150, 400)
            score += 1

        # Kiểm tra va chạm
        if (bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT or
            (pipe_x < bird_rect.right < pipe_x + PIPE_WIDTH and
             (bird_rect.top < PIPE_HEIGHT or bird_rect.bottom > PIPE_HEIGHT + PIPE_GAP))):
            play_again_button, change_mode_button, quit_button = game_over_screen(score)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if play_again_button.is_clicked(mouse_pos):
                            reset_game()
                            score = 0
                            waiting = False
                        elif change_mode_button.is_clicked(mouse_pos):
                            difficulty_buttons = draw_difficulty_selection()
                            selected_speed = get_difficulty_selection(difficulty_buttons)
                            if selected_speed is None:
                                return
                            game_speed = selected_speed
                            reset_game()
                            score = 0
                            waiting = False
                        elif quit_button.is_clicked(mouse_pos):
                            return

        # Vẽ nền cho phần trò chơi
        screen.fill((135, 206, 235), (0, 0, GAME_WIDTH, HEIGHT))  # Màu xanh nhạt

        # Vẽ chim
        screen.blit(bird_img, bird_rect)

        # Vẽ ống
        draw_pipe(pipe_x, PIPE_HEIGHT)

        # Hiển thị điểm
        show_score(score)

        # Vẽ webcam
        screen.blit(image, (GAME_WIDTH, 0))

        # Hiển thị độ khó hiện tại
        difficulty_name = next(level["name"] for level in DIFFICULTY_LEVELS if level["speed"] == game_speed)
        difficulty_text = font.render(f"Difficulty: {difficulty_name}", True, WHITE)
        screen.blit(difficulty_text, (10, 50))

        pygame.display.update()
        clock.tick(60)

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()