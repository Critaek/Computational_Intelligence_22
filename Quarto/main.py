import Quarto
from Player import RandomPlayer
import pickle
from joblib import Parallel, delayed
from MyPlayer import MyPlayer
import Utils

def play(player0, player1):
    game = Quarto.Quarto()
    n_0 = player0(game)
    n_1 = player1(game)
    game.set_players((n_0, n_1))
    return game.run()

def tournament(num, game):
    """
    Simple function that runs a tournament with num games
    between player0 and player1
    """
    
    win0 = 0
    win1 = 0
    for _ in range(num):
        game.reset()
        if _ % 1 == 0:
            print(_)
        winner = game.run()
        if winner == 0:
            win0 += 1
        if winner == 1:
            win1 += 1

    if win0 > win1:
        print(f"Player 0 won, with a winrate of: {(win0/(win0 + win1))*100}%")
    if win1 > win0:
        print(f"Player 1 won, with a winrate of: {(win1/(win0 + win1))*100}%")
    if win0 == win1:
        print(f"Draw")

def parallel_tournament(num, player0, player1):
    """
    Function that crate a torunament but with parallelization,
    each thread runes a game
    """
    results = Parallel(n_jobs = 4)(delayed(play)(player0, player1) for _ in range(num))
    win0 = results.count(0)
    win1 = results.count(1)

    if win0 > win1:
        print(f"Player 0 won, with a winrate of: {(win0/(win0 + win1))*100}%")
    if win1 > win0:
        print(f"Player 1 won, with a winrate of: {(win1/(win0 + win1))*100}%")
    if win0 == win1:
        print(f"Draw")

def build_cache():
    for _ in range(20):
        game = Quarto.Quarto()
        random_player = RandomPlayer(game)
        my_player = MyPlayer(game, 15)
        game.set_players((my_player, random_player))
        tournament(5, game)
        cache = my_player.get_cache()
        print(f"Cache size: {len(cache)}")
        print(f"In these game the cache hits were: {my_player.get_cache_hits()}")
        Utils.save_cache(cache)

if __name__ == "__main__":
    # build_cache()
    game = Quarto.Quarto()
    random_player = RandomPlayer(game)
    my_player = MyPlayer(game, 10)
    game.set_players((my_player, random_player))
    tournament(10, game)
    print(f"In these torunament the cache hits were: {my_player.get_cache_hits()}")

    
