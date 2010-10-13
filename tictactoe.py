import string, sys, random


"""
Game board for reference's sake
-------------
|0  |1  |2  |
|   |   |   |
|   |   |   |
-------------
|3  |4  |5  |
|   |   |   |
|   |   |   |
-------------
|6  |7  |8  |
|   |   |   |
|   |   |   |
-------------

Flag options for reference's sake


"""

#game vars
BOARD_HORIZ = "-------------\n"
BOARD_VERT_EMPTY = "|   |   |   |\n"
moves = [" ", " ", " ", " ", " ", " ", " ", " ", " "] #chars at each square
starting_player = "X" #X is default starting player
active_player = "X"
comp_player = "O" #defaults as Human v Human so No computer player
player_one = "X" #player one defaults to X
player_two = "O" #player two defaults to O
game_type = 1 #1 -> 1 player (Human v Comp), 2 -> 2 players (Human v Human)

#session vars
games_played = 0.0
x_wins = o_wins = draws = 0.0


"""     ***************     DRAWING FUNCTIONS     ***************     """

#draws the main menu and prompts user for input
def draw_main():
    menu = "\n=====Tic Tac Py=====\n"
    menu += " 1. New game\n"
    menu += " 2. Statistics\n"
    menu += " 3. Settings\n"
    menu += " 4. Help\n"
    menu += " 5. Exit\n"
    print menu

#draw the help info
def draw_help():
    print "help"
    
#calculate and print the game results for the current session
def draw_stats():
    global x_wins, o_wins_draws
    if games_played == 0.0:
       print "No games have been completed in this session"
       return
    x_per = '%.2f' % ((x_wins / games_played) * 100)
    o_per = '%.2f' % ((o_wins / games_played) * 100)
    d_per = '%.2f' % ((draws / games_played) * 100)
    res = "=====Session Statistics=====\n"
    res += "Games: %s\n" % int(games_played)
    res += "X wins: %s , %s%%\n" % (int(x_wins), x_per)
    res += "O wins: %s , %s%%\n" % (int(o_wins), o_per)
    res += "Draws: %s , %s%%" % (int(draws), d_per)
    print res
    
#print the board in its current state, takes in a list of the current moves
def draw_board(moves):
    board = BOARD_HORIZ
    ite = iter(moves) #iterator over list
    for i in range(1,4):
        board += get_board_nums(i)
        board += "| " + ite.next() + " | " + ite.next() + " | " + ite.next() + " |\n"
        board += BOARD_VERT_EMPTY
        board += BOARD_HORIZ
    print board

def get_board_nums(num):
    if num == 1:
        return "|0  |1  |2  |\n"
    elif num == 2:
        return "|3  |4  |5  |\n"
    elif num == 3:
        return "|6  |7  |8  |\n"
    else:
        return BOARD_VERT_EMPTY
    
    
"""     ***************     PROCESSING FUNCTIONS     ***************     """
    
#prompt user for input at main menu
def prompt_main():
    while True:
        try:
            choice = int(raw_input(" > "))
        except ValueError: #if users enter a non-integer
            print "Please enter a valid choice (1-5)"
            continue
            
        if not(choice < 6 and choice > 0):
            print "Please enter a valid choice (1-5)"
        else:
            return choice

#control the flow from the user's choice at the main menu
def process_main():
    choice = prompt_main()
    if choice == 1:
        #new game
        game_loop()
    elif choice == 2:
        draw_stats()
        draw_main()
        process_main()
    elif choice == 3:
        #settings
        print "settings"
    elif choice == 4:
        draw_help()
        draw_main()
        process_main()
    elif choice == 5:
        print "Good bye"
        sys.exit()
    else:
        print "We're not really quite sure what just happened"
        sys.exit()
    
#process the results of the game and congratulate the winner
def process_result(winner):
    global games_played, x_wins, o_wins, draws
    if winner == "X":
        x_wins += 1.0
        current = x_wins
    elif winner == "O":
        o_wins += 1.0
        current = o_wins
    elif winner == "D":
        draws += 1.0
        current = draws
    else:
        print "We're not really quite sure what just happened"
        return
        
    games_played += 1
    draw_board(moves)
    
    if winner == player_one:
        player = "Player 1"
    else:
        player = "Player 2"
    if winner == "D":
        print "It's a draw! There have been %s draw(s) in this session!" % int(current)
    else:
        print "Congratulations %s! %s wins!" % (player, winner)
        print "%s has now won %s game(s) in this session!" % (winner, int(current))

