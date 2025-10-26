import pygame
from utilities.button import Button
from utilities.grid import Grid
import sys

pygame.init()
height, width = 700, 1200
screen = pygame.display.set_mode((width, height))
cell_sizes = [1, 5, 10, 20, 25, 50]
dimensions = [(700, 1200),(140, 240), (70, 120), (35, 60), (28, 48), (14, 24)]
cell_dimension_map = {dimension: cell for cell, dimension in zip(cell_sizes, dimensions)}
# Frame rate
FPS = 60
clock = pygame.time.Clock()
# Initialize colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)
gray2 = (155, 155, 155)
yellow = (255, 255, 0)
pygame.display.set_caption("Maze Generator")

def create_button_bg(x_coor, y_coor, size, color):
    width_bg = size[0]+5
    height_bg = size[1]+5
    normal_surface = pygame.Surface((width_bg, height_bg), pygame.SRCALPHA)
    border_surface = pygame.Surface((width_bg + 8, height_bg + 8), pygame.SRCALPHA)
    alpha_value = 125

    normal_surface.fill((*color[:3], alpha_value))
    border_surface.fill((255, 255, 255, alpha_value))

    normal_rect = normal_surface.get_rect(center=(x_coor, y_coor))
    border_rect = border_surface.get_rect(center=(x_coor, y_coor))

    screen.blit(border_surface, border_rect)
    screen.blit(normal_surface, normal_rect)

def change_update(position, button_list):
    for buttons in button_list:
        buttons.changeColor(position)
        buttons.update(screen)

def get_font(size):
    return pygame.font.Font('Fonts/font.ttf', size)

def text_to_dimension(dimension_text):
    translate_table = str.maketrans('', '', '()')
    dimension_text = dimension_text.translate(translate_table).split(', ')
    dimension_text = [int(dimension_text[0]), int(dimension_text[1])]
    return dimension_text

def get_maze_file(file_name):
    maze_grid = []
    with open(file_name, "r") as f:
        for line in f:
            maze_grid.append(line)
    return maze_grid


def load_maze(file_name):
    """
    Function converts a maze in a file to a grid list.
    :param file_name
    :return: list
    """
    grid = []
    with open(file_name, 'r') as f:
        for line in f:
            new_line = line.strip("\n")
            grid.append(new_line)
    return grid

def choose_dimension_screen():
    run_dimension = True
    created_grid = False
    grid = None
    while run_dimension:
        screen.fill(black)
        mouse_pos = pygame.mouse.get_pos()
        change_update(mouse_pos, dimension_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in dimension_buttons:
                    if button.checkforInput(mouse_pos):
                        maze_size = text_to_dimension(button.text_input)
                        grid = Grid(cell_dimension_map[(maze_size[0], maze_size[1])], maze_size)
                        grid.set_start_end(screen)
                        grid.save_maze("test_maze.txt")
                        print("Saved maze")
                        created_grid = True
                        run_dimension = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu", None
        pygame.display.update()
        pygame.display.flip()
    if created_grid:
        return "play_game", grid
    return 'main_menu', None

def game_play(current_grid):
    if current_grid is None:
        print("Create grid first")
        return "main_menu"
    run = True
    while run:
        screen.fill(black)
        current_grid.draw_maze(screen)
        current_grid.blit_distance(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu"
        pygame.display.update()
        pygame.display.flip()
    return "main_menu"

#Main buttons
input_dimension = Button(None, "Choose maze dimensions", (width/2, height/3),get_font(30),
(227, 84, 49), (227, 152, 49))
play_button = Button(None, "Play game", (width/2, height*2/3), get_font(30), (227, 84, 49), (227, 152, 49))
main_buttons = [input_dimension, play_button]
#Choose dimension buttons
dimension_buttons = []
for i in range(1,len(dimensions)+1):
    dimension_button = Button(None, f"{dimensions[i-1]}", (width/2, i*height/(len(dimensions)+1)), get_font(20), (227, 84, 49), (227, 152, 49))
    dimension_buttons.append(dimension_button)
button_bg_color = (247, 191, 121)

def main():
    current_grid = None
    current_state = "main_menu"
    while True:
        if current_state == "main_menu":
            current_state = main_menu(current_grid)
        elif current_state == "choose_dimension_screen":
            next_state, new_grid = choose_dimension_screen()
            current_state = next_state
            if new_grid is not None:
                current_grid = new_grid
        elif current_state == "quit":
            pygame.quit()
            print("Thank you for playing!")
            sys.exit()
        elif current_state == "play_game":
            current_state = game_play(current_grid)
        else:
            print("Unrecognized state")
            pygame.quit()
            sys.exit()

def main_menu(current_grid):
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(gray)
        create_button_bg(width/2, height/3, input_dimension.get_size(), green)
        create_button_bg(width/2, height*2/3, play_button.get_size(), yellow)
        change_update(mouse_pos, main_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_p:
                    if current_grid is not None:
                        current_grid.print_grid()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for buttons in main_buttons:
                    if buttons == input_dimension:
                        if input_dimension.checkforInput(mouse_pos):
                            return "choose_dimension_screen"
                    if buttons == play_button:
                        if play_button.checkforInput(mouse_pos):
                            return "play_game"
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
    main()
