from numpy import array, zeros


from func.matrix_1_4 import matrix_1_4
from func.transition_matrix import transition_matrix


global_coordinate_system_upper_plate = zeros((4, 4, 4))
local_coordinate_system_lower_point = zeros((6, 4, 4, 1))
matrix_move_crosspoints_cs = zeros((6, 4, 4))
local_coordinate_system_crosspoints = zeros((6, 4, 4, 1))

# Нахождение координат для отрисовки СК
def coordinate_system(matrix_move_lower_plate, matrix_move_upper_CS, local_cross_coordinates, global_coordinate_system):
    for j in range(6):
        for i in range(len(global_coordinate_system)):
            # СК центра верхней плиты
            global_coordinate_system_upper_plate[i] = (matrix_move_upper_CS.dot(matrix_1_4(global_coordinate_system[i][0],
                                                                                           global_coordinate_system[i][1], global_coordinate_system[i][2])))
            # Локальные СК нижней плиты
            local_coordinate_system_lower_point[j][i] = matrix_move_lower_plate[j].dot(matrix_1_4(global_coordinate_system[i][0],
                                                                                               global_coordinate_system[i][1], global_coordinate_system[i][2]))   
            # Матрица перемещения для СК точек пересечения
            matrix_move_crosspoints_cs[j] = matrix_move_lower_plate[j].dot(transition_matrix(
                local_cross_coordinates[j][0][0], local_cross_coordinates[j][1][0], local_cross_coordinates[j][2][0]))
            # Локальные СК точек пересечения
            local_coordinate_system_crosspoints[j][i] = matrix_move_crosspoints_cs[j].dot(matrix_1_4(global_coordinate_system[i][0],
                                                                                                  global_coordinate_system[i][1], global_coordinate_system[i][2]))
            
    return global_coordinate_system_upper_plate, local_coordinate_system_lower_point, local_coordinate_system_crosspoints
