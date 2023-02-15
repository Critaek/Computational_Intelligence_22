import Quarto
import Utils
import copy
import numpy

load = Utils.load_cache()
cache = load if load else {}
if load != None:
    print(f"Loaded cache with len: {len(cache)}")

cache["hits"] = 0

MAX_DEPTH = 5

def get_empty_spaces_and_avaiable_pieces(board):
    empty_spaces = list()
    available_pieces = [x for x in range(16)]
    for x in range(4):
        for y in range(4):
            pos = board[y,x]
            if pos != -1:
                available_pieces.remove(pos)
            else:
                empty_spaces.append((x, y))
    return empty_spaces, available_pieces

def minmax(game: Quarto.Quarto, alpha = -1000, beta = 1000, flag = 0, depth = 0):
        # For every turn in quarto each player have to do two things, place a piece
        # and choose a piece to give to the opponent, the flag is used to do that,
        # it goes from 0 to 3, if it's 0 or 1 it means it's our turn, the first time
        # so at 0 we are searching for a place, the second time it's always our turn 
        # but we are looking for the best piece (best for us) to give to the opponent
        # the same happens with the other player, only that it's 2 or 3
        # When the complete turn is finished we can just check if we have 3 and go back to 1
        searching_for_space = flag % 2 == 0
        its_us = flag < 2
        
        # If we reached the max depth or the game is finished, return 0 if it's just finished,
        # -1 if it's us (that means we can't see any further, so it's better for the opponent),
        # +1 if it's the opponent for the same reason before
        if depth == 0 or game.check_finished():
            return None, 0 if game.check_finished() else -1 if its_us else 1
        
        # If someone won, give +1 is it's us, -1 if it's the opponent
        if game.check_winner() != -1:
            return None, 1 if its_us else -1
        
        board = game.get_board_status()
        hash = f"{numpy.array2string(board)} {flag}"
        if hash in cache.keys():
            cache["hits"] += 1
            return cache[hash]

        eval = list()
        empty_spaces, avaiable_pieces = get_empty_spaces_and_avaiable_pieces(board)

        for ply in empty_spaces if searching_for_space else avaiable_pieces:
            board = copy.deepcopy(game)
            if searching_for_space:
                board.place(ply[0], ply[1])
            else:
                board.select(ply)
            _, val = minmax(board, alpha, beta, flag=(flag+1)%4, depth=depth-1)
            eval.append((ply,val))
            if its_us:
                alpha = max(alpha, val)
            else:
                beta = min(beta, val)
            if beta <= alpha:
                break

        if its_us:
            val = max(eval, key = lambda k: k[1])
        else:
            val = min(eval, key = lambda k: k[1])
        cache[hash] = val
        return val

class MyPlayer(Quarto.Player):

    def __init__(self, quarto: Quarto.Quarto, max_depth = MAX_DEPTH) -> None:
        super().__init__(quarto)
        self.max_depth = max_depth

    def choose_piece(self) -> int:
        val = minmax(self.get_game(), flag=1, depth=self.max_depth)[0]
        return val

    def place_piece(self) -> tuple[int, int]:
        return minmax(self.get_game(), flag=0, depth=self.max_depth)[0]

    def get_cache(self):
        return cache
    
    def get_cache_hits(self):
        return cache["hits"]
    