import heapq
import random
import logging
from random import seed, choice
from typing import Callable
import numpy as np
N = 5
SEED = 42


class PriorityQueue:
    """A basic Priority Queue with simple performance optimizations"""

    def __init__(self):
        self._data_heap = list()
        self._data_set = set()

    def __bool__(self):
        return bool(self._data_set)

    def __contains__(self, item):
        return item in self._data_set

    def push(self, item, p=None):
        assert item not in self, f"Duplicated element"
        if p is None:
            p = len(self._data_set)
        self._data_set.add(item)
        heapq.heappush(self._data_heap, (p, item))

    def pop(self):
        p, item = heapq.heappop(self._data_heap)
        self._data_set.remove(item)
        return item

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

PROBLEM = problem(N, SEED)

def goal_test(state):
    new = set()
    #Concatenation of all lists without duplicates, a state is a list of lists (subset of problem)
    for list in state.data: 
        new.add(list)
    
    test = [x for x in range(N)]

    return all(x in new for x in test) #Returns True if all elements of "test" are contained in "new"

class State:
    def __init__(self, data: list):
        self._data = data.copy()
        #self._data.flags.writeable = False

    def __hash__(self):
        return hash(bytes(self._data))

    def __eq__(self, other):
        return bytes(self._data) == bytes(other._data)

    def __lt__(self, other):
        return bytes(self._data) < bytes(other._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    @property
    def data(self):
        return self._data

    def copy_data(self):
        return self._data.copy()

def possible_actions(state):
    #Return a possible action, in this case adding a list from the original problem A(s)
    return [l for l in PROBLEM]

def result(state, action):
    #Return new state with action a performed R(s, a)
    return State(state.data + action)

def search(
    initial_state: State,
    goal_test: Callable,
    parent_state: dict,
    state_cost: dict,
    priority_function: Callable,
    unit_cost: Callable,
):
    frontier = PriorityQueue()
    parent_state.clear()
    state_cost.clear()

    state = initial_state
    parent_state[state] = None
    state_cost[state] = 0

    while state is not None and not goal_test(state):
        for a in possible_actions(state):
            #print(f"Action: {a}")
            new_state = result(state, a)
            #print(f"New State: {new_state}")
            cost = unit_cost(a)
            if new_state not in state_cost and new_state not in frontier:
                parent_state[new_state] = state
                state_cost[new_state] = state_cost[state] + cost
                frontier.push(new_state, p=priority_function(new_state))
                logging.debug(f"Added new node to frontier (cost={state_cost[new_state]})")
            elif new_state in frontier and state_cost[new_state] > state_cost[state] + cost:
                old_cost = state_cost[new_state]
                parent_state[new_state] = state
                state_cost[new_state] = state_cost[state] + cost
                logging.debug(f"Updated node cost in frontier: {old_cost} -> {state_cost[new_state]}")
        if frontier:
            state = frontier.pop()
        else:
            state = None

    path = list()
    s = state
    while s:
        path.append(s.copy_data())
        s = parent_state[s]

    logging.info(f"Found a solution in {len(path):,} steps; visited {len(state_cost):,} states")
    return list(reversed(path))

parent_state = dict()
state_cost = dict()
INITIAL_STATE = State(list([]))

logging.getLogger().setLevel(logging.INFO)

#print(PROBLEM)

final = search(
    INITIAL_STATE,
    goal_test=goal_test,
    parent_state=parent_state,
    state_cost=state_cost,
    priority_function=lambda s: len(state_cost),
    unit_cost=lambda a: len(a),
)

print(final)