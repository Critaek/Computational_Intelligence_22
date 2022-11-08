import random

SEED = 42
POPULATION_SIZE = 1000
MAX_GENERATIONS = 10000

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

def random_gene():
        return random.choice([0,1])

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    def cal_fitness(self):
        '''
        Fitness is the total length of the considered lists if the goal is reached (all
        numbers between 0 and N-1 included) or maxint if not
        '''
        numbers = [x for x in range(N)]
        #contains only the contemplated lists
        lists = [PROBLEM[i] for i, x in enumerate(self.chromosome) if x == 1]
        new = set()

        for l in lists:
            new.update(l)

        a = all(x in new for x in numbers)
        if a:
            return sum([len(PROBLEM[i]) for i, x in enumerate(self.chromosome) if x == 1])
        else:
            return len(PROBLEM) + 1
    
    @classmethod
    def generate_chromosome(self):
        return [random_gene() for _ in range(len(PROBLEM))]

    def mate(g1, g2):
        child_chromosome = []

        for gp1, gp2 in zip(g1.chromosome, g2.chromosome):
            prob = random.random()

            if prob < 0.45:
                child_chromosome.append(gp1)

            elif prob < 0.9:
                child_chromosome.append(gp2)

            else:
                child_chromosome.append(random_gene())

        return Individual(child_chromosome)

    def print_list(ind):
        lists = [PROBLEM[i] for i, x in enumerate(ind.chromosome) if x == 1]
        #print(lists)
        return lists

def offspring(N):
    generation = 1

    population = []

    #Generate initial population
    for _ in range(POPULATION_SIZE):
        rand_chromosome = Individual.generate_chromosome()
        population.append(Individual(rand_chromosome))

    for _ in range(MAX_GENERATIONS):
        population = sorted(population, key = lambda x : x.fitness)

        if population[0].fitness == N:
            continue

        new_generation = []

        s = int((10*POPULATION_SIZE)/100)
        new_generation.extend(population[:s])

        s = int((90*POPULATION_SIZE)/100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = Individual.mate(parent1, parent2)
            new_generation.append(child)

        population = new_generation
  
        generation += 1

        #if generation % 100 == 0:
        #    print(f"N = {N} -> Generation: {generation}\tFitness: {population[0].fitness}")

    print(f"N = {N} -> Generation: {generation}\tString: {Individual.print_list(population[0])}\tFitness: {population[0].fitness}")

if __name__ == "__main__":
    for N in [5,10, 20, 100, 500, 1000]:
        PROBLEM = problem(N, SEED)
        #print(PROBLEM)
        offspring(N)