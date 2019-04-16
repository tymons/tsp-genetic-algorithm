import numpy as np
import matplotlib.pyplot as plt
import picker as cp
import random
from city import City
from chromosome import Chromosome
from evolution import one_point_pmx_crossover, mutate_switch_cities


def get_cities_from_map(no_cities):
    """
    Function for obtaining points from 2D map. User picks no_cities points.
    :param no_cities:   integer, how many point should be obtained
    :return: list of cities
    """
    plt.title("Set location of " + str(no_cities) + " cities", fontsize=12)
    plt.axis([0, 20, 0, 20])
    plt.grid(color='b', linestyle='--', linewidth=0.5)
    list_of_coordinates = plt.ginput(no_cities)
    cities_list = list(map(lambda coordinate: City(coordinate[0], coordinate[1]), list_of_coordinates))
    plt.close()
    return cities_list


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


def draw_path(winner_chromosome):
    """
    Function for drawing path with use of matplotlib
    :param winner_chromosome:              Chromosome object for which path should ne drawn
    """
    plt.ion()
    plt.clf()
    plt.axis([0, 20, 0, 20])
    plt.grid(color='b', linestyle='--', linewidth=0.5)
    coordinates = []
    for city in winner_chromosome.get_cities_list():
        coordinates.append((city.x, city.y))

    first_city = winner_chromosome.get_cities_list()[0]
    coordinates.append((first_city.x, first_city.y))
    plt.plot([x[0] for x in coordinates], [x[1] for x in coordinates], '-o')
    plt.plot(coordinates[0][0], coordinates[0][1], alpha=0.8, c="g", marker=r'$\clubsuit$',
             label="Start position", markersize=22)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()
    plt.pause(0.0001)


def main():
    max_cites = 25
    pop_size = 100
    no_chromosomes_out = 50
    population = []
    max_epochs = 2500
    epoch_num = 0

    # Interactive map for choosing city location
    cities = get_cities_from_map(max_cites)

    # Population initialization
    for idx in range(pop_size):
        # City with 0 number should be always at the start
        cities_permutation = np.append([cities[0]], np.random.permutation(cities[1:]))
        population.append(Chromosome(cities_permutation))

    current_winner = population[0]
    while epoch_num < max_epochs:

        # calculate distances with distances matrix
        fitness_list = list(map(lambda chromosome: chromosome.get_fitness(), population))
        fitness_min = min(fitness_list)
        print("Minimum fitness score at epoch " + str(epoch_num) + " is : " +
              str(fitness_min) + " with pop size: " + str(len(population)))
        if current_winner != population[fitness_list.index(fitness_min)]:
            current_winner = population[fitness_list.index(fitness_min)]
            draw_path(current_winner)

        for i in range(no_chromosomes_out // 2):
            offspring_list = cp.roulette_wheel_with_two_offsprings(population)
            offspring_one, offspring_two = one_point_pmx_crossover(
                offspring_list[0],
                offspring_list[1])
            mutated_child_one = mutate_switch_cities(offspring_one,
                                                     random.randrange(1, len(offspring_one)),
                                                     random.randrange(1, len(offspring_one)))
            mutated_child_two = mutate_switch_cities(offspring_two,
                                                     random.randrange(1, len(offspring_one)),
                                                     random.randrange(1, len(offspring_one)))
            # Add better child on their position
            population.append(Chromosome(mutated_child_one))
            population.append(Chromosome(mutated_child_two))

        fitness_list = list(map(lambda chromosome: chromosome.get_fitness(), population))

        # Get rid of the worst
        for j in range(no_chromosomes_out // 2):
            max_elem = max(fitness_list)
            idx_to_delete = fitness_list.index(max_elem)
            del population[idx_to_delete]
            del fitness_list[idx_to_delete]

            max_elem = max(fitness_list)
            idx_to_delete = fitness_list.index(max_elem)
            del population[idx_to_delete]
            del fitness_list[idx_to_delete]

        epoch_num = epoch_num + 1

    # Draw winner
    final_fitness_list = list(map(lambda chromosome: chromosome.get_fitness(), population))
    min_fitness = min(final_fitness_list)
    winner = population[final_fitness_list.index(min_fitness)]
    draw_path(winner)
    print("Click the image to exit")
    plt.waitforbuttonpress()


if __name__ == "__main__":
    main()
