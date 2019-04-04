# Roulette Wheel Selection is a common algorithm used to select an item proportional to its probability.

import random
import numpy as np


def tournament(population, fitness, packet_size):
    population_idx = np.random.choice(list(range(len(population))), packet_size, replace=False)

    minimum = fitness[population_idx[0]]
    minimum_idx = population_idx[0]
    for idx in population_idx:
        if minimum < fitness[idx]:
            minimum = fitness[idx]
            minimum_idx = idx

    return population[minimum_idx]


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
