# Import module
import random
import sys
import pygame
from pygame.locals import *

# All the Game Variables

# rendering variables
window_width = 600
window_height = 499
fps = 32

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))

# game variables
ground_y = window_height * 0.8
ground_x = 0

pipe_vel_x = -4

bird_vel_y_initial = -9
bird_vel_y_max = 10
bird_vel_y_min = -8
gravity = 1

# the velocity of the bird immediately after flapping
bird_flap_velocity = -8

# image paths
game_images = {}
pipe_image = 'images/pipe.png'
background_image = 'images/background.jpg'
bird_player_image = 'images/bird.png'
sea_level_image = 'images/base.jfif'


def flappygame():
    score = 0
    bird_x = int(window_width / 5)
    bird_y = int(window_width / 2)
    mytempheight = 100

    # Generating two pipes for blitting on window
    first_pipe = create_pipe()
    second_pipe = create_pipe()

    # List containing lower pipes
    down_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe['lower']['y']},
        {'x': window_width + 300 - mytempheight + (window_width / 2),
         'y': second_pipe['lower']['y']},
    ]

    # List Containing upper pipes
    up_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe['upper']['y']},
        {'x': window_width + 200 - mytempheight + (window_width / 2),
         'y': second_pipe['upper']['y']},
    ]

    bird_vel_y = bird_vel_y_initial
    while True:
        bird_flapped = False

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if bird_y > 0:
                    bird_vel_y = bird_flap_velocity
                    bird_flapped = True

        # This function will return true
        # if the flappy bird is crashed
        if is_game_over(bird_x, bird_y, up_pipes, down_pipes):
            return

        # check for score
        player_mid_pos = bird_x + game_images['flappy_bird'].get_width() / 2
        for pipe in up_pipes:
            pipe_mid_pos = pipe['x'] + game_images['pipe_image'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                print(f"Your score is {score}")

        # apply gravity
        if bird_vel_y < bird_vel_y_max and not bird_flapped:
            bird_vel_y += gravity

        # move the bird, but don't move it into the ground
        bird_height = game_images['flappy_bird'].get_height()
        bird_y = bird_y + min(bird_vel_y, ground_y - bird_y - bird_height)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipe_vel_x
            lowerPipe['x'] += pipe_vel_x

        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            new_pipe = create_pipe()
            up_pipes.append(new_pipe['upper'])
            down_pipes.append(new_pipe['lower'])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipe_image'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipe_image'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipe_image'][1], (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (ground_x, ground_y))
        window.blit(game_images['flappy_bird'], (bird_x, bird_y))

        # Fetching the digits of score.
        numbers = [int(x) for x in str(score)]
        score_width = 0

        # finding the width of score images from numbers.
        for num in numbers:
            score_width += game_images['score_images'][num].get_width()
        x_offset = (window_width - score_width) / 1.1

        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['score_images'][num], (x_offset, window_width * 0.02))
            x_offset += game_images['score_images'][num].get_width()

        # Refreshing the game window and displaying the score.
        pygame.display.update()
        fps_clock.tick(fps)


def is_game_over(bird_x, bird_y, up_pipes, down_pipes):
    if bird_y > ground_y - 25 or bird_y < 0:
        return True

    pipe_height = game_images['pipe_image'][0].get_height()
    pipe_width = game_images['pipe_image'][0].get_width()

    bird_height = game_images['flappy_bird'].get_height()

    for pipe in up_pipes:
        if abs(bird_x - pipe['x']) < pipe_width and bird_y < pipe_height + pipe['y']:
            return True

    for pipe in down_pipes:
        if abs(bird_x - pipe['x']) < pipe_width and bird_y + bird_height > pipe['y']:
            return True

    return False


def create_pipe():
    offset = window_height / 3
    pipe_height = game_images['pipe_image'][0].get_height()

    y_lower = random.randrange(0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset)) + offset
    y_upper = y_lower - pipe_height - offset

    pipe_x = window_width + 10

    return {
        'upper': {'x': pipe_x, 'y': y_upper},
        'lower': {'x': pipe_x, 'y': y_lower}
    }


# program where the game starts
if __name__ == "__main__":

    # For initializing modules of pygame library
    pygame.init()
    fps_clock = pygame.time.Clock()

    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game')

    # Load all the images which we will use in the game
    game_images['flappy_bird'] = pygame.image.load(bird_player_image).convert_alpha()
    game_images['sea_level'] = pygame.image.load(sea_level_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['pipe_image'] = (pygame.transform.rotate(pygame.image.load(pipe_image).convert_alpha(), 180),
                                 pygame.image.load(pipe_image).convert_alpha())

    # digit images for displaying score
    game_images['score_images'] = [pygame.image.load(f'images/{i}.png').convert_alpha() for i in range(10)]

    # game variables
    bird_start_x = int(window_width / 5)
    bird_start_y = int((window_height - game_images['flappy_bird'].get_height()) / 2)

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    # Here starts the main game
    while True:
        for event in pygame.event.get():

            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or
            # up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                flappygame()

            # if user doesn't press any key nothing happens
            else:
                window.blit(game_images['background'], (0, 0))
                window.blit(game_images['flappy_bird'], (bird_start_x, bird_start_y))
                window.blit(game_images['sea_level'], (ground_x, ground_y))
                pygame.display.update()
                fps_clock.tick(fps)
