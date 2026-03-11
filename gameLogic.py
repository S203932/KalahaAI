import numpy as np 

def pointsOfPlayer(playerNumber:int, board:np.ndarray):
    return board[playerNumber][6]

def gameOver(board:np.ndarray) -> bool:
    
    return np.any(np.all(board[:, :6] == 0, axis=1))

def isMoveLegal(board:np.ndarray, playerNumber:int, pit:int) -> bool:
    return board[playerNumber][pit] > 0


def moveRocksFromPit(playerNumber:int, board:np.ndarray, pitNumber:int) -> int:
    """
    Input:\n
    playerNumber: 0 or 1 for selecting the player\n
    pitNumber: Counting from the left to the right\n
    board: 2X7 np.array of the board\n
    Return:\n
    0 for normal\n
    1 for extra turn\n
    -1 for invalid pitnumber
    """
    
    # Checking if the selected pit exists on the board
    if pitNumber > 5 or pitNumber < 0:
        return -1
    
    stones:int = board[playerNumber][pitNumber]

    # There must be at least 1 stone in the pit
    if not isMoveLegal(board,playerNumber,pitNumber):
        return -1

    board[playerNumber][pitNumber] = 0

    # Moving all the stones until there are none left
    currentPlayer:int = playerNumber
    currentpit:int = (pitNumber+1)
    while stones > 0:

        # If it exceeds the constraints of the board, then set it to the other row/side
        if currentpit > 6 or currentpit > 5 and currentPlayer != playerNumber:
            currentpit = 0
            currentPlayer = (currentPlayer + 1)%2
                
        board[currentPlayer][currentpit] += 1
        stones -= 1
        currentpit +=1

    # The current pit is moved forward by the while loop and has to be placed one back
    # to account for the actual currentpit
    currentpit -= 1

    # If one ends in an empty pit on your side, then you shall receive all the stones
    # from both sides 
    # So if the last pit is on your side of the board and it currently only contains 1
    # i.e. the last one you added, then it should give you all of the stones
    # Also, it doesn't count if the current pit is your goal

    if currentPlayer == playerNumber and currentpit != 6 and board[currentPlayer][currentpit] == 1:
        
        # Empty the current pit into the current players goal 
        board[playerNumber][6] += board[currentPlayer][currentpit]
        board[currentPlayer][currentpit] = 0

        opposingPlayer = (playerNumber + 1)%2

        #Empty the opposing players pit into the current players goal
        board[playerNumber][6] += board[opposingPlayer][5-currentpit]
        board[opposingPlayer][5-currentpit] = 0

    # Check if any of the two sides on the board are empty
    if np.any(np.all(board[:, :6] == 0, axis=1)):
        
        opposingPlayer = (playerNumber + 1)%2

        # Check which side of the board is empty

        # If the current players side is empty:
        if np.sum(board[playerNumber][:6]) == 0:

            # Empty opposing players stones in currentplayers goal                  
            remaining = np.sum(board[opposingPlayer][:6])

            board[playerNumber][6] += remaining
            board[opposingPlayer][:6] = 0

        # If opponents side is empty
        else:

            # Empty current players stones in opposing players goal
            remaining = np.sum(board[playerNumber][:6])

            board[opposingPlayer][6] += remaining
            board[playerNumber][:6] = 0


    # If the last stone ends in the current players goal, then they get an extra turn
    if playerNumber == currentPlayer and currentpit == 6:
        # Indicates that the player should get another turn
        return 1
    
    # The turn ends as normal
    return 0


def printTable(board:np.ndarray, currentPlayer:int, choice:bool):

    # print the pits of the opposing player in reverse order (don't print the goal)
    opposingPlayer:int = (currentPlayer+1)%2

    opposingPlayerRow:np.ndarray = board[opposingPlayer][::-1]
    currentPlayerRow:np.ndarray = board[currentPlayer]

    emptySpace:str =''
    print('\t\t', end="") 

    for pit in opposingPlayerRow[1:]:
        print(f'[ {pit} ]', end="\t")

    # print the goals of opposing player first - then 6 spaces for the pits and then current players goal
    print(f'\nPlayer {opposingPlayer+1} |{opposingPlayerRow[0]}| \t\t\t\t\t\t\t |{currentPlayerRow[6]}| Player {currentPlayer+1}')


    # print the current player's 6 pits

    print('\t\t', end= '')
    for pit in currentPlayerRow[:6]:   
        print(f'[ {pit} ]', end="\t")
    

    # if the current player can currently choose
    if choice:

        # print arrows in pointing to each pit of the current player
        print("\n\t", end='')
        for i in range(6):
            print("\t  /\\", end='')
        # print the numbers for each arrow with "option:" to the far left
        print('\nOption: ', end='')

        for option in range(1,7):
            print(f'\t  {option}', end='')
        print("\n")

