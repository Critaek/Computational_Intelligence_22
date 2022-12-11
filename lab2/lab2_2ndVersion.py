import random
from progress.bar import Bar

POPULATION_SIZE = 100
MAX_GENERATIONS = 1000

def problem(N, seed=42):
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
    def generate_chromosome(cls):
        return [random_gene() for _ in range(len(PROBLEM))]
    
    def crossover(g1, g2):
        child_chromosome = []
        cut = int(len(g1.chromosome)/2)
        gp1 = g1.chromosome[0:cut]
        gp2 = g2.chromosome[cut:]
        child_chromosome.extend(gp1)
        child_chromosome.extend(gp2)

        return Individual(child_chromosome)

    def mutation(g1, g2):
        child_chromosome = []
        cut = int(len(g1.chromosome)/2)
        gp1 = g1.chromosome[0:cut]
        gp2 = g2.chromosome[cut:]
        child_chromosome.extend(gp1)
        child_chromosome.extend(gp2)
        #select a random gene and mutate it, from 1 to 0 or viceversa
        n = random.choice(range(len(g1.chromosome)))
        new_gene = 1 - child_chromosome[n]
        child_chromosome[n] = new_gene

        return Individual(child_chromosome)

    def print_list(ind):
        lists = [PROBLEM[i] for i, x in enumerate(ind.chromosome) if x == 1]
        return lists

def offspring(N):
    generation = 0

    population = []

    #Generate initial population
    for _ in range(POPULATION_SIZE):
        rand_chromosome = Individual.generate_chromosome()
        population.append(Individual(rand_chromosome))
        
    with Bar("Processing", max = MAX_GENERATIONS) as bar:  
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
                #every 10 child, one will have a random mutation
                if _ % 10 == 0:
                    child = Individual.mutation(parent1, parent2)
                else:
                    child = Individual.crossover(parent1, parent2)
                
                new_generation.append(child)

            population = new_generation
    
            generation += 1

            bar.next()

            #if generation % 1 == 0:
            #    print(f" N = {N} -> Generation: {generation}\tFitness: {population[0].fitness}")

    population = sorted(population, key = lambda x : x.fitness)

    print(f"N = {N} -> Generation: {generation}\tFitness: {population[0].fitness}")

if __name__ == "__main__":
    SEED = 42
    for N in [20]:
        PROBLEM = problem(N, SEED)
        #print(PROBLEM)
        offspring(N)