#processes the move of the player and alters the game state accordingly
def process_turn(move):
    global active_player
    moves[move] = active_player
    #switch whose turn it is
    if active_player == "X":
        active_player = "O"
    elif active_player == "O":
        active_player = "X"

#checks board to see if game decided yet, returns winner or "N" for not finished
def process_finish():
    #check all winning combinations
    if moves[0] != " ":
        if moves[0] == moves[1] == moves[2]: #first row
                return moves[0]
        if moves[0] == moves[3] == moves[6]: #first col
                return moves[0]
        if moves[0] == moves[4] == moves[8]: #left to right diagonal
                return moves[0]
                
    if moves[2] != " ":
        if moves[2] == moves[5] == moves[8]: #third col
            return moves[2]
        if moves[2] == moves[4] == moves[6]: #right to left diagonal
            return moves[2]
            
    if moves[3] == moves[4] == moves[5]: #second row
        if moves[3] != " ":
            return moves[3]
    if moves[6] == moves[7] == moves[8]: #third row
        if moves[6] != " ":
            return moves[6]
    if moves[1] == moves[4] == moves[7]: #second col
        if moves[1] != " ":
            return moves[7]
            
    #no winner found, so see if table full (draw) or not (unfinished game)
    for move in moves:
        if move == " ":
            return "N" #found a blank, so unfinished
    return "D" #no blanks but no winner, game is a draw
        
        
"""     ***************     GAME FUNCTIONS     ***************     """
    
#reset game variables for a new match
def game_reset():
    global moves, active_player
    moves = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    active_player = starting_player
    
#control loop of an actual tic tac toe game
def game_loop():
    global active_player
    active_player = starting_player
    finished = False
    #takes care of processing for one full game
    while not(finished):
        draw_board(moves)
        flag = False
        #if Human v Comp and it's comp's turn
        if game_type == 1 and active_player == comp_player:
            square = comp_move(moves)
            print "Computer moves to square %s" % square
        else:
            while not(flag):
                try:
                    square = int(raw_input("Pick a square(0-8) or 9 to quit\n %s > " % active_player))
                except ValueError: #if users enter a non-integer
                    print "Invalid input"
                    continue
                
                if not(square < 10 and square > -1):
                    print "Invalid input"
                else:
                    if square == 9: #chose 9 to quit
                        print "Quitting current game"
                        game_reset()
                        draw_main()
                        process_main()
                    else: #chose a square (0-8)
                        if moves[square] != " ":
                            print "Square is already taken"
                        else:
                            flag = True
        #have a valid pick at this point
        process_turn(square)
        game_check = process_finish()
        if game_check == "X" or game_check == "O" or game_check == "D":
            process_result(game_check)
            game_reset()
            draw_main()
            process_main()
            

"""     ***************     AI FUNCTIONS     ***************     """
       
#determines computer's best move using basic situation-action production system
def comp_move(moves):
    if comp_player == "X":
        human_player = "O"
    else:
        human_player = "X"
        
    if moves[4] == " ": #if center still unoccupied, occupy it
        return 4
    
    possible = can_finish(comp_player, moves)
    if possible != -1: #if comp has a winning move, make it
        return possible
    possible = can_finish(human_player, moves)
    if possible != -1: #if human has a winning move, block it
        return possible
        
    possible = can_pin(comp_player, moves)
    if possible != -1: #if comp can pin, do it
        return possible
    possible = can_pin(human_player, moves)
    if possible != -1: #if human can pin, block it
        return possible   
        
    possible = zero_in_set(moves)
    if possible != -1: #if comp can pioneer, do it
        return possible   
        
    possible = one_in_set(comp_player, moves)
    if possible != -1: #if comp can add, do it
        return possible   
    possible = one_in_set(human_player, moves)
    if possible != -1: #if human alone, get next to it
        return possible  
    
        
    #at this stage, pick a random square which is unoccupied and return it
    unoccupied = []
    for i in range(0,9):
        if moves[i] == " ":
            unoccupied.append(i)
    return unoccupied[random.randint(0,len(unoccupied)-1)]
    
