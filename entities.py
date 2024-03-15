from random import randint
import copy

class Bot:
    def __init__(self, board):
        self.board = board

    def analyze(self, board: list):
        self.board = board
        flag = False
        
        while True:
            j = randint(0, len(self.board[0]) - 1)

            for line in reversed(self.board):
                if line[j] == "0":
                    line[j] = "2"
                    flag = True
                    break
                
            if flag: break

    def getBoardUpdated(self): self.analyze(self.board)

class Connex:
    def __init__(self, board: list[list[str]]) -> None:
        self.board = board
        self.rows, self.columns = len(board), len(board[0])
        self.horizon = 4

    def getBoardUpdated(self):
        board = copy.deepcopy(self.board)
        self.playBestMove(board)

    def getLegalMoves(self, board: list[list[str]]) -> list:
        moves = [[] for _ in range(self.columns)]

        for col in range(self.columns):
            for row in range(self.rows):
                if self.board[row][col] == "0": moves[col] = [row,col]

        legalMoves = []
        for move in moves:
            if move != []: legalMoves.append(move)
        del moves
        
        return legalMoves

    def searchWin(self, board: list[list[str]], vector: tuple[int,int], turn: int):
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

    def checkGameStatus(self, board: list[list[str]], turn: int) -> int:
        checkingVectors = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)]
        for vector in checkingVectors:
            if self.searchWin(board, vector, turn): return turn
        if self.checkDraw(board): return 3
        return 0

    def checkDraw(self, board: list[list[str]]) -> bool:
        for row in self.board:
            for entry in row:
                if entry == "0": return False
        return True

    def getScore1(self, board, gameOver, piece) -> float:
        if gameOver != 0:
            match gameOver:
                case 1: return -float("inf")
                case 2: return float("inf")
                case 3: return 0
        return randint(1,50)

    def getScore(self, board: list[list[str]], gameOver: int, piece: str) -> float:
        score = 0

        if gameOver != 0:
            match gameOver:
                case 1: return -float("inf")
                case 2: return float("inf")
                case 3: return 0

        for row in range(self.rows):
            for col in range(self.columns):
                # Check horizontally
                if col <= self.columns - 4:
                    window = [board[row][col+i] for i in range(4)]
                    score += self.score_window(window, piece)

                # Check vertically
                if row <= self.rows - 4:
                    window = [board[row+i][col] for i in range(4)]
                    score += self.score_window(window, piece)

                # Check positively sloped diagonals
                if col <= self.columns - 4 and row <= self.rows - 4:
                    window = [board[row+i][col+i] for i in range(4)]
                    score += self.score_window(window, piece)

                # Check negatively sloped diagonals
                if col <= self.columns - 4 and row >= 3:
                    window = [board[row-i][col+i] for i in range(4)]
                    score += self.score_window(window, piece)

        return score

    def nline(self, window: str, piece: str, n: int, value: int) -> int:
        score = 0
        if window.count(piece) == n and window.count("0") == 4 - n: score += value
        return score

    def score_window(self, window: list[str], piece: str) -> float:
        score = 0
        opponent_piece = "1" if piece == "2" else "2"
        
        weigths = [-5,100,300,500,600]
        for n in range(0,5): score += self.nline(window, piece, n, weigths[n - 1] * 1) - self.nline(window, piece, n, weigths[n - 1] * 2)

        return score

        # if window.count(piece) == 3 and window.count("0") == 1: score += 500
        # elif window.count(piece) == 2 and window.count("0") == 2: score += 250
        # elif window.count(piece) == 1 and window.count("0") == 3: score += 150
        
        # if window.count(opponent_piece) == 3 and window.count("0") == 1: score -= 550
        # elif window.count(opponent_piece) == 2 and window.count("0") == 2: score -= 275
        # elif window.count(piece) == 1 and window.count("0") == 3: score -= 150
    
    def drop_piece(self, board: list[list[str]], row: int, col: int, piece: str) -> None:
        board[row][col] = piece
        return board

    def max_value(self, board: list[list[str]], iteration: int = 0) -> float:
        gameOver = self.checkGameStatus(board, 2)
        if self.horizon == iteration or gameOver != 0: return self.getScore(board, gameOver, "2")
        value = -float("inf")
        for move in self.getLegalMoves(board):
            value = max(value, self.min_value(self.drop_piece(copy.deepcopy(board), move[0], move[1], "2"), iteration + 1))
        return value

    def min_value(self, board: list[list[str]], iteration: int = 0) -> float:
        gameOver = self.checkGameStatus(board, 2)
        if self.horizon == iteration or gameOver != 0: return -self.getScore(board, gameOver, "1")
        value = float("inf")
        for move in self.getLegalMoves(board):
            value = min(value, self.max_value(self.drop_piece(copy.deepcopy(board), move[0], move[1], "1"), iteration + 1))
        return value

    def playBestMove(self, board: list[list[str]]):
        legalMoves = self.getLegalMoves(board)

        best_score = -float("inf")
        for move in legalMoves:
            score = self.max_value(self.drop_piece(copy.deepcopy(board), move[0], move[1], "2"))
            if score > best_score:
                best_score = score
                best_move = move
        
        self.board = self.drop_piece(self.board, best_move[0], best_move[1], "2")

class Player:
    def __init__(self, board, board_pos, square_size):
        self.moves = []
        self.board = board
        self.board_pos = board_pos
        self.square_size = square_size
        self.placed = False

    def placePiece(self):
        j = int((self.moves[0] - self.board_pos[0])//self.square_size)

        self.placed = False

        for line in reversed(self.board):
            if line[j] == "0":
                line[j] = "1"
                self.placed = True
                break

        self.moves = []

    def getPlaced(self) -> bool:
        if not self.placed: return False
        self.placed = False
        return True

    def getBoardUpdated(self):
        if self.moves: self.placePiece()
