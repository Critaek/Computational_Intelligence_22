from Nim import *
from copy import deepcopy

# In this case False is the player and True is the opponent
# player = True -> actual player
# player = False -> opponent
# We want to maximize True while minimizing False (the opponent)
def minmax(state: Nim, depth: int = 0, player: bool = True, max_depth: int = 4):
    # Get all the possible moves in the given state
    possible = state.possible_moves()
    
    # If the game is over
    if state.is_over() or not possible:
        if player == True:
            return (-1, None) # If True, and over or not possible, it means the opponent won, negative feedback 
        else:
            return (1, None) # If False, it means that player won, good!

    tried = []

    if depth == max_depth:
        return (0, None)

    # Each p is possible move (a ply)
    for m in possible:
        # For each ply, perform it, and call with the other player and so on recursively
        new_state = deepcopy(state)
        new_state.nimming(m)
        
        value, move = minmax(new_state, depth+1, not player)
        tried.append((value, m))

    if player:
        return max(tried, key = lambda x: x[0])
    else:
        return min(tried, key = lambda x: x[0])

# Simple wrapper to take only the move and not the tuple
def minimax(state: Nim):
    return minmax(state, 0, True, 4)[1]