from argparse import Action
from setting import*
import math

# Class board game
class board:
    def __init__(self, level):
        self.matrix = [[INF for j in range(level)] for i in range(level)]
        self.lev = level

    # Check board is empty
    def isEmpty(self):
        return self.marked == 0

    def toMatrix(self, matrix):
        self.matrix =  matrix
        self.lev = len(matrix)

    # Terminal test is -inf if the player is win, if BOT is win, terminal test return inf. 
    # The state where the game ends is called terminal state.
    def terminalTest(self):
        winer = None
        count = 0
        cell_1 = []
        cell_2 = [] # row, col

        if(len(self.matrix) == 3):
            legal = 3
        elif(len(self.matrix) == 5):
            legal = 4
        elif(len(self.matrix) == 7):
            legal = 5

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):

                # Check horizontal
                winer = self.matrix[i][j]
                cell_1 = [i, j]
                if winer != INF:
                    count = 0
                    for k in range(legal - 1):
                        if(j+k+1) < len(self.matrix):
                            if (winer == self.matrix[i][j+k+1]):
                                count += 1

                    if count == legal - 1:
                        cell_2 = [i, j + count]
                        return winer, cell_1, cell_2

                    count = 0

                    # Check vertical
                    for k in range(legal - 1):
                        if(i+k+1) < len(self.matrix):
                            if(winer == self.matrix[i+k+1][j]):
                                count += 1

                    if count == legal - 1:
                        cell_2 = [i + count, j]
                        return winer, cell_1, cell_2

                    # Check diagonal 
                    count = 0
                    for k in range(legal -1):
                        if(i+k+1) < len(self.matrix) and (j+k+1) < len(self.matrix):
                            if(winer == self.matrix[i+k+1][j+k+1]):
                                count += 1

                    if count == legal - 1:
                        cell_2 = [i + count, j + count]
                        return winer, cell_1, cell_2

                    # Check - diagonal
                    count = 0
                    for k in range(legal - 1):
                        if (i+k+1) < len(self.matrix) and (j-k-1) >= 0:
                            if(winer == self.matrix[i+k+1][j-k-1]):
                                count += 1

                    if count == legal - 1:
                        cell_2 = [i + count, j - count]
                        return winer, cell_1, cell_2
                        
        return None, None, None

    # Some mutual method
    def clearBoard(self):
        self.matrix = [[INF for j in range(self.level)] for i in range(self.level)]
        self.marked = 0

    def isEmptyCell(self, row, col):
        if(self.matrix[row][col] == INF):
            return True
        else:
            return False

    def get_empty_cells(self):
        empty = []
        for row in range(len(self.matrix)):
            for col  in range(len(self.matrix)):
                if(self.empty_cell(row, col)):
                    empty.append((row, col))
    
    def isfull(self):
        for i in self.matrix:
            for j in i:
                if j == INF:
                    return False
        return True
    
    def print(self):
        for m in self.matrix:
            print(m)
    # **End**

# Logic class XAT object BOT 
class XAT: # Assign value always equal to -1
    def __init__(self, play, player):
        self.play = play
        self.player = player #  Player

    def action(self, action, _board): # action is move[x,y, utilityMove]
        x = action[0]
        y = action[1]
        _board.matrix[x][y] =  self.play

    def backAction(self, action, _board):
        x = action[0]
        y = action[1]
        _board.matrix[x][y] = INF

    # Calculate the evaluation of current state of board
    def utility(self, _board):
        eval = 0.0
        # Get center position of the board
        middle = (_board.lev-1)/2 
        for i  in range (_board.lev): 
            for j in range(_board.lev):
                if _board.matrix[i][j] == self.play: # For BOT
                    #The evaluation is added a value which 1 divided by the distance of this position to the center position + 1.
                    eval += 1/(math.sqrt((middle-i)**2 + (middle-j)**2)+1) 
                    if i==j or _board.lev-1-i == j or i == _board.lev-1-j: # Check in main diagonal or minor diagonal
                        eval+=0.15 # Added by 0.15

                if _board.matrix[i][j] == self.player.play: # For player
                    # The evaluation is subtracted a value which 1 divided by the distance of this position to the center position + 1.
                    eval -= 1/(math.sqrt((middle-i)**2 + (middle-j)**2)+1)
                    if i==j or _board.lev-1-i == j or i == _board.lev-1-j:
                        eval-=0.15 # Subtracted by 0.15
                    
        return eval
    
    # List of cells that can be typed in the next step.
    def possibleMoves(self, mark, _board):
        result = []
        winner = _board.terminalTest()[0]

        if(winner == None):
            for i in range(_board.lev):
                for j in range(_board.lev):
                    if(_board.isEmptyCell(i,j)):
                        action = [i, j, mark]
                        result.append(action)

        return result

    # Min-Max Algorithm
    def minimaxAlgorithm(self, bot_XAT, depth, alpha, beta, _board):
        winner = _board.terminalTest()[0]
        # Set the stop state
        if(depth == 0 or winner == self.play or winner == self.player.play or winner == None): #depth = 0 or BOT is win or player is win or the match is draw
            if(winner == self.play):
                return float('inf')
            elif(winner == self.player.play):
                return float('-inf')
            elif(_board.isfull() and winner == None): 
                return self.utility(_board) # Calulate the evaluation of current state of board
            elif(depth == 0):
                return self.utility(_board) 

        if bot_XAT == True:
            max_value = float("-inf")
            # List of position that can be typed in the next step
            result = self.possibleMoves(self.play, _board) 
            for r in result:
                self.action(r, _board)
                # Call recursive of Min-Max Algorithm with current depth equals to previous depth 
                # to find the evaluations of all possible move.
                v = self.minimaxAlgorithm(False, depth-1, alpha, beta, _board)
                self.backAction(r, _board)
                max_value = max(max_value, v)
                # For Bot state is True return max value which max value of above list evaluations 
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break
            return max_value
        else:
            min_value = float("inf")
            # List of position that can be typed in the next step
            result = self.possibleMoves(self.player.play, _board)
            for r in result:
                self.player.action(r, _board)
                # Call recursive of Min-Max Algorithm with current depth equals to previous depth 
                # to find the evaluations of all possible move.
                v = self.minimaxAlgorithm(True, depth-1, alpha, beta, _board)
                self.player.backAction(r, _board)
                min_value = min(min_value, v)
                # Opposite that to return min value which min value of above list evaluations
                beta = min(beta, min_value)
                if beta <= alpha:
                    break
            return min_value

#Logic class player
class player: 
    # Assign value always equal to -1
    def __init__(self, play):
        self.play = play

    # Action is move[x,y, utilityMove]
    def action(self, action, _board): 
        x = action[0]
        y = action[1]
        _board.matrix[x][y] =  self.play

    def backAction(self, action, _board):
        x = action[0]
        y = action[1]
        _board.matrix[x][y] = INF
