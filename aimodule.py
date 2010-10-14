import random

#determines computer's best move using basic situation-action production system
def comp_move(moves, comp_player):
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
        
    possible = can_pin(comp_player, comp_player, moves)
    if possible != -1: #if comp can pin, do it
        return possible
    possible = can_pin(human_player, comp_player, moves)
    if possible != -1: #if human can pin, block it
        return possible   
        
    possible = is_l_shape(moves)
    if possible != -1: #if comp can exploit or block an L shape, do so
        return possible
        
    possible = is_caddy_corner(moves)
    if possible != -1: #if comp can exploit or block caddy corner, do so
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
def can_pin(pinner, comp, moves):
    side = -1
    if pinner == moves[0] == moves[8] and moves[2] == " ":
        if pinner == comp or moves[6] != " ":
            return 2
        else:
            side = check_sides(moves)
    if pinner == moves[0] == moves[8] and moves[6] == " ":
        if pinner == comp or moves[2] != " ":
            return 6
        else:
            side = check_sides(moves)
    if pinner == moves[2] == moves[6] and moves[0] == " ":
        if pinner == comp or moves[8] != " ":
            return 0
        else:
            side = check_sides(moves)
    if pinner == moves[2] == moves[6] and moves[8] == " ":
        if pinner == comp or moves[0] != " ":
            return 8
        else:
            side = check_sides(moves)
    
    if side != -1:
        return side
    else:
        return -1
    
#return a random unoccupied side square (non-corner, non-center)
def check_sides(moves):
    unoccupied = []
    if moves[1] == " ":
        unoccupied.append(1)
    if moves[3] == " ":
        unoccupied.append(3)
    if moves[5] == " ":
        unoccupied.append(5)
    if moves[7] == " ":
        unoccupied.append(7)
        
    if len(unoccupied) == 0:
        return -1
    else:
        return unoccupied[random.randint(0,len(unoccupied)-1)]
       
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
       
#determines if the ends of an L-shape are in place given board state (-1 if not)
def is_l_shape(moves):
    if moves[7] == moves[0] and moves[0] != " " and moves[3] == moves[6] == " ":
        return 6
    if moves[7] == moves[2] and moves[2] != " " and moves[5] == moves[8] == " ":
        return 8
    if moves[1] == moves[6] and moves[6] != " " and moves[3] == moves[0] == " ":
        return 0
    if moves[1] == moves[8] and moves[8] != " " and moves[5] == moves[2] == " ":
        return 2
    
    if moves[5] == moves[0] and moves[0] != " " and moves[1] == moves[2] == " ":
        return 2
    if moves[5] == moves[6] and moves[6] != " " and moves[7] == moves[8] == " ":
        return 8
    if moves[3] == moves[2] and moves[2] != " " and moves[1] == moves[0] == " ":
        return 0
    if moves[3] == moves[8] and moves[8] != " " and moves[7] == moves[6] == " ":
        return 6
        
    return -1
    
#determines if there is a caddy corner arrangement given board state (-1 if not)
def is_caddy_corner(moves):
    if moves[1] == moves[3] and moves[0] == " ":
        return 0
    if moves[1] == moves[5] and moves[2] == " ":
        return 2
    if moves[7] == moves[3] and moves[6] == " ":
        return 6
    if moves[7] == moves[5] and moves[8] == " ":
        return 8
        
    return -1
