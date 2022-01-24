import sys
import pygame
import random
import time


class Cell:
    cells = {}

    def __init__(self, coords: tuple, y, x, color="black") -> None:
        self.coords = coords
        self.color = color
        Cell.cells[(x, y)] = self

    def play_in_life(self, cell_id):
        neighbors = []
        for n_id in [(cell_id[0]-1, cell_id[1]-1),
                     (cell_id[0], cell_id[1]-1),
                     (cell_id[0]+1, cell_id[1]-1),
                     (cell_id[0]-1, cell_id[1]),
                     (cell_id[0]+1, cell_id[1]),
                     (cell_id[0]-1, cell_id[1]+1),
                     (cell_id[0], cell_id[1]+1),
                     (cell_id[0]+1, cell_id[1]+1)]:
            try:
                n_cell = Cell.cells[n_id]
                neighbors.append(n_cell)
            except KeyError:
                pass
        n_length = len([True for n in neighbors if n.color == "green"])
        if 3 >= n_length >= 2:
            if n_length == 3:
                self.color = "green"
        else:
            self.color = "black"


def runner(screen: pygame.Surface, amount: tuple, cell_size=10, frequence: float = 0.04):
    width_amount, height_amount = amount

    for y in range(height_amount//cell_size):
        start_pos, end_pos = [0, 0], [cell_size, cell_size]
        for x in range(width_amount//cell_size):
            start_pos[1], end_pos[1] = y * cell_size, cell_size + y * cell_size
            Cell((*start_pos, *end_pos), y+1, x+1)
            start_pos[0] += cell_size
            end_pos[0] += cell_size

    all_cells = list(Cell.cells.values())
    random.shuffle(all_cells)
    for green_cell in all_cells[:int(len(all_cells)*frequence):]:
        green_cell.color = "green"
    while True:
        start = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((0, 0, 0))
        for cell_id, cell in Cell.cells.items():
            cell.play_in_life(cell_id)
        for cell in Cell.cells.values():
            pygame.draw.rect(screen, cell.color, cell.coords)
        pygame.display.flip()
        time_dif = time.time()-start
        if time_dif < 0.1:
            time.sleep(0.1-time_dif)


if __name__ == '__main__':
    # It works correctly with amount of cells less than 160 000. Be sure that with*height/cell_size**2 <= 160 000.
    pygame.init()
    size = width, height = 900, 900
    display = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    runner(display, size)