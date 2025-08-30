import pygame
import random
import numpy as np
import math
import sys
import time


# Constants

WINDOW_SIZE = 400
GRID_SIZE = 4
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
PADDING = 10

COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

BACKGROUND_COLOR = (187, 173, 160)
TEXT_COLOR = (119, 110, 101)


# Game Class

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("2048 with AI Mode")
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.font = pygame.font.Font(None, 36)
        self.add_new_tile()
        self.add_new_tile()
        self.ai_mode = False # toggle AI on/off

    def add_new_tile(self):
        """Randomly place a new tile (2 or 4) in an empty cell."""
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def draw(self):
        """Draws the game grid and numbers."""
        self.screen.fill(BACKGROUND_COLOR)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                x = j * CELL_SIZE + PADDING
                y = i * CELL_SIZE + PADDING
                width = CELL_SIZE - 2 * PADDING
                pygame.draw.rect(self.screen, COLORS.get(value, COLORS[0]), 
                               (x, y, width, width), border_radius=5)
                if value != 0:
                    text = self.font.render(str(value), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=(x + width/2, y + width/2))
                    self.screen.blit(text, text_rect)
        pygame.display.flip()

    # Movement logic
    def move(self, direction):
        original_grid = self.grid.copy()
        # Horizontal moves
        if direction in ['LEFT', 'RIGHT']:
            for i in range(GRID_SIZE):
                row = list(self.grid[i])

                if direction == 'RIGHT':   # Reverse row for RIGHT move
                    row = row[::-1]
                
                # Step 1: remove zeros
                row = [x for x in row if x != 0]

                # Step 2: merge identical adjacent tiles
                j = 0
                while j < len(row) - 1:
                    if row[j] == row[j + 1]:
                        row[j] *= 2
                        row.pop(j + 1)  # remove merged tile
                    j += 1

                # Step 3: add zeros to maintain grid size
                row.extend([0]*(GRID_SIZE-len(row)))

                # Flip back if RIGHT move
                if direction == 'RIGHT':
                    row = row[::-1]
                self.grid[i] = row
        # Vertical moves
        elif direction in ['UP', 'DOWN']:
            for j in range(GRID_SIZE):
                col = list(self.grid[:, j])
                if direction == 'DOWN':
                    col = col[::-1]
                col = [x for x in col if x != 0]
                i = 0
                while i < len(col)-1:
                    if col[i] == col[i+1]:
                        col[i] *=2
                        col.pop(i+1)
                    i+=1
                col.extend([0]*(GRID_SIZE-len(col)))
                if direction == 'DOWN':
                    col = col[::-1]
                self.grid[:, j] = col

        # If grid changed, add new tile
        if not np.array_equal(original_grid, self.grid):
            self.add_new_tile()

    def game_over(self):
        """Check if no moves are possible (no empty cells + no merges)."""
        if 0 in self.grid:
            return False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE-1):
                if self.grid[i][j] == self.grid[i][j+1] or self.grid[j][i] == self.grid[j+1][i]:
                    return False
        return True


# AI


class AI:
    def __init__(self, game):
        self.game = game
        self.directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def get_move(self):
        best_score = -float('inf')
        best_move = None
        for move in self.directions:
            grid_copy = self.game.grid.copy()
            new_grid, changed = self.simulate_move(grid_copy, move)
            if not changed:
                continue
            score = self.evaluate(new_grid)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def simulate_move(self, grid, direction):
        """Simulate move on a grid array, returns (new_grid, changed_flag)"""
        g = grid.copy()
        changed = False

        def merge_line(line):
            original = list(line)
            line = [x for x in line if x != 0]
            i = 0
            while i < len(line)-1:
                if line[i] == line[i+1]:
                    line[i] *= 2
                    line.pop(i+1)
                i += 1
            line.extend([0]*(GRID_SIZE-len(line)))
            return line, line != original

        if direction in ['LEFT', 'RIGHT']:
            for i in range(GRID_SIZE):
                row = list(g[i])
                if direction == 'RIGHT':
                    row = row[::-1]
                new_row, changed_row = merge_line(row)
                if direction == 'RIGHT':
                    new_row = new_row[::-1]
                if not np.array_equal(g[i], new_row):
                    changed = True
                g[i] = new_row
        else:
            for j in range(GRID_SIZE):
                col = list(g[:, j])
                if direction == 'DOWN':
                    col = col[::-1]
                new_col, changed_col = merge_line(col)
                if direction == 'DOWN':
                    new_col = new_col[::-1]
                if not np.array_equal(g[:, j], new_col):
                    changed = True
                g[:, j] = new_col

        return g, changed

    def evaluate(self, grid):
        empty_cells = len([(i,j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j]==0])
        max_tile = np.max(grid)
        corner_bonus = 0
        if grid[0][0]==max_tile or grid[0][GRID_SIZE-1]==max_tile or grid[GRID_SIZE-1][0]==max_tile or grid[GRID_SIZE-1][GRID_SIZE-1]==max_tile:
            corner_bonus = max_tile*2
        smoothness = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE-1):
                smoothness -= abs(grid[i][j]-grid[i][j+1])
                smoothness -= abs(grid[j][i]-grid[j+1][i])
        return empty_cells*100 + corner_bonus + smoothness



# Main Loop

def main():
    pygame.init()
    clock = pygame.time.Clock()
    game = Game2048()
    ai = AI(game)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not game.ai_mode:
                    if event.key == pygame.K_LEFT:
                        game.move('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        game.move('RIGHT')
                    elif event.key == pygame.K_UP:
                        game.move('UP')
                    elif event.key == pygame.K_DOWN:
                        game.move('DOWN')
                if event.key == pygame.K_a:
                    game.ai_mode = not game.ai_mode

        if game.ai_mode and not game.game_over():
            move = ai.get_move()
            if move:
                game.move(move)
                # optional small delay for watching AI
                time.sleep(0.05)

        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main()
