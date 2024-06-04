import pygame
import numbers_round as nr

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

def play():
    # Initialize Pygame
    pygame.init()
    font = pygame.font.SysFont(None, 36)

    # Set up the display
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption('Numbers Game')

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    FONT_COLOR = (50, 50, 50)
    puzzle = nr.generate_puzzle()
    solution = nr.solve_puzzle(puzzle)

    def draw_tiles(screen, letters, tile_size, tile_color, font_color):
        font = pygame.font.SysFont(None, 36)
        tiles_per_row = 6  # Adjust based on your preference
        spacing = 10  # Space between tiles
        start_x = (screen.get_width() - (tiles_per_row * (tile_size + spacing) - spacing)) / 2
        start_y = 150  # Starting Y position of the first row of tiles

        tile_locs = {}
        
        for i, letter in enumerate(letters):
            row = i // tiles_per_row
            col = i % tiles_per_row
            x = start_x + col * (tile_size + spacing)
            y = start_y + row * (tile_size + spacing)
            pygame.draw.rect(screen, tile_color, (x, y, tile_size, tile_size))
            letter_text = font.render(letter, True, font_color)
            letter_rect = letter_text.get_rect(center=(x + tile_size / 2, y + tile_size / 2))
            screen.blit(letter_text, letter_rect)
            dup_letters = {}
            
            if letter in tile_locs.keys():
                if letter in dup_letters.keys():
                    dup_letters[letter] += 1
                else:
                    dup_letters[letter] = 2
                key = letter + str(dup_letters[letter])
            else:
                key = letter
            
            tile_locs[key] = {'pos': (x, y, tile_size, tile_size), 'used' : False}
        
        
        
        return tile_locs
    game_state = 'PLAYING'
    running = True
    while running:
        for event in pygame.event.get():
            event
            pass
        if game_state == 'PLAYING':
            font = pygame.font.SysFont(None, 55)
            screen.fill(WHITE)
            text = font.render('The letters are:', True, FONT_COLOR)
            text_rect = text.get_rect(center=(screen_width/2, screen_height/4))
            screen.blit(text, text_rect)
            draw_tiles(screen, [str(x) for x in puzzle['bigs']+puzzle['smalls']],tile_size = 50, tile_color = (0,0,255), font_color = BLACK)
            pygame.display.flip()
    user_score = 10


    return user_score, solution 

if __name__ == 'main':
    play()