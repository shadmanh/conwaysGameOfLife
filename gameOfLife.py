# Conway's Game of Life
# By: Shadman Hassan

# Here is my version of Conway's game of life. This was built in Python 3.9.0 with Pygame 2.1.2, SDL 2.0.18.
# The program accepts lines of input coordinates of the form:
# (x, y)
# where x, y are in the 64 bit signed range of integers. The program will start with the input at generation 0
# and will draw the generation on screen with each alive cell being represented as a white square. Every
# subsequent generation will be drawn until any key is pressed by the user, at which point the program will
# terminate. In the render, (0,0) will be at the center of the screen.

import re
import pygame


class gameOfLife:
    # Offset array used to find the neighbour coordinates of any cell
    NEIGHBOUR_ADJUSTMENT = [(-1, -1), (-1, 0), (-1, 1),
                            ( 0, -1), ( 0, 0), ( 0, 1),
                            ( 1, -1), ( 1, 0), ( 1, 1)]

    # Size of printed grid in standard output
    SIZE_OF_DISPLAY_GRID = 20

    # Dimensions of GUI window
    SCREEN_WIDTH = 1900
    SCREEN_HEIGHT = 1000

    # Colours for cell and background when drawn
    CELL_COL = (255, 255, 255)
    BACKGROUND_COL = (0, 0, 0)

    # Side length of each cell displayed in the GUI in terms of pixels
    CELL_PIXEL_SIZE = 10

    # Constructor creates empty Hashset members used to keep track of the alive cells in the current and future gens.
    def __init__(self):
        self.curGenAliveCells = set()
        self.nextGenAliveCells = set()
        self.curGen = 0

        pygame.init()
        self.surface = pygame.display.set_mode((gameOfLife.SCREEN_WIDTH, gameOfLife.SCREEN_HEIGHT))

    # Add cells to the hashset of alive cells in the current gen
    def addAliveCell(self, x, y):
        cell = (x,y)
        if self.isWithinBounds(cell):
            self.curGenAliveCells.add(cell)

    def cellIsOnScreen(self, cell):
        leftBorder = -gameOfLife.CELL_PIXEL_SIZE
        rightBorder = gameOfLife.SCREEN_WIDTH + gameOfLife.CELL_PIXEL_SIZE
        topBorder = -gameOfLife.CELL_PIXEL_SIZE
        bottomBorder = gameOfLife.SCREEN_HEIGHT + gameOfLife.CELL_PIXEL_SIZE

        return (leftBorder <= self.getCellScreenCoordinateX(cell) <= rightBorder and
                topBorder <= self.getCellScreenCoordinateY(cell) <= bottomBorder)

    # Draw cell grid with (0, 0) located in the center of the screen
    def drawCells(self):
        self.surface.fill(gameOfLife.BACKGROUND_COL)
        for cell in self.curGenAliveCells:
            if (self.cellIsOnScreen(cell)):
                cellRect = pygame.Rect(self.getCellScreenCoordinateX(cell), self.getCellScreenCoordinateY(cell),
                                             gameOfLife.CELL_PIXEL_SIZE, gameOfLife.CELL_PIXEL_SIZE)
                pygame.draw.rect(self.surface, gameOfLife.CELL_COL, cellRect)
        pygame.display.flip()

    def getCellScreenCoordinateX(self, cell):
        return gameOfLife.SCREEN_WIDTH // 2 + cell[0] * gameOfLife.CELL_PIXEL_SIZE

    def getCellScreenCoordinateY(self, cell):
        return gameOfLife.SCREEN_HEIGHT // 2 + cell[1] * gameOfLife.CELL_PIXEL_SIZE
        
    # Returns the nth neighbour of cell.
    # Note: n = 4 will return the cell itself as NEIGHBOUR_ADJUSTMENT[4] does no adjustments to the cell.
    def getNthNeighbour(self, cell, n):
        return (cell[0] + gameOfLife.NEIGHBOUR_ADJUSTMENT[n][0], cell[1] + gameOfLife.NEIGHBOUR_ADJUSTMENT[n][1])

    # Checks whether a cell has coordinates with integers within the 64 bit signed integer range
    def isWithinBounds(self, cell):
        return -(2 ** 63) <= cell[0] <= (2 ** 63 - 1) and -(2 ** 63) <= cell[1] <= (2 ** 63 - 1)

    # Prints a grid displaying the status of cells of the current gen centered around (0, 0) in standard output.
    # Alive cells are represented as 1's, dead cells as 0's.
    def printGrid(self):
        print("gen " + str(self.curGen))
        for y in range(gameOfLife.SIZE_OF_DISPLAY_GRID):
            lineToPrint = ""
            for x in range(gameOfLife.SIZE_OF_DISPLAY_GRID):
                if (x - gameOfLife.SIZE_OF_DISPLAY_GRID // 2, y - gameOfLife.SIZE_OF_DISPLAY_GRID // 2) in self.curGenAliveCells:
                    lineToPrint += "1 "
                else:
                    lineToPrint += "0 "
            print(lineToPrint)
        print()

    def simulateGeneration(self):
        # Check each alive cell and its 8 neighbours as they are the only ones with a chance to be alive in the generation
        for aliveCell in self.curGenAliveCells:
            for i in range(len(gameOfLife.NEIGHBOUR_ADJUSTMENT)):
                curCell = self.getNthNeighbour(aliveCell, i)

                # If the cell is within bounds and not yet confirmed to be alive next gen, check its 8 neighbours
                if self.isWithinBounds(curCell) and curCell not in self.nextGenAliveCells:
                    aliveNeighbours = 0
                    for x in range(len(gameOfLife.NEIGHBOUR_ADJUSTMENT)):
                        neighbour = self.getNthNeighbour(curCell, x)

                        if self.isWithinBounds(neighbour) and neighbour in self.curGenAliveCells and neighbour != curCell:
                            aliveNeighbours += 1

                    # If there are 2-3 alive neighbours for an alive cell, the current cell will remain alive in the next generation.
                    # If there are exactly 3 alive neighbours for a dead cell, then it will become alive in the next generation.
                    if (curCell in self.curGenAliveCells and 2 <= aliveNeighbours <= 3) or aliveNeighbours == 3:
                        self.nextGenAliveCells.add(curCell)

        # Update the current generation hashset to take on the next generation of alive cells. Reset next gen hashset
        self.curGenAliveCells = self.nextGenAliveCells.copy()
        self.nextGenAliveCells.clear()

        self.curGen += 1

# Parse through input and add each tuple of coordinates to hashset of current generation of alive cells
def getInput(game):
    while True:
        try:
            position = input()
            if position == "":
                break
            coordinates = re.split(', |\(|\)', position)
            game.addAliveCell(int(coordinates[1]), int(coordinates[2]))
        except EOFError as e:
            break

if __name__ == '__main__':
    game = gameOfLife()
    getInput(game)
    game.printGrid()
    game.drawCells()
    running = True

    while running:
        pygame.event.get()

        game.simulateGeneration()

        game.drawCells()

        game.printGrid()

        # Exit if any button is pressed while running
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False

    pygame.quit()
