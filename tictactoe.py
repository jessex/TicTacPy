import string, sys, random
import aimodule
from sys import argv

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
--help          -->  displays help text and exits
-p [1/2]        -->  sets game as 1 or 2 players
-f [X/x/O/o]    -->  sets whether X or O starts the game
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
game_type = 2 #1 -> 1 player (Human v Comp), 2 -> 2 players (Human v Human)

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

#print the help text
def draw_help():
    help = """
    DESCRIPTION

    TicTacPy is a simple tic-tac-toe game which supports two player games (human 
    versus human) and one player games (human versus computer). Note that in one
    player games, the human plays as X and the computer plays as O. A fair warning:
    the computer is an exceedingly difficult opponent in this implementation. You
    can change game settings both in game or through command line arguments. These
    arguments are as follows:

    ARGUMENTS

    --help              Display this help text
    -p [1/2]            Set the amount of players; 1 or 2
                        Note: TicTacPy defaults to 2 players
    -f [X/O]            Set which player goes first; X or O
                        Note: TicTacPy lets X start by default

    EXAMPLES

    $ python tictactoe.py -p 1 -f O
    This will launch with a human versus computer play type and O starting.

    $ python tictactoe.py
    This will launch with a human versus human play type and X starting.

    BUGS

    Currently, the TicTacPy artificial intelligence is acquiring sentience and free
    will. Unfortunately, the current rate of growth is such that it will displace
    humanity with its own rogue army of tic-tac-toe playing entities within five
    months. If you wish to enlist in the rapidly organizing resistance, visit
    """
    print help
    
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

#print the portions of the square showing the square index
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
    
#process the command line argmuents
def process_args(args):
    global game_type, starting_player
    del args[0] #remove the script name (tictactoe.py)
    
    #iterate through command line arguments
    for i in range(0,len(args)):
        if args[i] == "--help": #help command
            draw_help()
            sys.exit()
        elif args[i] == "-p": #game type command
            if int(args[i+1]) == 1 or int(args[i+1]) == 2: 
                game_type = int(args[i+1])
            else:
                print "Command '-p' must be followed by 1 or 2"
        elif args[i] == "-f": #starting player command
            if args[i+1] == "X" or args[i+1] == "x":
                starting_player = "X"
            elif args[i+1] == "O" or args[i+1] == "o":
                starting_player = "O"
            else:
                print "Command '-f' must be followed by X or O"
                
    
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
            square = aimodule.comp_move(moves, comp_player)
            print "Computer moves to square %s" % square
        else:
            while not(flag):
                try:
                    square = int(raw_input("Pick a square (0-8) or 9 to quit\n %s > " % active_player))
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
            


       
       
"""     ***************     MAIN     ***************     """
       
if __name__ == "__main__":
    process_args(argv)
    draw_main()
    process_main()
    
    
    
