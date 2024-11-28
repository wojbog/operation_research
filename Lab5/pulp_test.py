from pulp import * 
from data import generate_random_limits, genereate_random_matrix, load_data_from_example
def test_with_pulp(s, d, cost):
    import numpy as np
    n_supply = len(s)
    n_demand = len(d)

    model = LpProblem(name="Transportation_Problem", sense=LpMinimize)
    x = [[LpVariable(f"x_{i}_{j}", lowBound=0, cat="Continuous") for j in range(n_demand)] for i in range(n_supply)]
    model += lpSum(cost[i][j] * x[i][j] for i in range(n_supply) for j in range(n_demand) if cost[i][j] != 'M')

    for i in range(n_supply):
        model += lpSum(x[i][j] for j in range(n_demand) if cost[i][j] != 'M') == s[i], f"Supply_Constraint_{i}"

    for j in range(n_demand):
        model += lpSum(x[i][j] for i in range(n_supply) if cost[i][j] != 'M') == d[j], f"Demand_Constraint_{j}"

    model.solve(pulp.PULP_CBC_CMD(msg=False))
    # print("Pulp optimal value: ", model.objective.value())
    return model.objective.value()
