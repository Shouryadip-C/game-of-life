"""Conway's Game of Life simulation using python and pygame
"""

import numpy
import pygame

from settings import *


def update(surface, cur, sz):
    """Updates grid cell values and renders alive cells

    Rules:
        - Live call with less than 2 live neighbours dies
        - Live cell with two or three live neighbours lives
        - Live cell with more than three live neighbours dies
        - Dead cell with exactly three live neighbours becomes alive

    Args:
        surface (pygame.Surface): Surface to be rendered on
        cur (numpy array): Current grid of cells
        sz (int): Size of a cell in pixels

    Returns:
        numpy array: Updated grid of cells
    """

    # new grid to apply updates into
    nxt = numpy.zeros((cur.shape[0], cur.shape[1]))

    # visit each cell to check its state and update the new grid
    for r, c in numpy.ndindex(cur.shape):
        # get the number of neighbour cells that are alive
        num_alive = numpy.sum(cur[r - 1:r + 2, c - 1:c + 2]) - cur[r, c]

        # check if cell stays alive or dies and assign corresponding color
        if cur[r, c] == 1 and num_alive < 2 or num_alive > 3:
            col = col_about_to_die
        elif (cur[r, c] == 1 and 2 <= num_alive <= 3) \
                or (cur[r, c] == 0 and num_alive == 3):
            nxt[r, c] = 1
            col = col_alive

        col = col if cur[r, c] == 1 else col_background

        # Render only alive cells
        if col != col_background:
            pygame.draw.rect(surface, col, (c * sz, r * sz, sz - 1, sz - 1))

    return nxt


def init_grid(pattern=None):
    """Initialize new grid with alive cells as '1' and dead cells as '0'

    Args:
        pattern (str, optional): Name of pattern to be used. Defaults to None.

    Returns:
        numpy array: The initialised grid of cells.
    """

    cells = numpy.zeros(GRID_SIZE)

    # replace the pattern in the empty grid if specified
    if pattern is not None:
        data = PATTERNS[pattern]
        cells[data[1][0]: data[1][0] + len(data[0]),
              data[1][1]: data[1][1] + len(data[0][0])] = data[0]

    return cells


# Setup Pygame --------------------------------------------------------------- #
pygame.init()
pygame.display.set_caption(TITLE)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
cells = init_grid()

paused = True
running = True

# game loop
while running:
    dt = clock.tick(FPS) / 1000

    # Events ----------------------------------------------------------------- #
    for event in pygame.event.get():

        # quit when user closes window
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                paused = not paused

            # give player options to use predefined patterns for simulation
            elif event.key == pygame.K_r:
                paused = True
                available = list(PATTERNS.keys())
                print("-1 : Empty Grid")
                for index, pattern in enumerate(available):
                    print(f"{index} : {pattern}")
                i = int(input("Choose pattern (index no. of pattern): "))
                if 0 <= i < len(available):
                    cells = init_grid(available[i])
                else:
                    cells = init_grid()

        # make a clicked cell alive only when simulation is paused
        elif pygame.mouse.get_pressed()[0] and paused:
            x, y = pygame.mouse.get_pos()
            cells[y // CELL_SIZE, x // CELL_SIZE] = 1

    # Update ----------------------------------------------------------------- #
    screen.fill(col_background)

    # update the grid after resolving dead and alive cells
    if not paused:
        cells = update(screen, cells, CELL_SIZE)
    else:
        update(screen, cells, CELL_SIZE)

        # Highlight the cell currently being hovered over by a box
        x, y = pygame.mouse.get_pos()
        pygame.draw.rect(
            screen,
            col_highlight,
            (x // CELL_SIZE * CELL_SIZE,
             y // CELL_SIZE * CELL_SIZE,
             CELL_SIZE,
             CELL_SIZE),
            1
        )

    pygame.display.update()

pygame.quit()
