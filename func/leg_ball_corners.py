from numpy import  zeros, linalg, pi
from math import atan2


from func.cross_normal_to_oz import cross_normal_to_oz
from func.matrix_1_4 import matrix_1_4
from func.transition_matrix import transition_matrix
from func.rotation_matrix import rotation_matrix


# Координаты верхний точек относительно нижних
position_upper_points_from_lower = zeros((6,4,1))
# Координаты точек пересечения в локальных координатах
local_cross_coordinates = zeros((6,4,1))
# Координаты точек пересечения в глобальных координатах
global_cross_coordinates = zeros((6,4,1))
# Углы рычагов 
arm_angle = zeros(6) 
# Матрица перемещения для СК точек пересечения
matrix_move_crosspoints = zeros((6,4,4))
 # Коорд. верхней точки относительно пересечения
coordinates_upper_points_from_crosspoints = zeros((6,4,1))   
coordinates_crosspoints_from_upper_points = zeros((6,4,1))
# Угол между проекцией тяги (на XY) и верхней точки, чтобы повернуть XY на полученный угол
angles_between_crosspoints_and_upper_points = zeros(6)
angles_between_upper_points_and_crosspoints = zeros(6)
# Матрицы поворота СК в точке пересечения до верхней точки
matrix_rotate_cs_crosspoints_to_upper_points = zeros((6,4,4))
# Матрицы поворота СК в верхней точке до точки пересечения  
matrix_rotate_cs_upper_points_to_crosspoints = zeros((6,4,4))
# Общая матрица перемещения до точки пересечения с последующим поворотом до XZ
matrix_move_to_new_cs_of_crosspoints = zeros((6,4,4))
# Создадим общую матрицу перемещения до верхней точки с последующим поворотом до YZ
matrix_move_to_new_cs_of_upper_points = zeros((6,4,4))
# Узнаем координаты верхнего шарнира точки пересечения в новой СК
coordinates_upper_points_from_crosspoints_in_new_planes = zeros((6,4,1))
# Узнаем координаты нижнего шарнира относительно верхнего в новой СК
coordinates_crosspoints_from_upper_points_in_new_planes = zeros((6,4,1))
# Углы шаровых для ног
angle_lower_joint = zeros(9)
angle_upper_joint = zeros(9)


# Нахождение углов шаровых наконечников для ног
def leg_ball_corners(matrix_move_lower_plate, upper_points, matrix_move_upper_plate, border_of_arm_angle, R, r):
    for i in range(6):

            """4.1 Точки пересечения"""

            position_upper_points_from_lower[i] = linalg.inv(matrix_move_lower_plate[i]).dot(upper_points[i])
            cross_matrix = cross_normal_to_oz(position_upper_points_from_lower[i], R, r)
            # Координаты точек пересечения в локальных координатах
            local_cross_coordinates[i] = matrix_1_4(cross_matrix[0], cross_matrix[1], cross_matrix[2])
            # Углы рычагов
            if border_of_arm_angle[0] <= cross_matrix[3]*180/pi <= border_of_arm_angle[1]:
                arm_angle[i] = cross_matrix[3]
            else:
                print(f'Угол рычага {i+1} = {cross_matrix[3]*180/pi} => не входит в допустимый диапазон')
                return False
            # Эти локальные координаты являются частью объекта, который мы и переносим
            global_cross_coordinates[i] =  matrix_move_lower_plate[i].dot(local_cross_coordinates[i])
    #_____________________________________________________________________________________________________________________________________________________________

            """4.2 Поиск углов шаровых наконечников ног"""

            # Матрица перемещения для СК точек пересечения
            matrix_move_crosspoints[i] = matrix_move_lower_plate[i].dot(
                                        transition_matrix(local_cross_coordinates[i][0][0], local_cross_coordinates[i][1][0], local_cross_coordinates[i][2][0]))

            # Находим координаты верхней шаровой относительно точек пересечения
            coordinates_upper_points_from_crosspoints[i] = linalg.inv(matrix_move_crosspoints[i]).dot(upper_points[i])
            # Находим координаты нижней шаровой относительно верхней
            coordinates_crosspoints_from_upper_points[i] = linalg.inv(matrix_move_upper_plate[i]).dot(global_cross_coordinates[i])

            # Найдём угол между проекцией тяги (на XY) и верхней точки, чтобы повернуть XY на полученный угол (тяга няходится в 1-ей четверти)
            angles_between_crosspoints_and_upper_points[i] = atan2(coordinates_upper_points_from_crosspoints[i][1][0], coordinates_upper_points_from_crosspoints[i][0][0])
            # Для верхней точки плиты тяга няходится в 3-ей четверти, поэтому ближе повернуть плоскость YZ, а не XZ
            angles_between_upper_points_and_crosspoints[i] = atan2(coordinates_crosspoints_from_upper_points[i][0][0], coordinates_crosspoints_from_upper_points[i][1][0])

            # Матрицы поворота СК (чтобы тяга лежала в плоскости ZX)
            matrix_rotate_cs_crosspoints_to_upper_points[i] = rotation_matrix(0, 0, angles_between_crosspoints_and_upper_points[i])
            # Матрицы поворота СК (чтобы тяга лежала в плоскости ZY)
            matrix_rotate_cs_upper_points_to_crosspoints[i] = rotation_matrix(0, 0, -angles_between_upper_points_and_crosspoints[i])

            # Создадим общую матрицу перемещения до точки пересечения с последующим поворотом до XZ
            matrix_move_to_new_cs_of_crosspoints[i] = matrix_move_crosspoints[i].dot(matrix_rotate_cs_crosspoints_to_upper_points[i]) 
            # Создадим общую матрицу перемещения до верхней точки с последующим поворотом до YZ
            matrix_move_to_new_cs_of_upper_points[i] = matrix_move_upper_plate[i].dot(matrix_rotate_cs_upper_points_to_crosspoints[i])

            # Узнаем координаты верхнего шарнира точки пересечения в новой СК
            coordinates_upper_points_from_crosspoints_in_new_planes[i] = linalg.inv(matrix_move_to_new_cs_of_crosspoints[i]).dot(upper_points[i])
            # Узнаем координаты нижнего шарнира относительно верхнего в новой СК
            coordinates_crosspoints_from_upper_points_in_new_planes[i] = linalg.inv(matrix_move_to_new_cs_of_upper_points[i]).dot(global_cross_coordinates[i])

            # Найдём углы
            angle_lower_joint[i] = atan2(coordinates_upper_points_from_crosspoints_in_new_planes[i][2][0], coordinates_upper_points_from_crosspoints_in_new_planes[i][0][0])
            angle_upper_joint[i] = atan2(coordinates_crosspoints_from_upper_points_in_new_planes[i][2][0], coordinates_crosspoints_from_upper_points_in_new_planes[i][1][0])

    return arm_angle, angle_lower_joint, angle_upper_joint