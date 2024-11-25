# def load_data_from_example():
#     matrix = [
#         [7, 5, 5, 0],
#         [3, 10, 10, 'M'],
#         [3, 10, 10, 0],
#         ['M', 'M', 0, 0]
#     ]
#     source_limits = [30, 20, 80, 80]
#     destination_limits = [40, 40, 20, 110]

#     return matrix, source_limits, destination_limits

def load_data_from_example():
    matrix = [[5, 6, 4, 8, 2], [3, 6, 3, 8, 0], [2, 6, 3, 3, 5], [6, 0, 2, 4, 4], [8, 2, 7, 4, 8]]
    source_limits = [34, 2, 57, 6, 0]
    destination_limits = [59, 2, 24, 3, 11]

    return matrix, source_limits, destination_limits

def genereate_random_matrix(n):
    import random
    matrix = []
    for i in range(n):
        temp = []
        for j in range(n):
            temp.append(random.randint(0, 10))
        matrix.append(temp)

    return matrix

def generate_random_limits(n):
    import numpy as np
    breakpoints_1 = np.sort(np.random.uniform(0, 1, n-1))
    breakpoints_1 = np.concatenate(([0], breakpoints_1, [1]))
   
    limits_1 = np.diff(breakpoints_1) * 100
    limits_1 = np.round(limits_1).astype(int)

    breakpoints_2 = np.sort(np.random.uniform(0, 1, n-1))
    breakpoints_2 = np.concatenate(([0], breakpoints_2, [1]))
   
    limits_2 = np.diff(breakpoints_2) * 100
    limits_2 = np.round(limits_2).astype(int)

    diff = limits_1.sum() - limits_2.sum()
    if diff > 0:
        limits_2[-1] += diff
    elif diff < 0:
        limits_1[-1] += abs(diff)


    return limits_1.tolist(), limits_2.tolist()