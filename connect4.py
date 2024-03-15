from settings import *
from entities import Bot, Connex, Player
from button import Button
import sys

class Connect4:
    def __init__(self):
        self.screen = screen
        self.gameLoopEnable = True
        
        self.initialize()

        self.mainMenuButton = Button(self.screen, WIDTH//2 - 150, HEIGHT//2 - 50, 300, 100, COLORS["light_gray"], "PLAY", "Comic Sans", 72, COLORS["dark_gray"]) 

    def initialize(self):
        self.drawPiece = [False, None]
        self.board = [["0" for _ in range(7)] for _ in range(6)]
        self.turn = 1
        self.gameStatus = 0
        self.inGame = False

        self.player = Player(self.board, (BOARD_TOP_LEFT_X,BOARD_TOP_LEFT_Y), SQUARE_SIZE)
        self.bot = Connex(self.board)

    def cleanScreen(self):
        # Clear the screen
        self.screen.fill(COLORS['dark_gray'])  # Fill the screen with the background color

    def boardDraw(self):
        self.cleanScreen()

        pygame.draw.rect(self.screen, COLORS['light_gray'], pygame.Rect(BOARD_TOP_LEFT_X, BOARD_TOP_LEFT_Y, BOARD_WIDTH, BOARD_HEIGHT))
        pygame.draw.rect(self.screen, COLORS['teal'], pygame.Rect(BOARD_TOP_LEFT_X, 0, BOARD_WIDTH, HEIGHT - BOARD_HEIGHT))

        # Draw pieces on the board based on self.board
        for row in range(6):
            for col in range(7):
                center_x = BOARD_TOP_LEFT_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = BOARD_TOP_LEFT_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2

                color = COLORS["teal"]
                if self.board[row][col] == "1": color = COLORS["red"]
                elif self.board[row][col] == "2": color = COLORS["yellow"]

                pygame.draw.circle(self.screen, color, (center_x, center_y), SQUARE_SIZE // 2 - 5)

    def drawHeldPiece(self, state): 
        if state[0]: pygame.draw.circle(self.screen, COLORS['red'], (state[1][0], HEIGHT - BOARD_HEIGHT - SQUARE_SIZE//2 - 5), SQUARE_SIZE//2) 

    def searchWin(self, board, vector, turn):
        def verify(i, j, vector, turn, count):
            if count == 4: return True
            elif not (-1 < i < len(board) and -1 < j < len(board[0])): return False
            elif board[i][j] != str(turn): return False
            return verify(i + vector[0], j + vector[1], vector, turn, count + 1)

        for i, line in enumerate(board):
            for j, entry in enumerate(line):
                if entry == str(turn):
                    check = verify(i, j, vector, turn, 0)
                    if check: return check
        return False

    def checkGameStatus(self, board: list, turn: int) -> int:
        checkingVectors = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)]
        for vector in checkingVectors:
            if self.searchWin(board, vector, turn): return turn
        if self.checkDraw(self.board): return 3
        return 0

    def checkDraw(self, board: list) -> bool:
        for row in self.board:
            for entry in row:
                if entry == "0": return False
        return True

    def drawWinningLabel(self, player: int) -> None:
        self.cleanScreen()
        color = "red" if player == 1 else "yellow"
        label = MAIN_FONT.render(f"Player {player} won", True, COLORS[color])
        self.screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - label.get_height()//2))

    def drawDrawLabel(self) -> None:
        self.cleanScreen()
        label = MAIN_FONT.render("Draw", True, COLORS["light_gray"])
        self.screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - label.get_height()//2))

    def equal(self, board1: list, board2: list) -> bool:
        for i in range(len(board1)):
            for j in range(len(board1[0])):
                if board1[i][j] != board2[i][j]: return False
        return True

    def gameLoop(self, counter: int, delayTillLabel: int, labelClock: int) -> tuple[int,int,int]:

        if self.getGameStatus() != 0:
            if delayTillLabel == 3*120:
                if self.getGameStatus() != 3: self.drawWinningLabel(self.getGameStatus())
                else: self.drawDrawLabel()

                if labelClock == 10*120:
                    self.inGame = False
                    labelClock = 0
                    delayTillLabel = 0
                labelClock += 1
                
            else:
                self.boardDraw()
                delayTillLabel += 1

        else:
            if self.turn == 1:
                self.player.getBoardUpdated()
                if self.player.getPlaced(): self.turn = 2
                if self.checkGameStatus(self.board, 1) == 1: self.gameStatus = 1
                    
            elif self.turn == 2:
                self.bot.getBoardUpdated()
                self.turn = 1
                if self.checkGameStatus(self.board, 2) == 2: self.gameStatus = 2

            if self.checkGameStatus(self.board, 1) == 3: self.gameStatus = 3

            self.boardDraw()
            self.drawHeldPiece(self.drawPiece)
        
        return counter, delayTillLabel, labelClock

    def mainMenu(self):
        self.cleanScreen()
        self.mainMenuButton.draw()

    def getGameLoopEnable(self) -> bool: return self.gameLoopEnable
    def getGameStatus(self) -> int: return self.gameStatus
    def isInGame(self) -> bool: return self.inGame

    def run(self):
        counter, delayTillLabel, labelClock = 0, 0, 0
        while self.getGameLoopEnable():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameLoopEnable = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    if self.isInGame():
                        if 0 < event.pos[1] < HEIGHT and WIDTH//2 - BOARD_WIDTH//2 < event.pos[0] < WIDTH//2 + BOARD_WIDTH//2: self.drawPiece = [True, event.pos] 
                        else: self.drawPiece = [False, None]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.isInGame():
                        if self.turn == 1 and self.getGameStatus() == 0: self.player.moves = [event.pos[0]]
                    else:
                        if self.mainMenuButton.x <= event.pos[0] <= self.mainMenuButton.x + self.mainMenuButton.width and self.mainMenuButton.y <= event.pos[1] <= self.mainMenuButton.y + self.mainMenuButton.height:
                            if not self.mainMenuButton.getClicked(): self.mainMenuButton.setClicked(True)

            if self.mainMenuButton.getClicked():
                self.inGame = True
                self.mainMenuButton.setClicked(False)

            if self.isInGame(): counter, delayTillLabel, labelClock = self.gameLoop(counter, delayTillLabel, labelClock)
            else:
                self.initialize()
                self.mainMenu()
            pygame.display.update()
        
        pygame.quit()
        sys.exit()
