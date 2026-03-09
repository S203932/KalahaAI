import numpy as np 

def pointsOfPlayer(playerNumber:int, board:np.ndarray):
    return board[playerNumber][6]

def gameOver(board:np.ndarray) -> bool:
    
    return np.any(np.all(board[:, :6] == 0, axis=1))

def isMoveLegal(board:np.ndarray, playerNumber:int, pitt:int) -> bool:
    return board[playerNumber][pitt] > 0


def moveRocksFromPitt(playerNumber:int, board:np.ndarray, pittNumber:int) -> int:
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

    # There must be at least 1 stone in the pitt
    if not isMoveLegal(board,playerNumber,pittNumber):
        return -1

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
        board[playerNumber][6] += board[opposingPlayer][5-currentPitt]
        board[opposingPlayer][5-currentPitt] = 0

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
    if playerNumber == currentPlayer and currentPitt == 6:
        # Indicates that the player should get another turn
        return 1
    
    # The turn ends as normal
    return 0


def printTable(board:np.ndarray, currentPlayer:int, choice:bool):

    # print the pitts of the opposing player in reverse order (don't print the goal)
    opposingPlayer:int = (currentPlayer+1)%2

    opposingPlayerRow:np.ndarray = board[opposingPlayer][::-1]
    currentPlayerRow:np.ndarray = board[currentPlayer]

    emptySpace:str =''
    print('\t\t', end="") 

    for pitt in opposingPlayerRow[1:]:
        print(f'[ {pitt} ]', end="\t")

    # print the goals of opposing player first - then 6 spaces for the pitts and then current players goal
    print(f'\nPlayer {opposingPlayer+1} |{opposingPlayerRow[0]}| \t\t\t\t\t\t\t |{currentPlayerRow[6]}| Player {currentPlayer+1}')


    # print the current player's 6 pitts

    print('\t\t', end= '')
    for pitt in currentPlayerRow[:6]:   
        print(f'[ {pitt} ]', end="\t")
    

    # if the current player can currently choose
    if choice:

        # print arrows in pointing to each pitt of the current player
        print("\n\t", end='')
        for i in range(6):
            print("\t  /\\", end='')
        # print the numbers for each arrow with "option:" to the far left
        print('\nOption: ', end='')

        for option in range(1,7):
            print(f'\t  {option}', end='')
        print("\n")


def startGame():
    # The first 6th represents the 6 pits and the 7th represents the goal
    # of the given player
    player = np.array([6,6,6,6,6,6,0])

    # The board is the 2 arrays for each player half of the board
    board = np.array([player,player])

    # The currentplayer counter 
    currentPlayer:int = 1

    # Variable to store extra turn value
    extraTurn:int = 0

    while(not gameOver(board)):

        if(extraTurn == 0):
            currentPlayer = (currentPlayer+1)%2

        print(f'\nPlayer {currentPlayer+1}\'s turn\n')

        ## I need to print it from the point of view from the current player
        ## Arrows should show options and names should be next to their goals

        printTable(board=board, currentPlayer=currentPlayer,choice=True)
        
        ## I should then let them choose which field they want to move the stones from

        playerChoice:int = int(input("Select what field you'd like to move the stones from:"))-1

        extraTurn = moveRocksFromPitt(playerNumber=currentPlayer,board=board,pittNumber=playerChoice)

        ## Print board state again after the move
        print('\nBoard after the move\n')
        printTable(board=board, currentPlayer=currentPlayer,choice=False)

        if(extraTurn == -1):
            print(f'\n\nThe pitt option {playerChoice+1} is not a valid choice.\n')

        elif(extraTurn == 1):
            print(f'\n\nPlayer {currentPlayer+1} ended their turn in their goal. They\'re granted an extra turn.\n')
        
        else:
            print('\n\n')


    print("\nThe game has ended\n")
    print(f'Player 1 won with {board[0][6]} points to player 2\'s {board[1][6]} points') if board[0][6]>board[1][6] else print(f'Player 2 won with {board[1][6]} points to player 1\'s {board[0][6]} points') if board[0][6]<board[1][6] else print(f'The game is tied as Player 1 has {board[0][6]} points and player 2 has {board[1][6]} points')

#startGame()