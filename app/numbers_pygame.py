import pygame


def draw_input_bar(screen, input_text, font, input_bar_position, input_bar_size, input_bar_color, text_color):
    # Draw the input bar rectangle
    pygame.draw.rect(screen, input_bar_color, (*input_bar_position, *input_bar_size))
    
    # Render the input text
    text_surface = font.render(input_text, True, text_color)
    # Adjust the text position to be inside the input bar
    text_position = (input_bar_position[0] + 5, input_bar_position[1] + input_bar_size[1] / 2 - text_surface.get_height() / 2)
    
    screen.blit(text_surface, text_position)
    # Input bar settings
    input_bar_position = (100, 400)  # Example position
    input_bar_size = (440, 50)  # Example size
    input_bar_color = (200, 200, 200)  # Light grey
    text_color = (0, 0, 0)  # Black
    input_text = ''  # To store user input
    # Font for input text
    font = pygame.font.SysFont(None, 36)

