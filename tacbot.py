import pygame
import math
import copy

pygame.init()

# Vars
WIDTH = 1280
HEIGHT = 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
INF = math.inf
running = True

board = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
turn = 0

# Icons
boardIcon = "Icons/board.png"
pieces = [
    "Icons/x.png",
    "Icons/o.png"
]

# Dimenions and stuff
cellSize = HEIGHT / 4
boardPos = ((WIDTH/2) - 1.5*cellSize, (HEIGHT/2) - 1.5*cellSize)
pieceSize = cellSize * 0.75
piecePadding = (cellSize - pieceSize) / 2

# Functions
def drawSprite(img, pos=(0,0), size=(100,100)):
    img = pygame.image.load(img)
    img = pygame.transform.scale(img, size)
    img = SCREEN.blit(img, pos)
    return img

def clamp(val, minv, maxv):
    return max(min(val, maxv), minv)

def checkWin(b):
    winStates = [
        [[0,0],[0,1],[0,2]],
        [[1,0],[1,1],[1,2]],
        [[2,0],[2,1],[2,2]],
        [[0,0],[1,0],[2,0]],
        [[0,1],[1,1],[2,1]],
        [[0,2],[1,2],[2,2]],
        [[0,0],[1,1],[2,2]],
        [[0,2],[1,1],[2,0]]
    ]

    for state in winStates:
        if (board[state[0][0]][state[0][1]] == board[state[1][0]][state[1][1]]) and (board[state[0][0]][state[0][1]] == board[state[2][0]][state[2][1]]):
            return board[state[0][0]][state[0][1]]
        if (not -1 in board):
            return -2
    return -1

def computerMove(b, t, goal, r, d):
    computerMove(b, int(not bool(t)), goal, False, d-1)

def getMouseGrid():
    mouse = pygame.mouse.get_pos()
    mouse = [math.floor((mouse[0] - boardPos[0]) / 200), math.floor((mouse[1] - boardPos[1]) / 200)]

    return [clamp(mouse[1], 0, 2), clamp(mouse[0], 0, 2)]

while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
            break
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if event.button == 1:
                square = getMouseGrid()
                if board[square[0]][square[1]] == -1:
                    board[square[0]][square[1]] = turn
                    turn = int(not bool(turn))
                    bestMove = computerMove(board, turn, turn, True, 3)
                    print(bestMove)
                    board[bestMove[0]][bestMove[1]] = turn
                    print(bestMove)
    
    SCREEN.fill("#1e1e1e")
    drawSprite(boardIcon, boardPos, (cellSize*3, cellSize*3))
    for row in range (len(board)):
        for col in range (len(board[0])):
            if (not board[row][col] == -1):
                drawSprite(pieces[board[row][col]], (boardPos[0] + (cellSize) * col + piecePadding, boardPos[1] + (cellSize) * row + piecePadding), (pieceSize,pieceSize))
    
    pygame.display.update()