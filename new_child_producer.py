import numpy as np
import random


class NewChildProducer:
    @staticmethod
    def one_point_crossover(parent_one, parent_two):
        """
        Function witch use PMX crossover for TSP
        :param parent_one:
        :param parent_two:
        :return:
        """
        crossover_point = random.randint(2, len(parent_one))
        parent_one_temp = np.array(parent_one)
        parent_two_temp = np.array(parent_two)

        # We start from index no 1 because city with no 0 should be always at the beginning
        offspring_one = [parent_one[0]]  # Zero at the beginning
        for idx in range(1, crossover_point - 1):
            value = parent_two[idx]
            parent_one_temp[np.where(parent_one_temp == value)], parent_one_temp[idx] \
                = parent_one_temp[idx], parent_one_temp[np.where(parent_one_temp == value)]
            offspring_one = np.append(offspring_one, parent_one_temp[idx])
        offspring_one = np.concatenate((offspring_one, parent_one_temp[(crossover_point - 1):]))

        offspring_two = [parent_two[0]]  # Zero at the beginning
        for idx in range(1, crossover_point - 1):
            value = parent_one[idx]
            parent_two_temp[np.where(parent_two_temp == value)], parent_two_temp[idx] \
                = parent_two_temp[idx], parent_two_temp[np.where(parent_two_temp == value)]
            offspring_two = np.append(offspring_two, parent_two_temp[idx])
        offspring_two = np.concatenate((offspring_two, parent_two_temp[(crossover_point - 1):]))

        return offspring_one, offspring_two

    @staticmethod
    def mutate_reverse(chromosome, start_index, length):
        if start_index <= 0:
            start_index = 1

        sub_chromosome = list(reversed(chromosome[start_index:(start_index + length)]))
        chromosome[start_index:(start_index + length)] = sub_chromosome
        return chromosome

    @staticmethod
    def mutate_switch_cities(chromosome, index_first, index_second):
        if index_first <= 0:
            index_first = 1

        if index_second <= 0:
            index_second = 0

        chromosome[index_second], chromosome[index_first] = chromosome[index_first], chromosome[index_second]
        return chromosome
