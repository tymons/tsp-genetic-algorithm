# Roulette Wheel Selection is a common algorithm used to select an item proportional to its probability.

import random
import numpy as np


class RouletteWheel:
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

    def tournament(self, population_with_fitness, packet_size):
        fit_sub = np.random.choice([x[1] for x in population_with_fitness], packet_size, replace=False)
        elem = population_with_fitness[np.argmin(fit_sub)]
        return elem