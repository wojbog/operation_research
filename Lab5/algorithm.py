# transportation simplex algorithm
from data import load_data_from_example

def find_basic_base(matrix, source_limits, destination_limits):
    basic_base = []
    s_limits = source_limits.copy()
    d_limits = destination_limits.copy()
    row_index = 0
    col_index = 0
    while row_index < len(matrix) and col_index < len(matrix[0]):
      mini = min(s_limits[row_index], d_limits[col_index])
         
      basic_base.append(((row_index, col_index),mini))

      s_limits[row_index] -= mini
      d_limits[col_index] -= mini

      if s_limits[row_index] == 0:
          row_index += 1
      if d_limits[col_index] == 0:
          col_index += 1
      


    return basic_base

def calculate_cost(matrix, basic_base):
    cost = 0
    for (i,j),value in basic_base:
        if matrix[i][j] != 'M':
            return 'M'
        cost += matrix[i][j] * value
    return cost

def optimality_test(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 'M' and matrix[i][j] < 0:
                return False
    return True

def get_the_smallest(matrix):
    smallest = matrix[0][0]
    index = (0,0)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 'M' and matrix[i][j] < smallest:
                smallest = matrix[i][j]
                index = (i,j)
    return smallest, index


def generate_U_V(matrix, basic_base):
    u_source = [None  for i in range(len(matrix))]
    v_destination = [None for i in range(len(matrix[0]))]
    u_source[0] = 0
    queue = basic_base
    while len(queue)!=0:
      element = queue.pop(0)
      i,j = element[0]
      if u_source[i] is not None:
          v_destination[j] = matrix[i][j] - u_source[i]
      elif v_destination[j] is not None:
          u_source[i] = matrix[i][j] - v_destination[j]
      else:
          queue.append(element)
    
    return u_source, v_destination

def fill_in_matrix(matrix, basic_base, u_source, v_destination):
    m_matrix = []
    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix[0])):
            if (i,j) in basic_base:
                temp.append(0)
            else:
                if matrix[i][j] == 'M':
                  temp.append('M')
                else:
                  temp.append(matrix[i][j] - u_source[i] - v_destination[j])
        m_matrix.append(temp)
    
    return m_matrix


matrix, s_limits, d_limits = load_data_from_example() 

base = find_basic_base(matrix, s_limits, d_limits)
# print(calculate_cost(matrix, base))

u_source, v_destination =generate_U_V(matrix, base)

print(fill_in_matrix(matrix, base, u_source, v_destination))