from numpy import zeros, linalg, sqrt, array, nan
from math import atan2
from func.matrix_1_4 import matrix_1_4


from func.rotation_matrix import rotation_matrix
import constants


moving_gas_spring = constants.MOVING_GAS_SPRING
global_coordinate_system = constants.GLOBAL_COORDINATE_SYSTEM


# Расчёт нижнего шарнира пружины
coordinates_upper_joint_of_gas_spring_from_lower = zeros((3, 4, 1))
angles_between_spring_and_ZY_of_lower_joint = zeros(3)
matrix_rotate_cs_lower_joint_of_gas_spring = zeros((3, 4, 4))
matrix_move_to_new_cs_of_lower_joint_of_gas_spring = zeros((3, 4, 4))
coordinates_upper_joint_gas_spring_from_lower_in_new_planes = zeros((3, 4, 1))
# Расчёт верхнего шарнира пружины
coordinates_lower_joint_of_gas_spring_from_upper = zeros((3, 4, 1))
angles_between_spring_and_ZY_of_upper_joint = zeros(3)
matrix_rotate_cs_upper_joint_of_gas_spring = zeros((3, 4, 4))
matrix_move_to_new_cs_of_upper_joint_of_gas_spring = zeros((3, 4, 4))
coordinates_lower_joint_gas_spring_from_upper_in_new_planes = zeros((3, 4, 1))
len_spring = zeros(3)

# Для локальных СК
local_coordinate_system_cs_lower_joint_of_gas_spring = zeros((3, 4, 4, 1))
local_coordinate_system_cs_upper_joint_of_gas_spring = zeros((3, 4, 4, 1))


# Нахождение углов шаровых наконечников для пружин
def spring_ball_corners(upper_points, lower_points, matrix_move_lower_plate, matrix_move_upper_plate, angle_lower_joint, angle_upper_joint):
    """5. Поиск углов шаровых наконечников пружин"""

    for i in range(3):
        # Находим координаты верхней шаровой относительно нижней
        coordinates_upper_joint_of_gas_spring_from_lower[i] = linalg.inv(
            matrix_move_lower_plate[i+6]).dot(upper_points[i+6])
        coordinates_lower_joint_of_gas_spring_from_upper[i] = linalg.inv(
            matrix_move_upper_plate[i+6]).dot(lower_points[i+6])

        # Найдём угол между проекцией пружины (на YX) и ZY, чтобы повернуть XY на полученный угол по OZ (пружина няходится в 1-ей четверти)
        angles_between_spring_and_ZY_of_lower_joint[i] = atan2(
            coordinates_upper_joint_of_gas_spring_from_lower[i][0][0], coordinates_upper_joint_of_gas_spring_from_lower[i][1][0])
        # (пружина няходится в 3-ей четверти)
        angles_between_spring_and_ZY_of_upper_joint[i] = atan2(
            coordinates_lower_joint_of_gas_spring_from_upper[i][0][0], coordinates_lower_joint_of_gas_spring_from_upper[i][1][0])

        # Матрицы поворота СК (чтобы пружина лежала в плоскости ZY)
        matrix_rotate_cs_lower_joint_of_gas_spring[i] = rotation_matrix(
            0, 0, -angles_between_spring_and_ZY_of_lower_joint[i])
        # Матрицы поворота СК (чтобы пружина лежала в плоскости ZX)
        matrix_rotate_cs_upper_joint_of_gas_spring[i] = rotation_matrix(
            0, 0, -angles_between_spring_and_ZY_of_upper_joint[i])

        # Создадим общую матрицу перемещения с последующим поворотом
        matrix_move_to_new_cs_of_lower_joint_of_gas_spring[i] = matrix_move_lower_plate[i+6].dot(
            matrix_rotate_cs_lower_joint_of_gas_spring[i])
        # Создадим общую матрицу перемещения с последующим поворотом
        matrix_move_to_new_cs_of_upper_joint_of_gas_spring[i] = matrix_move_upper_plate[i+6].dot(
            matrix_rotate_cs_upper_joint_of_gas_spring[i])

        # Узнаем координаты верхнего шарнира точки пересечения в новой СК
        coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i] = linalg.inv(
            matrix_move_to_new_cs_of_lower_joint_of_gas_spring[i]).dot(upper_points[i+6])
        # Узнаем координаты нижнего шарнира точки пересечения в новой СК
        coordinates_lower_joint_gas_spring_from_upper_in_new_planes[i] = linalg.inv(
            matrix_move_to_new_cs_of_upper_joint_of_gas_spring[i]).dot(lower_points[i+6])

        # Найдём углы шаровой
        angle_lower_joint[i+6] = atan2(coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i]
                                       [2][0], coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i][1][0])
        angle_upper_joint[i+6] = atan2(coordinates_lower_joint_gas_spring_from_upper_in_new_planes[i]
                                       [2][0], coordinates_lower_joint_gas_spring_from_upper_in_new_planes[i][1][0])

        len_spring[i] = sqrt(coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i][0][0]**2 + coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i][1][0]**2 +
                             coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i][2][0]**2)

        # Если длина пружины <> её max/min - отметаем решение
        if len_spring[i] >= moving_gas_spring[1]:
            print('Длина пружины больше допустимой max')
            return array((nan, nan, nan, nan, nan, nan, nan, nan, nan)), array((nan, nan, nan, nan, nan, nan, nan, nan, nan))
        elif len_spring[i] <= moving_gas_spring[0]:
            print('Длина пружины меньше допустимой min')
            return array((nan, nan, nan, nan, nan, nan, nan, nan, nan)), array((nan, nan, nan, nan, nan, nan, nan, nan, nan))
    
        # Локальные СК шаровых
        for j in range(len(global_coordinate_system)):
            local_coordinate_system_cs_lower_joint_of_gas_spring[i][j] = matrix_move_to_new_cs_of_lower_joint_of_gas_spring[i].dot(matrix_1_4(global_coordinate_system[j][0],
                                                                                                                                                 global_coordinate_system[j][1], global_coordinate_system[j][2]))
            local_coordinate_system_cs_upper_joint_of_gas_spring[i][j] = matrix_move_to_new_cs_of_upper_joint_of_gas_spring[i].dot(matrix_1_4(global_coordinate_system[j][0],
                                                                                                                                           global_coordinate_system[j][1], global_coordinate_system[j][2]))
            
    return angle_lower_joint, angle_upper_joint, local_coordinate_system_cs_lower_joint_of_gas_spring, local_coordinate_system_cs_upper_joint_of_gas_spring
