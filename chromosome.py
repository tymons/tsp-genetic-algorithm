class Chromosome:
    def __init__(self, cities):
        self.cities = cities
        self.fitness = self.__calculate_fitness(cities)

    def __calculate_fitness(self, cities):
        fitness = 0
        for city, idx in cities:
            if idx + 1 < len(cities):
                fitness += city.distance(cities[idx + 1])
            else:
                fitness += city.distance(cities[0])

        return fitness


