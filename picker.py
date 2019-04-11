# Roulette Wheel Selection is a common algorithm used to select an item proportional to its probability.

import random
import numpy as np


def tournament(chromosome_population, subset_size):
    """
    Function for tournament selection
    :param chromosome_population:   list of chromosomes objects, holding whole population
    :param subset_size:             size of subset used in tournament
    :return:                        chromosome with the lowest fitness score
    """
    random_idx_list = np.random.choice(list(range(len(chromosome_population))), subset_size, replace=False)

    winner_chromosome = chromosome_population[random_idx_list[0]]
    for idx in random_idx_list:
        if winner_chromosome.get_fitness() < chromosome_population[idx].get_fitness():
            winner_chromosome = chromosome_population[idx]

    return winner_chromosome


class ChromosomePicker:
    def __init__(self):
        self.fitness_values = []
        self.population = []
        self.scaled_list = []

    def feature_scaling(self, input_list):
        max_val = max(input_list)
        min_val = min(input_list)

        for i in range(0, len(input_list)):
            value = (input_list[i] - min_val) / (max_val - min_val)
            self.scaled_list.append(value)

        self.scaled_list = np.divide(self.scaled_list, sum(self.scaled_list))

    def wheel(self):
        if len(self.scaled_list) == 0:
            self.feature_scaling(self.fitness_values)
        random_val = random.uniform(0, 1)

        idx = 0
        cumsum = 0
        while idx < len(self.scaled_list):
            cumsum += self.scaled_list[idx]
            if cumsum > random_val:
                return self.population[idx]
            idx += 1

        return self.population[-1]
