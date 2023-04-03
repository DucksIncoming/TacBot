import pygame
import math
import copy
import random

pygame.init()
pygame.font.init()

# Vars
WIDTH = 1280
HEIGHT = 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
INF = math.inf
running = True

board = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
turn = 0
mode = "Godmode"
playerPiece = 0

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

def drawText(text, pos, size, color):
    font = pygame.font.SysFont('Roboto', size)
    text_surface = font.render(text, False, color)
    SCREEN.blit(text_surface, pos)

def clamp(val, minv, maxv):
    return max(min(val, maxv), minv)

def isDraw(b):
    for row in range (len(b)):
        for col in range (len(b[0])):
            if (b[row][col] == -1):
                return False
    return True

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
        if (b[state[0][0]][state[0][1]] == b[state[1][0]][state[1][1]]) and (b[state[0][0]][state[0][1]] == b[state[2][0]][state[2][1]]):
            return b[state[0][0]][state[0][1]]
    return -1

def getMouseGrid():
    mouse = pygame.mouse.get_pos()
    mouse = [math.floor((mouse[0] - boardPos[0]) / 200), math.floor((mouse[1] - boardPos[1]) / 200)]

    return [clamp(mouse[1], 0, 2), clamp(mouse[0], 0, 2)]


# Engines
def randomStrat(pBoard, pTurn):
    attempts = 100
    while (attempts > 0):
        attempts -= 1

        row = random.randint(0,2)
        col = random.randint(0,2)
        if (pBoard[row][col] == -1):
                return [row, col]
    return linearStrat(pBoard, pTurn)

def linearStrat(pBoard, pTurn):
    for row in range(len(pBoard)):
        for col in range(len(pBoard[0])):
            if (pBoard[row][col] == -1):
                return [row, col]
    return [-1,-1]

def fillStrat(pBoard, pTurn):
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
        if (pBoard[state[0][0]][state[0][1]] == pBoard[state[1][0]][state[1][1]] and pBoard[state[2][0]][state[2][1]] == -1 and (not pBoard[state[0][0]][state[0][1]] == -1)):
            return [state[2][0], state[2][1]]
        if (pBoard[state[1][0]][state[1][1]] == pBoard[state[2][0]][state[2][1]] and pBoard[state[0][0]][state[0][1]] == -1 and (not pBoard[state[1][0]][state[1][1]] == -1)):
            return [state[0][0], state[0][1]]
        if (pBoard[state[0][0]][state[0][1]] == pBoard[state[2][0]][state[2][1]] and pBoard[state[1][0]][state[1][1]] == -1 and (not pBoard[state[2][0]][state[2][1]] == -1)):
            return [state[1][0], state[1][1]]
    return randomStrat(pBoard, pTurn)
            
def godStrat(pBoard, pTurn):
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
        if (pBoard[state[0][0]][state[0][1]] == pBoard[state[1][0]][state[1][1]] and pBoard[state[2][0]][state[2][1]] == -1 and (not pBoard[state[0][0]][state[0][1]] == -1)):
            return [state[2][0], state[2][1]]
        if (pBoard[state[1][0]][state[1][1]] == pBoard[state[2][0]][state[2][1]] and pBoard[state[0][0]][state[0][1]] == -1 and (not pBoard[state[1][0]][state[1][1]] == -1)):
            return [state[0][0], state[0][1]]
        if (pBoard[state[0][0]][state[0][1]] == pBoard[state[2][0]][state[2][1]] and pBoard[state[1][0]][state[1][1]] == -1 and (not pBoard[state[2][0]][state[2][1]] == -1)):
            return [state[1][0], state[1][1]]
    
    if pBoard[1][1] == -1:
        return [1, 1]
    else:
        return randomStrat(pBoard, pTurn)

def engineMove(mode, pBoard, pTurn):
    if mode == "Linear":
        return linearStrat(pBoard, pTurn)
    if mode == "Random":
        return randomStrat(pBoard, pTurn)
    if mode == "Fill":
        return fillStrat(pBoard, pTurn)
    if mode == "Godmode":
        return godStrat(pBoard, pTurn)

# Main loop
if playerPiece == 1:
    bestMove = engineMove(mode, board, turn)
    if (not bestMove == [-1,-1]):
        board[bestMove[0]][bestMove[1]] = turn
        turn = int(not bool(turn))

while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
            break
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if event.button == 1: 
                square = getMouseGrid()
                if board[square[0]][square[1]] == -1 and (checkWin(board) == -1):
                    board[square[0]][square[1]] = turn
                    turn = int(not bool(turn))
                    if (checkWin(board) == -1):
                        bestMove = engineMove(mode, board, turn)
                        if (not bestMove == [-1,-1]):
                            board[bestMove[0]][bestMove[1]] = turn
                            turn = int(not bool(turn))
    
    SCREEN.fill("#1e1e1e")
    drawSprite(boardIcon, boardPos, (cellSize*3, cellSize*3))
    if checkWin(board) == playerPiece:
        drawText("You Win!!", (100,100), 30, "white")
    if (isDraw(board)):
        drawText("Tie. I am bored.", (100,100), 30, "white")
    elif checkWin(board) == int(not bool(playerPiece)):
        drawText("You Lose nooo :(", (100,100), 30, "white")

    for row in range (len(board)):
        for col in range (len(board[0])):
            if (not board[row][col] == -1):
                drawSprite(pieces[board[row][col]], (boardPos[0] + (cellSize) * col + piecePadding, boardPos[1] + (cellSize) * row + piecePadding), (pieceSize,pieceSize))
    
    pygame.display.update()