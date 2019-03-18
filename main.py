import numpy as np
import operator
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
from roulette_wheel import RouletteWheel

from fitness import Fitness


def create_route(city_list):
    return random.sample(city_list, len(city_list))


def initial_population(population_size, city_list):
    population = []

    for i in range(0, population_size):
        population.append(create_route(city_list))
    return population


def rank_routes(population):
    fitness_results = {}
    for i in range(0, len(population)):
        fitness_results = Fitness(population[i]).fitness_function()
    return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)


def selection(pop_ranked, elite_size):
    selection_results = []
    df = pd.DataFrame(np.array(pop_ranked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, elite_size):
        selection_results.append(pop_ranked[i][0])
    for i in range(0, len(pop_ranked) - elite_size):
        pick = 100 * random.random()
        for i in range(0, len(pop_ranked)):
            if pick <= df.iat[i, 3]:
                selection_results.append(pop_ranked[i][0])
                break
    return selection_results


def mating_pool(population, selection_results):
    matingpool = []
    for i in range(0, len(selection_results)):
        index = selection_results[i]
        matingpool.append(population[index])
    return matingpool


def get_distances_matrix(size_of_matrix):
    shape = (size_of_matrix, size_of_matrix)
    a = np.ones(shape)

    for i in range(size_of_matrix):
        for j in range(i, size_of_matrix):
            rand = np.ceil(np.random.uniform(1, 25))
            a[i][j] = rand
            a[j][i] = rand
            a[i][i] = 0

    return a


def main():
    max_cites = 10
    pop_size = 100
    population = []

    # population initialization
    for idx in range(1, pop_size):
        population.append(np.random.permutation(max_cites))

    distances_matrix = get_distances_matrix(max_cites)

    # calculate distances with distances matrix


    # Show distribution o population
    # plt.figure()
    # plt.hist(population, color='blue', bins=200)
    # plt.show()

    # rw = RouletteWheel(rand_vec)

    # for i in range(0, 10):
    #    elem.append(rw.wheel())


if __name__ == "__main__":
    main()
