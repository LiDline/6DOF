from numpy import zeros


from func.matrix_1_4 import matrix_1_4


global_coordinate_system_upper_plate = zeros((4, 4, 4))
local_coordinate_system_lower_point = zeros((6, 4, 4, 1))
local_coordinate_system_upper_point = zeros((6, 4, 4, 1))

# Нахождение координат для отрисовки СК
def coordinate_system_lower_and_upper(matrix_move_lower_plate, matrix_move_upper_plate, matrix_move_upper_CS, global_coordinate_system):
    for j in range(6):
        for i in range(len(global_coordinate_system)):
            # СК центра верхней плиты
            global_coordinate_system_upper_plate[i] = (matrix_move_upper_CS.dot(matrix_1_4(global_coordinate_system[i][0],
                                                                                           global_coordinate_system[i][1], global_coordinate_system[i][2])))
            # Локальные СК нижней плиты
            local_coordinate_system_lower_point[j][i] = matrix_move_lower_plate[j].dot(matrix_1_4(global_coordinate_system[i][0],
                                                                                                  global_coordinate_system[i][1], global_coordinate_system[i][2]))
            local_coordinate_system_upper_point[j][i] = matrix_move_upper_plate[j].dot(matrix_1_4(global_coordinate_system[i][0],
                                                                                                  global_coordinate_system[i][1], global_coordinate_system[i][2]))

    return global_coordinate_system_upper_plate, local_coordinate_system_lower_point, local_coordinate_system_upper_point
