import logging
from collections import namedtuple
import random
from typing import Callable
from copy import deepcopy
from itertools import accumulate
from operator import xor

Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    # Example with k = 3, where k is the number of rows
    #   *
    #  ***
    # *****

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    # Make an action in the game (a ply is a move by one player)
    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects


# Random Strategy, this is the same as the professor code, it takes a random number
# of sticks (objects) from a random row
def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

# Gabriele Strategy, also from the prof's code
def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))
    

# Function that calculate the mathematical way of solving Nim
def nim_sum(state: Nim) -> int:
    # With *_, result we skip all the returned element apart from the last, which will be store in result
    *_, result = accumulate(state.rows, xor)
    return result

def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ]
    cooked["active_rows_number"] = sum(o > 0 for o in state.rows)
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longest_row"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]
    cooked["nim_sum"] = nim_sum(state)

    brute_force = list()
    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked["brute_force"] = brute_force

    return cooked

# Function that applies the matematical way of playing Nim
def optimal_strategy(state: Nim) -> Nimply:
    data = cook_status(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]

# Function that make a strategy based on a genome, in this case a genome is a probability,
# it can choose between a play or another
def strategy_to_evolve(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        if random.random() < genome["p"]:
            ply = Nimply(data["shortest_row"], random.randint(1, state.rows[data["shortest_row"]]))
        else:
            ply = Nimply(data["longest_row"], random.randint(1, state.rows[data["longest_row"]]))

        return ply

    return evolvable

# GLOBAL VARIABLES #
NUM_MATCHES = 100
NIM_SIZE = 5

# Function to perform a tournament with NUM_MATCHES matches, it returns the fraction of games
# won by the strategy function (the first parameter), so if we pass as strategy the optimal_strategy
# and as the opponent pure_random (for example), it will return 1.0
def evaluate(strategy: Callable, opponent: Callable) -> float:
        opponents = (strategy, opponent)
        won = 0

        for m in range(NUM_MATCHES):
            nim = Nim(NIM_SIZE)
            player = 0
            while nim:
                ply = opponents[player](nim)
                nim.nimming(ply)
                player = 1 - player
            if player == 1:
                won += 1

        logging.debug(f" Player 0 won {won} time in {NUM_MATCHES} game, corresponding to {won / NUM_MATCHES * 100} % of the games")

        return won / NUM_MATCHES


# In this individual, the lower the module, the best we can evolve the strategy
class Individual:
    def __init__(self, opponent: Callable):
        self.genome = {"p" : round(random.random(), 3)}
        self.module = 0.01
        self.opponent = opponent
        self.fitness = self.cal_fitness()

    def recal_fitness(self):
        self.fitness = self.cal_fitness()

        return self
    
    def cal_fitness(self):
        return evaluate(strategy_to_evolve(self.genome), self.opponent)

    def mutate(self):
        # In this case i want to have a random mutation in a direction
        # If -1, subtract "module" from "p"
        # If 1, add it
        direction = random.choice([-1,1])
        self.genome["p"] += direction * self.module
        
        # Update the fitness and return the updated Individual
        self.fitness = self.cal_fitness()

        return self

POPULATION_SIZE = 100
MAX_GENERATIONS = 100

# Function that evolves the strategy_to_evolve playing against an opponent
# In this case "p" is the only parameter to optimize
def evolve(opponent: Callable):
    # Initialize the population
    # Each individual will have a random starting "p" with 3 decimal digits at the start
    # and it will updated randomly at every generation
    population = []

    generation = 0

    for _ in range(POPULATION_SIZE):
        population.append(Individual(opponent))

    for _ in range(MAX_GENERATIONS):
        population = sorted(population, key = lambda x: x.fitness, reverse = True)

        new_generation = []

        # 10% of the best individuals will survive
        individuals_to_survive = int(0.1 * POPULATION_SIZE)
        for i in range(individuals_to_survive):
            new_generation.append(population[i].recal_fitness())

        # The other 90% will mutate
        mutants = population[individuals_to_survive:]
        for ind in mutants:
            new_generation.append(ind.mutate())

        population = new_generation
        generation += 1

        print(f"Generation -> {generation} Best found so far: {population[0].fitness}")
    
    population = sorted(population, key = lambda x: x.fitness, reverse = True)

    # Return the strategy with the best genome found
    return strategy_to_evolve(population[0].genome)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    evolved_strategy = evolve(gabriele)
    print( evaluate(evolved_strategy, pure_random) )