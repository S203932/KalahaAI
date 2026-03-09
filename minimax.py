import numpy as np
from main import gameOver, isMoveLegal, moveRocksFromPitt, pointsOfPlayer


# I need to carry forth the information about what pitt it is an the score it has
class PittOption:
    def __init__(self, move:int, score:int):
        self.move=move
        self.score=score


def minimax(depth:int, board:np.ndarray, maxPlayer:int, currentPlayer:int, move:int=-1):
    """
    move: the move that is best
    depth: max depth for the tree
    board: current board state
    maxPlayer: player who stands to benefit
    currentPlayer: player whose turn it is
    """


    # If the maximum depth or the game is over, evaluate the state
    if depth == 0 or gameOver(board):
        return PittOption(move,evaluate(board, maxPlayer))
    
    #If it is the turn of the desired player
    if maxPlayer == currentPlayer:
        # Setting a default worst such that one solution will always be found
        maxEval:PittOption = PittOption(-1,-73)

        # Traversing each pitt option
        for pitt in range(6):
            # It should only attempt to do it if it's a legal move (need a check)
            if isMoveLegal(board,currentPlayer,pitt):
                # Make a copy of the board to be modified
                newBoard:np.ndarray = board.copy()
                # Make the move
                extraTurn:int = moveRocksFromPitt(playerNumber=currentPlayer,board=newBoard,pittNumber=pitt)
                
                #If the currentPlayer is granted an extra turn
                if(extraTurn == 1):
                    #evaluate the move
                    score:int = minimax(depth=depth-1,board=newBoard,maxPlayer=maxPlayer,currentPlayer=currentPlayer).score
                else:
                    #evaluate the move
                    score:int = minimax(depth=depth-1,board=newBoard,maxPlayer=maxPlayer,currentPlayer=(currentPlayer+1)%2).score
                
                # If the move is better than rewrite maxEval
                if maxEval.score < score:
                    maxEval.score = score
                    maxEval.move = pitt 
                
        # Return the value of the node
        return maxEval
    
    # If it is the turn of the opponent
    else:
        # Setting a default worst such that one solution will always be found
        minEval:PittOption = PittOption(-1, 73)

        # Traversing each pitt option
        for pitt in range(6):
            # It should only attempt to do it if it's a legal move (need a check)
            if isMoveLegal(board,currentPlayer,pitt):
                newBoard:np.ndarray = board.copy()
                # Make the move
                extraTurn:int =moveRocksFromPitt(playerNumber=currentPlayer,board=newBoard,pittNumber=pitt)
                
                #If the currentPlayer is granted an extra turn
                if(extraTurn == 1):
                    #evaluate the move
                    score:int = minimax(depth=depth-1,board=newBoard,maxPlayer=maxPlayer, currentPlayer=currentPlayer).score

                else:
                    #evaluate the move
                    score:int = minimax(depth=depth-1,board=newBoard,maxPlayer=maxPlayer, currentPlayer=(currentPlayer+1)%2).score


                # If the move is better than rewrite minEval
                if minEval.score > score:
                    minEval.score = score
                    minEval.move = pitt

        #Return the value of the node
        return minEval


# The evaluation method will be calculating the lead the player has
def evaluate(board:np.ndarray, maxPlayer:int):
    opposingPlayer:int = (maxPlayer+1)%2
    return pointsOfPlayer(maxPlayer, board) - pointsOfPlayer(opposingPlayer, board)