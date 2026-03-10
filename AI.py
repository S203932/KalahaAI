import numpy as np
from gameLogic import gameOver, isMoveLegal, moveRocksFromPitt, pointsOfPlayer


# I need to carry forth the information about what pitt it is an the score it has
class PittOption:
    def __init__(self, move:int, score:int):
        self.move=move
        self.score=score


def minimax(depth:int, board:np.ndarray, maxPlayer:int, currentPlayer:int, alpha:int=-73, beta:int=73):
    """
    move: the move that is best
    depth: max depth for the tree
    board: current board state
    maxPlayer: player who stands to benefit
    currentPlayer: player whose turn it is
    """

    # If the maximum depth or the game is over, evaluate the state
    if depth == 0 or gameOver(board):
        return PittOption(-1,evaluate(board, maxPlayer))
    
    isMaximizing:bool = maxPlayer == currentPlayer
    bestScore:int = -73 if isMaximizing else 73
    bestMove:int = -1

    # Traversing each pitt option
    for pitt in range(6):
        # It should only attempt to do it if it's a legal move (need a check)
        if isMoveLegal(board,currentPlayer,pitt):
            # Make a copy of the board to be modified
            newBoard:np.ndarray = board.copy()
            # Make the move
            extraTurn:int = moveRocksFromPitt(playerNumber=currentPlayer,board=newBoard,pittNumber=pitt)
            nextPlayer:int = currentPlayer if extraTurn == 1 else (currentPlayer + 1) % 2
            
            score:int = minimax(depth=depth-1,board=newBoard,maxPlayer=maxPlayer,currentPlayer=nextPlayer, alpha=alpha, beta=beta).score

            if isMaximizing:
                if bestScore < score:
                    bestScore = score
                    bestMove = pitt
                alpha = max(alpha,bestScore)
                
            else:
                if bestScore > score:
                    bestScore = score
                    bestMove = pitt
                beta = min(beta,bestScore)
            
            if beta <= alpha:
                    break

    return PittOption(bestMove,bestScore)


# The evaluation method will be calculating the lead the player has
def evaluate(board:np.ndarray, maxPlayer:int):
    opposingPlayer:int = (maxPlayer+1)%2
    return pointsOfPlayer(maxPlayer, board) - pointsOfPlayer(opposingPlayer, board)


# Heuristic function that prioritize each option is preferred
# So rather than going through each branch in chronological order, order them according to extra turns and
# Amount of points in the goal 

# Caching is also possible at a later point 
# Essentially caching board states with their associated scores (maybe even depth), 
# so they won't have to be calculated again.

