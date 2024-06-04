import letters_round as lr
import time
import pygame

def play():
    # Initialize Pygame
    pygame.init()
    font = pygame.font.SysFont(None, 36)

    # Set up the display
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption('Letters Round Game')

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    FONT_COLOR = (50, 50, 50)

    def click_was_inside_box(mouse_pos, box_position, box_size):
        return box_position[0] <= mouse_pos[0] <= box_position[0] + box_size[0] and box_position[1] <= mouse_pos[1] <= box_position[1] + box_size[1]

    # Function to draw the button, call this in your game loop
    def draw_button(screen, position, size, color, text):
        pygame.draw.rect(screen, color, (*position, *size))
        text_render = font.render(text, True, WHITE)
        text_rect = text_render.get_rect(center=(position[0] + size[0] // 2, position[1] + size[1] // 2))
        screen.blit(text_render, text_rect)


    def draw_tiles(screen, letters, tile_size, tile_color, font_color):
        font = pygame.font.SysFont(None, 36)
        num_tiles = len(letters)
        tiles_per_row = 5  # Adjust based on your preference
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

    running = True
    game_state = 'PLAYING'
    user_word = ''
    player_has_given_valid_word = False
    tile_size, tile_color, font_color = 50, (100, 100, 200), (255, 255, 255)

    BACKSPACE_BUTTON_POS = (350,400)
    BACKSPACE_BUTTON_SIZE = (240,60)

    SUBMIT_BUTTON_POS = (50,400)
    SUBMIT_BUTTON_SIZE = (240,60)
    letters = lr.generate_letters()  # Call the function to generate letters
    answers = lr.solve_game(letters)
    # print(letters['game_letters'])  # For demonstration, print the letters. Update this to display on screen as needed.
    tile_locs = draw_tiles(screen, letters['game_letters'], tile_size, tile_color, font_color)
    running = True
    last_letter_played = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and game_state == 'PLAYING':
        
                if event.key == pygame.K_BACKSPACE and len(user_word) > 0:
                    user_word = user_word[:-1]
                elif event.key == pygame.K_RETURN:
                    game_state = 'GUESS_SUBMITTED'
                else:
                    user_word += event.unicode  # Add the character to the string
            
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'PLAYING':
                for letter, data in tile_locs.items():
                    pos_x, pos_y, size_x, size_y = data['pos']
                    box_pos = (pos_x, pos_y)
                    size = (size_x, size_y)
                    if click_was_inside_box(mouse_pos=event.pos, box_position=box_pos, box_size=size) and not tile_locs[letter]['used']:
                        print(tile_locs[letter]['used'])
                        user_word += letter[0]
                        print(user_word)
                        tile_locs[letter]['used'] = True
                        print(data)
                        last_letter_played = letter
                
                if click_was_inside_box(event.pos, BACKSPACE_BUTTON_POS, BACKSPACE_BUTTON_SIZE):
                    if len(user_word) > 0:
                        print('backspaced a letter')
                        user_word = user_word[:-1]
                        tile_locs[last_letter_played]['used'] = False

                if click_was_inside_box(event.pos, SUBMIT_BUTTON_POS, SUBMIT_BUTTON_SIZE):
                    game_state = 'GUESS_SUBMITTED'
                    print('Guess submitted')

            elif game_state == 'GUESS_VERIFIED':
                # Fill the screen with a color
                screen.fill(WHITE)
                # Set up fonts
                font = pygame.font.SysFont(None, 55)
                # Render text
                text = font.render(f'You scored {len(user_word)} points!', True, FONT_COLOR)
                text_rect = text.get_rect(center=(screen_width/2, screen_height/4))
                screen.blit(text, text_rect)
                
                button_color = (0, 0, 200)  # Green color
                button_position = (screen_width // 2 - 50, screen_height // 2 - 25)  # Centered
                button_size = (100, 50)
                button_text = 'Play Numbers Game'

                draw_button(screen, button_position, button_size, button_color, button_text)
                pygame.display.flip()


        if game_state == 'PLAYING':
            font = pygame.font.SysFont(None, 55)
            screen.fill(WHITE)
            text = font.render('The letters are:', True, FONT_COLOR)
            text_rect = text.get_rect(center=(screen_width/2, screen_height/4))
            screen.blit(text, text_rect)
            draw_tiles(screen, letters['game_letters'], tile_size, tile_color, font_color)
            draw_button(screen, BACKSPACE_BUTTON_POS, BACKSPACE_BUTTON_SIZE, (100, 100, 200), "BACKSPACE")
            draw_button(screen, SUBMIT_BUTTON_POS, SUBMIT_BUTTON_SIZE, (100, 100, 200), "SUBMIT")
            text = font.render(user_word, True, FONT_COLOR)
            text_rect = text.get_rect(center=(0.2*screen_width, 0.7*screen_height))
            screen.blit(text, text_rect)
            pygame.display.flip()

        if game_state == 'GUESS_SUBMITTED':
            out = lr.process_guess(user_word=user_word)
            if out:
                running = False
            else:
                text = font.render(f"Sorry, {user_word} is not a valid word.", True, (255,0,0))
                text_rect = text.get_rect(center=(0.5*screen_width, 0.8*screen_height))
                screen.blit(text, text_rect)
                pygame.display.flip()
                game_state = 'PLAYING'
                time.sleep(3)
                user_word = ''
                tile_locs = draw_tiles(screen, letters['game_letters'], tile_size, tile_color, font_color)


    return answers, user_word

