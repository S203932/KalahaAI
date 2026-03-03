import numpy as np 


# The first 6th represents the 6 pits and the 7th represents the goal
# of the given player
player = np.array([6,6,6,6,6,6,0])

# The board is the 2 arrays for each player half of the board
board = np.array([player,player])

def pointsOfPlayer(playerNumber:int, board:np.array):
    return board[playerNumber][6]



def moveRocksFromPitt(playerNumber:int, board:np.array, pittNumber:int) -> int:
    """
    Input:\n
    playerNumber: 0 or 1 for selecting the player\n
    pittNumber: Counting from the left to the right\n
    board: 2X7 np.array of the board\n
    Return:\n
    0 for normal\n
    1 for extra turn\n
    -1 for invalid pittnumber
    """
    
    # Checking if the selected pitt exists on the board
    if pittNumber > 5 or pittNumber < 0:
        return -1
    
    stones:int = board[playerNumber][pittNumber]

    board[playerNumber][pittNumber] = 0

    # Moving all the stones until there are none left
    currentPlayer:int = playerNumber
    currentPitt:int = (pittNumber+1)
    while stones > 0:

        # If it exceeds the constraints of the board, then set it to the other row/side
        if currentPitt > 6 or currentPitt > 5 and currentPlayer != playerNumber:
            currentPitt = 0
            currentPlayer = (currentPlayer + 1)%2
                
        board[currentPlayer][currentPitt] += 1
        stones -= 1
        currentPitt +=1

    # The current pitt is moved forward by the while loop and has to be placed one back
    # to account for the actual currentpitt
    currentPitt -= 1

    # If one ends in an empty pitt on your side, then you shall receive all the stones
    # from both sides 
    # So if the last pitt is on your side of the board and it currently only contains 1
    # i.e. the last one you added, then it should give you all of the stones
    # Also, it doesn't count if the current pitt is your goal

    if currentPlayer == playerNumber and currentPitt != 6 and board[currentPlayer][currentPitt] == 1:
        
        # Empty the current pitt into the current players goal 
        board[playerNumber][6] += board[currentPlayer][currentPitt]
        board[currentPlayer][currentPitt] = 0

        opposingPlayer = (playerNumber + 1)%2

        #Empty the opposing players pitt into the current players goal
        board[playerNumber][6] += board[opposingPlayer][currentPitt]
        board[opposingPlayer][currentPitt] = 0


    # If the last stone ends in the current players goal, then they get an extra turn
    if playerNumber == currentPlayer and currentPitt == 6:
        # Indicates that the player should get another turn
        return 1
    
    # The turn ends as normal
    return 0




# Temporary for testing
tempPlayer1 = np.array([0,6,6,6,6,6,10])
tempPlayer2 = np.array([7,6,6,6,6,6,0])

# Temporary board for testing
tempBoard = np.array([tempPlayer1,tempPlayer2])

print(tempBoard)
print(f'\nShould they get an extra turn: {moveRocksFromPitt(1,tempBoard,0)}')
print(tempBoard)