#determine if winner can win given the board state (-1 if not)
def can_finish(winner, moves):
    #all rows
    for i in range(0,7):
        if (i % 3) == 0: #first col
            if winner == moves[i] == moves[i+1] and moves[i+2] == " ":
                return i+2
            elif winner == moves[i+1] == moves[i+2] and moves[i] == " ":
                return i
            elif winner == moves[i] == moves[i+2] and moves[i+1] == " ":
                return i+1
        
    #all cols
    for i in range(0,3):
        if winner == moves[i] == moves[i+3] and moves[i+6] == " ":
            return i+6
        if winner == moves[i] == moves[i+6] and moves[i+3] == " ":
            return i+3
    for i in range(3,6):
        if winner == moves[i] == moves[i+3] and moves[i-3] == " ":
            return i-3
       
    #diagonals
    if winner == moves[0] == moves[4] and moves[8] == " ":
        return 8
    if winner == moves[0] == moves[8] and moves[4] == " ":
        return 4
    if winner == moves[4] == moves[8] and moves[0] == " ":
        return 0
    if winner == moves[2] == moves[4] and moves[6] == " ":
        return 6
    if winner == moves[2] == moves[6] and moves[4] == " ":
        return 4
    if winner == moves[4] == moves[6] and moves[2] == " ":
        return 2
    
    return -1
       
#determine if pinner can pin the corners given the board state (-1 if not)
def can_pin(pinner, moves):
    if pinner == moves[0] == moves[8] and moves[2] == " ":
        return 2
    if pinner == moves[0] == moves[8] and moves[6] == " ":
        return 6
    if pinner == moves[2] == moves[6] and moves[0] == " ":
        return 0
    if pinner == moves[2] == moves[6] and moves[8] == " ":
        return 8
        
    return -1
       
#determine if row/col/dia has 2 empty squares given board state (-1 if not)
def one_in_set(player, moves):
    #all rows
    for i in range(0,9):
        if (i % 3) == 0: #first col
            if player == moves[i] and moves[i+1] == moves[i+2] == " ":
                return i+1
        if ((i-1) % 3) == 0: #second col
            if player == moves[i] and moves[i-1] == moves[i+1] == " ":
                return i-1
        if ((i+1) % 3) == 0: #third col
            if player == moves[i] and moves[i-1] == moves[i-2] == " ":
                return i-1

    #all cols
    for i in range(0,3):
        if player == moves[i] and moves[i+3] == moves[i+6] == " ":
            return i+3
    for i in range(3,6):
        if player == moves[i] and moves[i-3] == moves[i+3] == " ":
            return i-3
    for i in range(6,9):
        if player == moves[i] and moves[i-6] == moves[i-3] == " ":
            return i-3
    
    #diagonals
    if player == moves[0] and moves[4] == moves[8] == " ":
        return 4
    if player == moves[4] and moves[0] == moves[8] == " ":
        return 0
    if player == moves[8] and moves[0] == moves[4] == " ":
        return 4
    if player == moves[2] and moves[4] == moves[6] == " ":
        return 4
    if player == moves[4] and moves[0] == moves[6] == " ":
        return 0
    if player == moves[6] and moves[0] == moves[4] == " ":
        return 4
       
    return -1
    
#determine if row/col/dia has 3 empty squares given board state (-1 if not)
def zero_in_set(moves):
    #all rows
    for i in range(0,7):
        if (i % 3) == 0: #first col
            if moves[i] == moves[i+1] == moves[i+2] == " ":
                return i
                
    #all cols
    for i in range(0,3):
        if moves[i] == moves[i+3] == moves[i+6] == " ":
            return i
            
    #diagonals
    if moves[0] == moves[4] == moves[8] == " ":
        return i
    if moves[2] == moves[4] == moves[6] == " ":
        return i
    
    return -1
       
       
       
       
"""     ***************     MAIN     ***************     """
       
if __name__ == "__main__":
    draw_main()
    process_main()
    
    
    
