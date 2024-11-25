# transportation simplex algorithm
from data import load_data_from_example, genereate_random_matrix, generate_random_limits

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
      else:
          col_index += 1
      


    return basic_base


def normalize_base(base, matrix):
    mm = matrix.copy()
    new_base = []
    # u = [0 for i in range(len(matrix))]
    # v = [0 for i in range(len(matrix[0]))]
    u = []
    v = []

    for i in range(len(base)):
        u.append(i)
        v.append(i)
    
    for i in range(len(u)):
        if u[i] > 1 or v[i] > 1:
            continue
        base.append(((i,j),mm[i][j]))
    
    for i in range(len(mm)):
        licznik = 0
        for j in range(len(mm[0])):
            if mm[i][j] != 'BASE':
                licznik+=1
        if licznik == 1:
            for j in range(len(mm[0])):
                if mm[i][j] != 'BASE':
                    new_base.append(((i,j),mm[i][j]))
                    break


def calculate_cost(matrix, basic_base):
    cost = 0
    for (i,j),value in basic_base:
        if matrix[i][j] == 'M':
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

def sort_base(base, index, row):
    sorted_base = []
    not_sorted = []
    for (i,j),value in base:
        if row:
            if i == index:
                sorted_base.append(((i,j),value))
            else:
                not_sorted.append(((i,j),value))
    if not row:
        for (i,j),value in base:
            if j == index:
                sorted_base.append(((i,j),value))
            else:
                not_sorted.append(((i,j),value))
    sorted_base.extend(not_sorted)
    return sorted_base

def generate_U_V(matrix, basic_base):
    u_source = [None  for i in range(len(matrix))]
    v_destination = [None for i in range(len(matrix[0]))]
    rows = [0 for i in range(len(u_source))]
    cols = [0 for i in range(len(v_destination))]
    for (i,j),value in basic_base:
        rows[i] += 1
        cols[j] += 1

    maxi_row = 0
    maxi_index_row = 0
    for i in range(len(rows)):
        if rows[i] > maxi_row:
            maxi_row = rows[i]
            maxi_index_row = i
    
    maxi_col = 0
    maxi_index_col = 0
    for i in range(len(cols)):
        if cols[i] > maxi_col:
            maxi_col = cols[i]
            maxi_index_col = i

    if maxi_row > maxi_col:
        u_source[maxi_index_row] = 0
        queue = sort_base(basic_base, maxi_index_row, True)
    else:
        v_destination[maxi_index_col] = 0
        queue = sort_base(basic_base, maxi_index_col, False)


    # u_source[0] = 0
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
            if matrix[i][j] == 'M':
                temp.append('M')
            else:
                if u_source[i] is None or v_destination[j] is None:
                    temp.append('M')
                else:
                    temp.append(matrix[i][j] - u_source[i] - v_destination[j])
        m_matrix.append(temp)
    
    for (x,y),value in basic_base:
        m_matrix[x][y] = value
    
    return m_matrix

def get_row_or_column_from_base(base, index, is_row):
    result = []
    for (i,j), value in base:
        if is_row and i == index[0] and j != index[1]:
            result.append((i,j))
        elif not is_row and j == index[1] and i != index[0]:
            result.append((i,j))
    return result

def get_path(base, start_position, index, row, stos, check):
    if index in stos:
        return False, stos
    stos.append(index)

    if index[0] == start_position[0] and index[1] != start_position[1]:
        return True, stos


    if row:
        neighbours = get_row_or_column_from_base(base, index, True)
    else:
        neighbours = get_row_or_column_from_base(base, index, False)
    
    for i,j in neighbours:
        if row:
            check, stos = get_path(base, start_position, (i,j), False, stos, check)
        else:
            check, stos = get_path(base, start_position, (i,j), True, stos, check)

        if check:
            break
    
    if not check:
        stos.pop()
    
    return check, stos
        
