from gameLogic import *
from AI import *



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



def startGameAI():
    # The first 6th represents the 6 pits and the 7th represents the goal
    # of the given player
    player = np.array([6,6,6,6,6,6,0])

    # The board is the 2 arrays for each player half of the board
    board = np.array([player,player])

    # The currentplayer counter 
    currentPlayer:int = 1

    aiPlayer:int = 1

    # Variable to store extra turn value
    extraTurn:int = 0

    while(not gameOver(board)):

        if(extraTurn == 0):
            currentPlayer = (currentPlayer+1)%2

        print(f'\nPlayer {currentPlayer+1}\'s turn\n')

        ## I need to print it from the point of view from the current player
        ## Arrows should show options and names should be next to their goals

        printTable(board=board, currentPlayer=currentPlayer,choice=True)
        

        # If it is the players turn
        if currentPlayer != aiPlayer:
            ## I should then let them choose which field they want to move the stones from
            playerChoice:int = int(input("Select what field you'd like to move the stones from:"))-1
        
        #Otherwise it is the AI's turn
        else:
            #Get the AI value
            bestCase:PittOption = minimax(depth=7,board=board,maxPlayer=aiPlayer,currentPlayer=currentPlayer)
            playerChoice:int = bestCase.move
            print(f'\nThe AI chooses pitt {playerChoice + 1} as it has the best score of {bestCase.score} stones difference\n')

        extraTurn = moveRocksFromPitt(playerNumber=currentPlayer,board=board,pittNumber=playerChoice)

        ## Print board state again after the move
        print('\nBoard after the move\n')
        printTable(board=board, currentPlayer=currentPlayer,choice=False)

        if(extraTurn == -1):
            print(f'\n\nThe pitt option {playerChoice+1} is not a valid choice.\n')

        elif(extraTurn == 1):
            if currentPlayer != aiPlayer:
                print(f'\n\nThe player ended their turn in their goal. They\'re granted an extra turn.\n')
            else:
                print(f'\n\nThe AI ended its turn in their goal. It\'s granted an extra turn.\n')
        
        else:
            print('\n\n')


    print("\nThe game has ended\n")
    print(f'The player won with {board[0][6]} points to the AI\'s {board[1][6]} points') if board[0][6]>board[1][6] else print(f'The AI won with {board[1][6]} points to the player\'s {board[0][6]} points') if board[0][6]<board[1][6] else print(f'The game is tied as the player has {board[0][6]} points and the AI has {board[1][6]} points')


startGameAI()