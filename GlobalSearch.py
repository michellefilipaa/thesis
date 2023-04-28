import random
import numpy as np
from pyariadne import *

pop_size = 10
gen_size = 10
mutation_rate = 0.1


class GlobalSearch:
    """
    |payoff_function: the payoffs for the players
    |d: the number of players in the game
    |lower_bound: the starting point of the interval in which the candidate solutions will be
    |upper_bound: the end point of the interval
    """
    def __init__(self, payoff_function, d=2, lower_bound=-1, upper_bound=1):
        self.payoff_function = payoff_function
        self.d = d
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    """
    |The initial population will be multiple possible roots i.e. Nash equilibria
    |The set of candidate solutions will be points that cover the full domain.
    |This will be done using Latin hypercube sampling.
    |size: the number of candidate solutions in the initial population
    |Returns: the initial population as a set of FloatDPBoundsVectors of dimension d
    """
    def initial_population(self, size):
        temp = []
        population = []

        # Divide each dimension into n equal intervals
        intervals = np.linspace(self.lower_bound, self.upper_bound, size+1)

        # Randomly assign one point to each interval for each dimension
        for i in range(self.d):
            dim_points = [(random.uniform(intervals[j], intervals[j+1])) for j in range(size)]
            random.shuffle(dim_points)
            temp.append(dim_points)

        temp2 = np.column_stack(temp)

        # Convert the type from np.float to Vector
        for row in temp2:
            population.append(FloatDPBoundsVector([x_(float(row[0])), x_(float(row[1]))], dp))

        return population

    """
    |Selection based on fitness.
    |The top 2 are selected for further generation.
    """
    def selection(self, population):
        exp_payoffs = []

        for individual in population:
            exp_payoffs.append(self.fitness(individual))

        # TODO: how to determine which are the best because there are different values for each player
        index1 = random.randint(0, 9)
        index2 = random.randint(0, 9)

        return exp_payoffs[index1], exp_payoffs[index2]

    """
    |Individuals with higher expected payoff are fitter. 
    |Fitness is calculated by subtracting the expected payoff from the maximum expected payoff. 
    |candidate_solution: an individual in the population
    """
    def fitness(self, candidate_solution):
        return self.payoff(candidate_solution)

    """
    |Single point crossover implemented as follows:
    |If mother = [x1,x2] and father = [x3,x4]
    |child1 = [x1,x4] and child2 = [x2,x3]
    |Returns both children
    """
    @staticmethod
    def crossover(mother, father):
        child1 = [mother[0], father[1]]
        child2 = [mother[1], father[0]]

        return child1, child2


    """
    |Real value mutation using a uniform random number generator within the boundary.
    |individual: a candidate solution in the population
    |Returns: the new value of the individual
    """
    def mutation(self, individual):
        n1 = random.uniform(self.lower_bound, self.upper_bound)
        n2 = random.uniform(self.lower_bound, self.upper_bound)

        return individual + Vector[FloatDPBounds]([x_(n1), x_(n2)], dp)

    def evolution(self, population):
        next_gen = []

        for i in range(0, pop_size):
            mother, father = self.selection(population)
            child1, child2 = self.crossover(mother, father)

            if random.random() < mutation_rate:
                child1 = self.mutation(child1)
                child2 = self.mutation(child2)

            next_gen.append(child1)
            next_gen.append(child2)

        return next_gen

    def payoff(self, candidate_solution):
        return self.payoff_function(candidate_solution)