def change_base(base, path, m_matrix):
    new_base = []
    # for (x,y),value in base:
    #    if m_matrix[x][y] == 0:
    #           new_base.append((path[0],m_matrix[path[0][0]][path[0][1]]))
    #           continue
    #    new_base.append(((x,y),m_matrix[x][y]))

    new_base.append(((path[0][0],path[0][1]),m_matrix[path[0][0]][path[0][1]]))
    for (x,y),value in base:
       if m_matrix[x][y] == 'Z':
              m_matrix[x][y] = 0
            #   new_base.append((path[0],m_matrix[path[0][0]][path[0][1]]))
              continue
       new_base.append(((x,y),m_matrix[x][y]))

    return new_base




# matrix, s_limits, d_limits = load_data_from_example() 

# base = find_basic_base(matrix, s_limits, d_limits)
# # print(calculate_cost(matrix, base))

# u_source, v_destination =generate_U_V(matrix, base)

# print(fill_in_matrix(matrix, base, u_source, v_destination))
# get_the_smallest(fill_in_matrix(matrix, base, u_source, v_destination))


def algorithm(cost_matrix, s_limits, d_limits):
    base = find_basic_base(cost_matrix, s_limits, d_limits)

    u_source, v_destination = generate_U_V(cost_matrix, base)
   
    m_matrix = fill_in_matrix(cost_matrix, base, u_source, v_destination)
    smallest, index = get_the_smallest(m_matrix)
    licznik = 0
    average_chain = 0
    while smallest<0:
        licznik+=1
        _, stos = get_path(base, index, index, False, [], False)
        average_chain+=len(stos)
        mini_substruction=min([m_matrix[stos[i][0]][stos[i][1]] for i in range(1,len(stos),2)])
        for i in range(1,len(stos),2):
            m_matrix[stos[i][0]][stos[i][1]]-=mini_substruction
        for i in range(2,len(stos),2):
            m_matrix[stos[i][0]][stos[i][1]]+=mini_substruction
        
        m_matrix[stos[0][0]][stos[0][1]]=mini_substruction
        base = change_base(base, stos, m_matrix)
        u_source, v_destination = generate_U_V(cost_matrix, base)
        m_matrix = fill_in_matrix(cost_matrix, base, u_source, v_destination)

        smallest, index = get_the_smallest(m_matrix)


    return calculate_cost(cost_matrix, base), licznik, average_chain/licznik


if __name__ == "__main__":
    # cost_matrix, s_limits, d_limits = load_data_from_example()
    cost_matrix = genereate_random_matrix(6)
    # cost_matrix = [[10, 1, 9, 3, 1, 3], [4, 9, 4, 2, 10, 2], [2, 2, 10, 6, 0, 2], [9, 3, 10, 2, 9, 9], [5, 9, 1, 10, 4, 3], [0, 0, 2, 3, 2, 3]]
    # s_limits = [13, 1, 2, 10, 4, 71]
    # d_limits = [5, 13, 33, 15, 29, 6]
    s_limits, d_limits = generate_random_limits(6)
    base = find_basic_base(cost_matrix, s_limits, d_limits)

    u_source, v_destination = generate_U_V(cost_matrix, base)

    m_matrix = fill_in_matrix(cost_matrix, base, u_source, v_destination)

    smallest, index = get_the_smallest(m_matrix)
    licznik = 0
    while smallest<0:
        licznik+=1
        check, stos = get_path(base, index, index, False, [], False)
        mini_substruction=min([m_matrix[stos[i][0]][stos[i][1]] for i in range(1,len(stos),2)])
        for i in range(1,len(stos),2):
            m_matrix[stos[i][0]][stos[i][1]]-=mini_substruction
        for i in range(2,len(stos),2):
            m_matrix[stos[i][0]][stos[i][1]]+=mini_substruction
        
        m_matrix[stos[0][0]][stos[0][1]]=mini_substruction
        base = change_base(base, stos, m_matrix)

        u_source, v_destination = generate_U_V(cost_matrix, base)

        m_matrix = fill_in_matrix(cost_matrix, base, u_source, v_destination)

        smallest, index = get_the_smallest(m_matrix)

    print(calculate_cost(cost_matrix, base))