from numpy import radians, zeros


from func.transition_matrix import transition_matrix
from func.rotation_matrix import rotation_matrix
import constants


offset_lower = constants.OFFSET_LOWER
rotate_local_cs = constants.ROTATE_LOCAL_CS
local_lower_CS = constants.LOCAL_LOWER_CS
offset_upper = constants.OFFSET_UPPER
local_upper_CS = constants.LOCAL_UPPER_CS


# Матрица переноса нижней плиты
matrix_move_lower_plate = zeros((9,4,4))
# Точки нижней плиты
lower_points = zeros((9,4,1))
# Матрица переноса верхней плиты
matrix_move_upper_plate = zeros((9,4,4))
# Точки верхней плиты
upper_points = zeros((9,4,1))


# Создание матриц с координатами точек верхней и нижней плиты
def plate_coordinates(move_upper_CS):

    """"3. Координаты плит"""

    matrix_rotate_local_cs = rotation_matrix(radians(rotate_local_cs[3]), radians(rotate_local_cs[4]), radians(rotate_local_cs[5])) 

    # Сначала поворачиваем, затем смещаем верхнюю центральную точку
    matrix_move_upper_CS = transition_matrix(move_upper_CS[0], move_upper_CS[1], move_upper_CS[2]).dot(
                            # Умножаю матрицу смещения верхней точки на матрицу смещения точек плиты
                            rotation_matrix(radians(move_upper_CS[3]), radians(move_upper_CS[4]), radians(move_upper_CS[5])))

    # Вычисляем матрицы переноса и находим точки
    for i in range(9):
        # Запишем матрицы перемещений для каждого центра тяги в один массив
        matrix_move_lower_plate[i] = (transition_matrix(offset_lower[i][0], offset_lower[i][1], offset_lower[i][2]).dot(
                                    rotation_matrix(radians(offset_lower[i][3]), radians(offset_lower[i][4]), radians(offset_lower[i][5])))).dot(
                                    matrix_rotate_local_cs)
        # Координаты нижней плиты находим через перемножение матрицы перемещения на локальную СК
        lower_points[i] = matrix_move_lower_plate[i].dot(local_lower_CS)
        
        # Матрица переноса для точек верхней плиты 
        matrix_move_upper_plate[i] = matrix_move_upper_CS.dot((transition_matrix(offset_upper[i][0], offset_upper[i][1], offset_upper[i][2]).dot(
                                    rotation_matrix(radians(offset_upper[i][3]), radians(offset_upper[i][4]), radians(offset_upper[i][5])))).dot(
                                    matrix_rotate_local_cs))    
        upper_points[i] = matrix_move_upper_plate[i].dot(local_upper_CS) # Перемещение и поворот верхней плиты

    return matrix_move_lower_plate, matrix_move_upper_plate, lower_points, upper_points