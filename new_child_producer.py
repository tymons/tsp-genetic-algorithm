import numpy as np
import random


class NewChildProducer:
    @staticmethod
    def one_point_crossover(parent_one, parent_two, crossover_index):
        """
        Function witch use PMX crossover for TSP
        :param parent_one:
        :param parent_two:
        :param crossover_index:
        :return:
        """
        offsprings = dict()
        crossover_point = random.randint(2, len(parent_one))
        parent_one_temp = np.array(parent_one)
        parent_two_temp = np.array(parent_two)

        # We start from index no 1 because city with no 0 should be always at the beginning
        offspring_one = [parent_one[0]]
        for idx in range(1, crossover_point - 1):
            value = parent_two[idx]
            parent_one_temp[np.where(parent_one_temp == value)], parent_one_temp[idx] \
                = parent_one_temp[idx], parent_one_temp[np.where(parent_one_temp == value)]
            offspring_one.append(parent_one_temp[idx])
        offspring_one = np.concatenate((offspring_one, parent_one_temp[(crossover_point - 1):]))

        offspring_two = [parent_two[0]]
        for idx in range(1, crossover_point - 1):
            value = parent_one[idx]
            parent_two_temp[np.where(parent_two_temp == value)], parent_two_temp[idx] \
                = parent_two_temp[idx], parent_two_temp[np.where(parent_two_temp == value)]
            offspring_two.append(parent_two_temp[idx])
        offspring_two = np.concatenate((offspring_two, parent_two_temp[(crossover_point - 1):]))

        offsprings['child_one'] = offspring_one
        offsprings['child_two'] = offspring_two
        return offsprings

    @staticmethod
    def mutate_reverse(chromosome, start_index, length):
        if start_index <= 0:
            start_index = 1

        sub_chromosome = list(reversed(chromosome[start_index:(start_index + length)]))
        chromosome[start_index:(start_index + length)] = sub_chromosome
        return chromosome
