import numpy as np
import matplotlib.pyplot as plt
import chromosome_picker as cp
from new_child_producer import NewChildProducer


def get_cities_from_map(no_cities):
    plt.title("Set location of " + str(no_cities) + " cities", fontsize=12)
    plt.axis([0, 20, 0, 20])
    plt.grid(color='b', linestyle='--', linewidth=0.5)
    x = plt.ginput(no_cities)
    plt.close()
    return x


def calculate_fitness(chromosomes_list, distances_matrix):
    """
    Function that calculates fitness for every chromosome based on distance matrix
    :param chromosomes_list:         array of vectors with chromosomes
    :param distances_matrix:    matrix of distances between different cities
    :return:                    List of tuples where first element is chromosome and second fitness score
    """
    population_fitness = []
    for i in range(len(chromosomes_list)):
        acc = 0
        for j in range(len(chromosomes_list[i])):
            if j + 1 < len(chromosomes_list[i]):
                value = distances_matrix[chromosomes_list[i][j]][chromosomes_list[i][j + 1]]
            else:
                value = distances_matrix[chromosomes_list[i][j]][chromosomes_list[i][0]]
            acc += value
        population_fitness.append(acc)

    return population_fitness


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

    coordinates.append(coordinates_table[0])
    plt.plot([x[0] for x in coordinates], [x[1] for x in coordinates], '-o')
    plt.plot(coordinates[0][0], coordinates[0][1], alpha=0.8, c="g", marker=r'$\clubsuit$',
             label="Start position", markersize=22)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


def main():
    max_cites = 15
    pop_size = 100
    no_chromosomes_out = 80
    population = []
    max_epochs = 1500
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

    fitness = calculate_fitness(population, distances_matrix)

    while epoch_num < max_epochs:
        # calculate distances with distances matrix
        print("Minimum fitness score at epoch " + str(epoch_num) + " is : " +
              str(min(fitness)) + " with pop size: " + str(len(population)))

        for i in range(no_chromosomes_out // 2):
            offspring_one, offspring_two = NewChildProducer.one_point_crossover(
                cp.tournament(population, fitness, 20),
                cp.tournament(population, fitness, 20))
            mutated_child_one = NewChildProducer.mutate_reverse(offspring_one, 4, 2)
            mutated_child_two = NewChildProducer.mutate_reverse(offspring_two, 4, 2)
            # Add better child on their position
            population.append(mutated_child_one)
            fitness.append(calculate_fitness([mutated_child_one], distances_matrix))
            population.append(mutated_child_two)
            fitness.append(calculate_fitness([mutated_child_one], distances_matrix))

        # Get rid of the worst
        for j in range(no_chromosomes_out // 2):
            del population[(fitness.index(max(fitness)))]
            del fitness[fitness.index(max(fitness))]
            del population[fitness.index(max(fitness))]
            del fitness[fitness.index(max(fitness))]

        epoch_num = epoch_num + 1

    print("GA has ended after " + str(epoch_num) + " epochs!")
    # Draw winner
    winner = population[fitness.index(min(fitness))]
    draw_path(winner, coordinates)
    print("Click the image to exit")
    plt.waitforbuttonpress()


if __name__ == "__main__":
    main()
