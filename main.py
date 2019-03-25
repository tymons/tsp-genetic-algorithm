import numpy as np
import time
import matplotlib.pyplot as plt
from roulette_wheel import RouletteWheel
from new_child_producer import NewChildProducer


def get_cities_from_map(no_cities):
    plt.title("Set location of " + str(no_cities) + " cities", fontsize=12)
    plt.axis([0, 20, 0, 20])
    plt.grid(color='b', linestyle='--', linewidth=0.5)
    x = plt.ginput(no_cities)
    plt.close()
    return x


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


def get_distances_matrix(coordinates_tuple_list):
    """
    Function that prepares random distance matrix based on the max cities
    :param coordinates_tuple_list:
    :return:
    """
    shape = (len(coordinates_tuple_list), len(coordinates_tuple_list))
    a = np.zeros(shape)

    for row_idx, tuple_one in enumerate(coordinates_tuple_list):
        for col_idx, tuple_two in enumerate(coordinates_tuple_list[row_idx:], start=row_idx):
            # Euclidean distance
            distance = np.sqrt(np.power(tuple_two[0] - tuple_one[0], 2) + np.power(tuple_two[1] - tuple_one[1], 2))
            a[row_idx][col_idx] = distance
            a[col_idx][row_idx] = distance

    return a


def draw_path(winner, coordinates_table):
    plt.ion()
    plt.clf()
    plt.axis([0, 20, 0, 20])
    plt.grid(color='b', linestyle='--', linewidth=0.5)
    coordinates = []
    for city_no in winner:
        coordinates.append(coordinates_table[city_no])

    plt.plot([x[0] for x in coordinates], [x[1] for x in coordinates], '-o')
    plt.pause(0.05)
    plt.show()


def main():
    max_cites = 10
    pop_size = 100
    no_chromosomes_out = 6
    population = []
    max_epochs = 50
    epoch_num = 0

    # Interactive map for choosing city location
    coordinates = get_cities_from_map(max_cites)
    # Calculate matrix of distances
    distances_matrix = get_distances_matrix(coordinates)

    # Population initialization
    for idx in range(pop_size):
        permutation_list = np.random.permutation(range(1, max_cites))
        # City with 0 number should be always at the start
        permutation_list = np.insert(permutation_list, 0, 0)
        population.append(permutation_list)

    while epoch_num < max_epochs:
        # calculate distances with distances matrix
        fitness_score = calculate_fitness(population, distances_matrix)
        print("Minimum fitness score is : " +
              str(fitness_score[np.argmin(fitness_score)]))
        # winner = population[np.argmin(fitness_score)]
        # draw_path(winner, coordinates)

        rw = RouletteWheel(population, fitness_score)
        for i in range(no_chromosomes_out//2):
            offsprings = NewChildProducer.one_point_crossover(rw.wheel(), rw.wheel(), 4)
            mutated_child_one = NewChildProducer.mutate_reverse(offsprings['child_one'], 3, 2)
            mutated_child_two = NewChildProducer.mutate_reverse(offsprings['child_two'], 3, 2)
            # Add better child on their position
            population.append(mutated_child_one)
            population.append(mutated_child_two)

        # Get rid of the worst ones
        for j in range(no_chromosomes_out // 2):
            del population[fitness_score.argmax()]
            del population[fitness_score.argmax()]

        epoch_num = epoch_num + 1

    print("GA has ended after " + str(epoch_num) + " epochs!")


if __name__ == "__main__":
    main()
