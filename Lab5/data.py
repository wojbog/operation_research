def load_data_from_example():
    matrix = [
        [7, 5, 5, 0],
        [3, 10, 10, 'M'],
        [3, 10, 10, 0],
        ['M', 'M', 0, 0]
    ]
    source_limits = [30, 20, 80, 80]
    destination_limits = [40, 40, 20, 110]

    return matrix, source_limits, destination_limits