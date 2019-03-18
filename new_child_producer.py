import numpy as np


class NewChildProducer:
    @staticmethod
    def one_point_crossover(parent_one, parent_two, crossover_index):
        offsprings = dict()
        offsprings['child_one'] = np.concatenate((parent_one[:crossover_index], parent_two[crossover_index:]))
        offsprings['child_two'] = np.concatenate((parent_two[:crossover_index], parent_one[crossover_index:]))
        return offsprings
