import random
import numpy as np


def rank_selection_with_two_offsprings(chromosome_population):
    """
    Function for picking up chromosomes based on ranked selection algorithm.
    Ranked Selection Algorithm firstly sorts all chromosomes based on their fitness function.
    Then every chromosome is assigned with value reflecting position in the sorted list. Indexes are normalized
    for probability-like values (min-max scaling) and then divided by sum of indexes to add up to one.
    Having such one can perform ordinary roulette selection algorithm which will be not so biased as basic Roulette
    algorithm.
    :param chromosome_population:   set or list of chromosomes
    :return:                        list of two chromosomes picked up based on renk selection algorithm
    """
    chromosome_population_temp = list(chromosome_population)
    chromosome_population_temp.sort(reverse=True)

    range_fitness = range(1, len(chromosome_population_temp))
    range_fitness_scaled = np.divide(range_fitness, sum(range_fitness))

    offsprings_list = []
    for _ in range(1, 2):
        idx = 0
        cumulative_sum = 0

        random_val = random.uniform(0, 1)
        while idx < len(range_fitness_scaled):
            cumulative_sum += range_fitness_scaled[idx]
            if cumulative_sum > random_val:
                offsprings_list.append(chromosome_population[idx])
            idx += 1
        offsprings_list.append(chromosome_population[-1])

    return offsprings_list


# Ta funkcja jest bardzo dziwna, zwraca listę chromosomów, a powinna zwrócić (chyba) jeden.
# Dlaczego 'with_two_offsprings' ?? to selecja rodziców, jak rozumiem, nie potomków
def roulette_wheel_with_two_offsprings(chromosome_population):
    """
    Function that implements roulette wheel selection. One chromosome is picked from whole population based on his fitness score.
    Chromosome which has better fitness score will be selected with higher probability.
    :param chromosome_population:   population will all chromosomes
    :return:                        roulette wheel selected chromosomes
    """
    fitness_list = list(map(lambda chromosome: chromosome.get_fitness(), chromosome_population))

    # Scaling to vector which sum up to one
    max_val = max(fitness_list)
    min_val = min(fitness_list)
    scaled_fitness_list = list(map(lambda x: ((x - min_val) / (max_val - min_val)), fitness_list))
    scaled_fitness_list = np.divide(scaled_fitness_list, sum(scaled_fitness_list))

    offsprings_list = []
    for _ in range(1, 2):               # ?????
        idx = 0
        cumulative_sum = 0

        random_val = random.uniform(0, 1)
        while idx < len(scaled_fitness_list):
            cumulative_sum += scaled_fitness_list[idx]
            if cumulative_sum > random_val:
                return chromosome_population[idx]
        return chromosome_population[-1]
    #             offsprings_list.append(chromosome_population[idx])
    #             break
    #             # TU POWINIEN BYĆ BREAK
    #         idx += 1
    #     offsprings_list.append(chromosome_population[-1])
    #
    # return offsprings_list


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
