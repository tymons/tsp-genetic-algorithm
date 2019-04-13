# Roulette Wheel Selection is a common algorithm used to select an item proportional to its probability.

import random
import numpy as np


def rank_selection(chromosome_population):
    """
    NOT IMPLEMENTED!
    :param chromosome_population:
    :return:
    """
    return 0


def roulette_wheel(chromosome_population):
    fitness_list = list(map(lambda chromosome: chromosome.get_fitness(), chromosome_population))

    # Scaling to vector which sum up to one
    max_val = max(fitness_list)
    min_val = min(fitness_list)
    scaled_fitness_list = list(map(lambda x: ((x - min_val)/(max_val - min_val)), fitness_list))
    scaled_fitness_list = np.divide(scaled_fitness_list, sum(scaled_fitness_list))

    random_val = random.uniform(0, 1)

    idx = 0
    cumulative_sum = 0
    while idx < len(scaled_fitness_list):
        cumulative_sum += scaled_fitness_list[idx]
        if cumulative_sum > random_val:
            return chromosome_population[idx]
        idx += 1

    return chromosome_population[-1]


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
