import string, sys

#move list for testing purposes
#moves = ["X", " ", "O", "O", "X", "X", " ", "X", "O"]

#game vars
board_horiz = "-------------\n"
board_vert_empty = "|   |   |   |\n"
moves = [" ", " ", " ", " ", " ", " ", " ", " ", " "] #chars at each square
starting_player = "X" #X is default starting player
active_player = "X"
player_one = "X" #player one defaults to X
player_two = "O" #player two defaults to O
game_type = 2 #1 -> 1 player (Human v Comp), 2 -> 2 players (Human v Human)

#session vars
games_played = 0.0
results = []

prompt = " > "



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
    if games_played == 0.0:
       print "No games have been completed in this session"
       return
    x_wins = o_wins = draws = 0.0
    #tally up results from games in current session
    for result in results:
        if result == "X":
            x_wins += 1.0
        elif result == "O":
            o_wins += 1.0
        elif result == "D":
            draws += 1.0
    #calculate percentages
    x_per = '%.2f' % (x_wins / games_played)
    o_per = '%.2f' % (o_wins / games_played)
    d_per = '%.2f' % (draws / games_played)
    res = "=====Session Statistics=====\n"
    res += "Games: %s\n" % games_played
    res += "X wins: %s , %s\n" % (x_wins, x_per)
    res += "O wins: %s , %s\n" % (o_wins, o_per)
    res += "Draws: %s , %s\n" % (draws, d_per)
    print res
    
#print the board in its current state, takes in a list of the current moves
def draw_board(moves):
    board = board_horiz
    ite = iter(moves) #iterator over list
    for i in range(1,4):
        board += board_vert_empty
        board += "| " + ite.next() + " | " + ite.next() + " | " + ite.next() + " |\n"
        board += board_vert_empty
        board += board_horiz
    print board
    
"""     ***************     PROCESSING FUNCTIONS     ***************     """
    
#prompt user for input at main menu
def prompt_main():
    while True:
        try:
            choice = int(raw_input(prompt))
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
        print "new game"
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
    if winner == "X":
        x_wins += 1
        current = x_wins
    elif winner == "O":
        o_wins += 1
        current = o_wins
    elif winner == "D":
        draws += 1
        current = draws
    else:
        print "We're not really quite sure what just happened"
        return
        
    games_played += 1
    results.append(winner)
    
    if winner == player_one:
        player = "Player 1"
    else:
        player = "Player 2"
    print "Congratulations %s (%s) on the win!" % (player, winner)
    print "%s has now won %s game(s) in this session!" %(winner, current)
        
    
#reset game variables for a new match
def reset_game():
    moves = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    active_player = starting_player
    


            
       
if __name__ == "__main__":
    draw_main()
    process_main()
    
    
    
