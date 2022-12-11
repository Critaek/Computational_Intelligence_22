# 3.1 Fixed Rules
Just pure_random and gabriele. Also nim_sum. <br />
Strategies are evaluated with the evaluate function by having a tournament with two strategies. The function accepts two strategies and returns the Win Rate of the first strategy passed. <br />
<br/>
<strong> evaluate() Example </strong> <br />
evaluate(strategy_1, strategy_2) <br />
If strategy_1 is <strong> always </strong> better than strategy_2, evaluate will return 1.0, and 0.0 in the opposite case.

# 3.2 Evolved Rules 
Very similar to the last lab, an Individual ha a genome composed by a probability. This is used to find the best probabilty to choose between two strategies, short_first and long_first. <br />
In my case the results are really bad, maybe I am mising something or simply I need a more complex model. Any suggestion will be gratefully accepted!

# 3.3 MinMax
Simple MinMax (also called MiniMax) algorithm, I tried to implement alpha-beta pruning but it wasn't working. <br />
The max_depth limit has been implemented by returning simply 0 point and no move.

# 3.4 Reinforcement Learning Agent
I'm not sure about my implementation, it's maximizing and not minimizing. I thins i messed up something. Any advice will be appreciated.