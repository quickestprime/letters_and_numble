import numbers_round as nr
import letters_round as lr

import warnings
warnings.filterwarnings('ignore')


import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Letters Round Game')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_COLOR = (50, 50, 50)


# Function to draw the button, call this in your game loop
def draw_button(screen, position, size, color, text):
    pygame.draw.rect(screen, color, (*position, *size))
    font = pygame.font.SysFont(None, 36)
    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(position[0] + size[0] // 2, position[1] + size[1] // 2))
    screen.blit(text_render, text_rect)




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # Gets the mouse position
            # Check if mouse position is within the button bounds
            if button_position[0] <= mouse_pos[0] <= button_position[0] + button_size[0] and button_position[1] <= mouse_pos[1] <= button_position[1] + button_size[1]:
                letters = lr.generate_letters()  # Call the function to generate letters
                print(letters['letters'])  # For demonstration, print the letters. Update this to display on screen as needed.




    # Fill the screen with a color
    screen.fill(WHITE)
    # Set up fonts
    font = pygame.font.SysFont(None, 55)
    # Render text
    text = font.render('Welcome to the Letters Round!', True, FONT_COLOR)
    text_rect = text.get_rect(center=(screen_width/2, screen_height/4))
    screen.blit(text, text_rect)
    # Update the display
    pygame.display.flip()

    button_color = (0, 0, 200)  # Green color
    button_position = (screen_width // 2 - 50, screen_height // 2 - 25)  # Centered
    button_size = (100, 50)
    button_text = 'Start'

    

    draw_button(screen, button_position, button_size, button_color, button_text)




pygame.quit()
sys.exit()



# Initialize an empty string for the user's word
user_word = ''
# Inside the game loop, before pygame.display.flip()
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            user_word = user_word[:-1]
        elif event.key == pygame.K_RETURN:
            print(user_word)  # For now, just print the word to console
            user_word = ''  # Reset user_word after pressing enter
        else:
            user_word += event.unicode  # Add the character to the string
# Display the user's current word
word_text = font.render(user_word, True, FONT_COLOR)
word_rect = word_text.get_rect(center=(screen_width/2, screen_height/2))
screen.blit(word_text, word_rect)

letters_text = font.render('Letters: ' + letters, True, FONT_COLOR)
letters_rect = letters_text.get_rect(center=(screen_width/2, screen_height/3))
screen.blit(letters_text, letters_rect)

