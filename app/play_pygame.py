import pygame 

import letters_pygame as lp
import numbers_pygame as np
import sys


# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 640
screen_height = 480

screen = pygame.display.set_mode((screen_width, screen_height))


tile_size, tile_color, font_color = 50, (100, 100, 200), (255, 255, 255)

# Function to draw the button, call this in your game loop
def draw_button(screen, position, size, color, text):
    pygame.draw.rect(screen, color, (*position, *size))
    font = pygame.font.SysFont(None, 36)
    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(position[0] + size[0] // 2, position[1] + size[1] // 2))
    screen.blit(text_render, text_rect)

def click_was_inside_box(mouse_pos, box_position, box_size):
    return box_position[0] <= mouse_pos[0] <= box_position[0] + box_size[0] and box_position[1] <= mouse_pos[1] <= box_position[1] + box_size[1]

pygame.display.set_caption('Main Menu')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_COLOR = (50, 50, 50)

button_color = (0, 0, 200)  # Green color
button_position = (screen_width // 2 - 50, screen_height // 2 - 25)  # Centered
button_size = (100, 50)
button_text = 'Start'


running = True
game_state = "INITIAL"
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == "INITIAL":
            print('registered click')
            mouse_pos = event.pos  # Gets the mouse position
            # Check if mouse position is within the button bounds
            if click_was_inside_box(mouse_pos, button_position, button_size):
                game_state = 'PLAYING'
                answers, user_word = lp.play()
                game_state = 'SHOW LETTER RESULTS'
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == "SHOW LETTER RESULTS" and click_was_inside_box(event.pos, (100,400), (400, 50)):
            print('should play numbers here')
            game_state = 'PLAYING_NUMBERS'
            user_score, numbers_solution = np.play()

    if game_state == "INITIAL":
        # Fill the screen with a color
        screen.fill(WHITE)
        # Set up fonts
        font = pygame.font.SysFont(None, 55)
        # Render text
        text = font.render('Welcome to Letters and Numbers!', True, FONT_COLOR)
        text_rect = text.get_rect(center=(screen_width/2, screen_height/4))
        screen.blit(text, text_rect)

        draw_button(screen, button_position, button_size, button_color, button_text)
        pygame.display.flip()
    
    if game_state == "SHOW LETTER RESULTS":
        # Fill the screen with a color
        screen.fill(WHITE)
        # Set up fonts
        font = pygame.font.SysFont(None, 55)
        # Render text
        longest_word_length = list(answers.keys())[0]
        longest_words = list(set(answers[longest_word_length]))[:3]
        answer_string = f'The best was a {longest_word_length}: e.g. {longest_words}'
        text = font.render(answer_string, True, FONT_COLOR)
        text_rect = text.get_rect(center=(screen_width/2, screen_height/4))
        screen.blit(text, text_rect)

        draw_button(screen, (100,400), size = (400, 50), color = button_color, text = 'Continue to Numbers Round')
        pygame.display.flip()
    
   
pygame.quit()
sys.exit()    