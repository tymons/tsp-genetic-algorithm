import numpy as np


class Chromosome:
    def __init__(self, cities):
        self.__cities = cities
        self.__fitness = self.__calculate_fitness(cities)

    def __calculate_fitness(self, cities):
        fitness = 0
        for idx, city in enumerate(cities):
            if idx + 1 < len(cities):
                fitness += city.get_distance_to(cities[idx + 1])
            else:
                fitness += city.get_distance_to(cities[0])

        return fitness

    def get_fitness(self):
        return self.__fitness

    def get_cities_list(self):
        return self.__cities
