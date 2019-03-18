import numpy as np
from roulette_wheel import RouletteWheel
from new_child_producer import NewChildProducer


def calculate_fitness(chromosomes, distances_matrix):
    """
    Function that calculates fitness for every chromosome based on distance matrix
    :param chromosomes:         array of vectors with chromosomes
    :param distances_matrix:    matrix of distances between different cities
    :return:                    vector with length of len(chromosomes) and calculates fitness functions
    """
    fitness_score = np.zeros(len(chromosomes))
    for i in range(len(chromosomes)):
        for j in range(len(chromosomes[i])):
            if j + 1 < len(chromosomes[i]):
                value = distances_matrix[chromosomes[i][j]][chromosomes[i][j + 1]]
            else:
                value = distances_matrix[chromosomes[i][j]][chromosomes[i][0]]
            fitness_score[i] += value

    return fitness_score


def get_distances_matrix(size_of_matrix):
    """
    Function that prepares random distance matrix based on the max cities
    :param size_of_matrix:      max number of cities
    :return:                    size_of_matrix X size_of_matrix matrix with distances
    """
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
    fitness_score = calculate_fitness(population, distances_matrix)

    rw = RouletteWheel(population, fitness_score)
    new_population = []
    for i in range(len(population)):
        offsprings = NewChildProducer.one_point_crossover(rw.wheel(), rw.wheel(), 7)
        mutated_child_one = NewChildProducer.mutate(offsprings['child_one'])
        mutated_child_two = NewChildProducer.mutate(offsprings['child_one'])
        new_population.append(mutated_child_one)
        new_population.append(mutated_child_two)

    # Show distribution o population
    # plt.figure()
    # plt.hist(population, color='blue', bins=200)
    # plt.show()


if __name__ == "__main__":
    main()
