from numpy import radians, array, zeros, linalg


import constants
from func.rotation_matrix import rotation_matrix
from func.transition_matrix import transition_matrix
from func.coordinate_system_lower_and_upper import coordinate_system_lower_and_upper
from func.matrix_1_4 import matrix_1_4
from func.cross_normal_to_oz import cross_normal_to_oz


local_lower_CS = constants.LOCAL_LOWER_CS
local_upper_CS = constants.LOCAL_UPPER_CS

# Координаты точек в глобальной СК 
offset_lower = constants.OFFSET_LOWER
offset_upper = constants.OFFSET_UPPER
rotate_local_cs = constants.ROTATE_LOCAL_CS
global_coordinate_system = constants.GLOBAL_COORDINATE_SYSTEM
R = constants.R_CIRCLE
r = constants.R_SPHERE

matrix_rotate_local_cs = rotation_matrix(radians(rotate_local_cs[3]), 
                                         radians(rotate_local_cs[4]), 
                                         radians(rotate_local_cs[5]))



# Матрица переноса нижней плиты
matrix_move_lower_plate = zeros((6,4,4))
# Точки нижней плиты
lower_points = zeros((6,4,1))
# Матрица переноса верхней плиты
matrix_move_upper_plate = zeros((9,4,4))
# Точки верхней плиты
upper_points = zeros((9,4,1))
# Координаты верхний точек относительно нижних
position_upper_points_from_lower = zeros((6, 4, 1))
# Координаты точек пересечения в локальных координатах
local_cross_coordinates = zeros((6, 4, 1))
# Углы рычагов
arm_angle = zeros(6)
# Координаты точек пересечения в глобальных координатах
global_cross_coordinates = zeros((6, 4, 1))

def main_for_4(x, y, z, ax, ay, az):
    move_upper_CS = array((x, y, z, ax, ay, az)) 
    
    # Сначала поворачиваем, затем смещаем верхнюю центральную точку
    matrix_move_upper_CS = transition_matrix(move_upper_CS[0], 
                                         move_upper_CS[1],
                                         move_upper_CS[2]).dot(
                            rotation_matrix(radians(move_upper_CS[3]), 
                                            radians(move_upper_CS[4]), 
                                            radians(move_upper_CS[5])))
    
    for i in range(6):
        # Запишем матрицы перемещений для каждого центра тяги в один массив
        matrix_move_lower_plate[i] = (transition_matrix(offset_lower[i][0], 
                                                            offset_lower[i][1], 
                                                            offset_lower[i][2]).dot(
                                        rotation_matrix(radians(offset_lower[i][3]), 
                                                        radians(offset_lower[i][4]), 
                                                        radians(offset_lower[i][5])))).dot(
                                        matrix_rotate_local_cs) 
        # Координаты нижней плиты находим через перемножение матрицы перемещения на локальную СК
        lower_points[i] = matrix_move_lower_plate[i].dot(local_lower_CS)     
        # Матрица переноса для точек верхней плиты 
        matrix_move_upper_plate[i] = matrix_move_upper_CS.dot(
                (transition_matrix(offset_upper[i][0], 
                                   offset_upper[i][1], 
                                   offset_upper[i][2]).dot(
                                        rotation_matrix(radians(offset_upper[i][3]), 
                                                        radians(offset_upper[i][4]), 
                                                        radians(offset_upper[i][5])))).dot(
                                        matrix_rotate_local_cs))  
        # Перемещение и поворот точек верхней плиты
        upper_points[i] = matrix_move_upper_plate[i].dot(local_upper_CS)        
        position_upper_points_from_lower[i] = linalg.inv(
                    matrix_move_lower_plate[i]).dot(upper_points[i])
        cross_matrix = cross_normal_to_oz(
                    position_upper_points_from_lower[i], R, r)

        local_cross_coordinates[i] = matrix_1_4(
                    cross_matrix[0], cross_matrix[1], cross_matrix[2])
        arm_angle[i] = cross_matrix[3]
        global_cross_coordinates[i] = matrix_move_lower_plate[i].dot(
                    local_cross_coordinates[i])

    global_coordinate_system_upper_plate, local_coordinate_system_lower_point, local_coordinate_system_upper_point = coordinate_system_lower_and_upper(matrix_move_lower_plate, matrix_move_upper_plate, matrix_move_upper_CS, global_coordinate_system)                  
    
    return lower_points, upper_points, move_upper_CS, global_coordinate_system_upper_plate, local_coordinate_system_lower_point, local_coordinate_system_upper_point, arm_angle, global_cross_coordinates, matrix_move_lower_plate, local_cross_coordinates, matrix_move_upper_plate