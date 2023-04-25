from numpy import array, cos, sin, zeros, hstack, vstack


# Реализация матрицы поворота по последовательности XYZ
def rotation_matrix(alpha, beta, gamma):
    
    Rx_matrix = array([[1, 0,  0],
                       [0, cos(alpha), -sin(alpha)],
                       [0, sin(alpha), cos(alpha)]])

    # Матрица поворота относительно ОY
    Ry_matrix = array([[cos(beta), 0,  sin(beta)],
                       [0, 1, 0],
                       [-sin(beta), 0, cos(beta)]])


    # Матрица поворота относительно ОZ
    Rz_matrix = array([[cos(gamma), -sin(gamma), 0],
                   [sin(gamma),  cos(gamma), 0],
                   [0, 0, 1]])

    rotation_matrix = Rx_matrix.dot(Ry_matrix.dot(Rz_matrix))  # 1. x  2. y  3. z

    # Создаю матрицу 4 на 4
    rotation_matrix = hstack([rotation_matrix, zeros((3, 1))])
    rotation_matrix = vstack([rotation_matrix, zeros((1, 4))])
    rotation_matrix[3][3] = 1

    return rotation_matrix