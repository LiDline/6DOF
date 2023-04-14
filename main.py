from numpy import  zeros, array, linalg, pi, sqrt, radians
from math import atan2


from func.rotation_matrix import rotation_matrix
from func.transition_matrix import transition_matrix
from func.matrix_1_4 import matrix_1_4
from func.cross_normal_to_oz import cross_normal_to_oz
from constants import constants


# Константы
max_angle_spherical_joint, border_of_arm_angle, R, r, moving_gas_spring, offset_lower, offset_upper, rotate_local_cs, local_lower_CS, local_upper_CS = constants()

#_____________________________________________________________________________________________________________________________________________________________


def solve(x, y, z, alpha, beta, gamma):

    move_upper_CS = array((x, y, z, alpha, beta, gamma))    # Смещение центра верхней плиты

    """2. Объявим используемые массивы"""

    # Матрица переноса нижней плиты
    matrix_move_lower_plate = zeros((9,4,4))
    # Точки нижней плиты
    lower_points = zeros((9,4,1))
    # Матрица переноса верхней плиты
    matrix_move_upper_plate = zeros((9,4,4))
    # Точки верхней плиты
    upper_points = zeros((9,4,1))
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
    # Углы шаровых
    angle_lower_joint = zeros(9)
    angle_upper_joint = zeros(9)
    # Расчёт нижнего шарнира пружины
    coordinates_upper_joint_of_gas_spring_from_lower = zeros((3,4,1))
    angles_between_spring_and_ZY_of_lower_joint = zeros(3) 
    matrix_rotate_cs_lower_joint_of_gas_spring =  zeros((3,4,4))
    matrix_move_to_new_cs_of_lower_joint_of_gas_spring = zeros((3,4,4))
    coordinates_upper_joint_gas_spring_from_lower_in_new_planes = zeros((3,4,1))
    # Расчёт верхнего шарнира пружины
    coordinates_lower_joint_of_gas_spring_from_upper = zeros((3,4,1))
    angles_between_spring_and_ZY_of_upper_joint = zeros(3) 
    matrix_rotate_cs_upper_joint_of_gas_spring = zeros((3,4,4))
    matrix_move_to_new_cs_of_upper_joint_of_gas_spring = zeros((3,4,4))
    coordinates_lower_joint_gas_spring_from_upper_in_new_planes = zeros((3,4,1))
    len_spring = zeros(3)
#_____________________________________________________________________________________________________________________________________________________________

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
    #_____________________________________________________________________________________________________________________________________________________________              
  
    for i in range(6):

        """4. Точки пересечения"""

        position_upper_points_from_lower[i] = linalg.inv(matrix_move_lower_plate[i]).dot(upper_points[i])
        cross_matrix = cross_normal_to_oz(position_upper_points_from_lower[i], R, r)
        # Координаты точек пересечения в локальных координатах
        local_cross_coordinates[i] = matrix_1_4(cross_matrix[0], cross_matrix[1], cross_matrix[2])
        # Углы рычагов
        if border_of_arm_angle[0] <= cross_matrix[3]*180/pi <= border_of_arm_angle[1]:
            arm_angle[i] = cross_matrix[3]
        else:
            return f'Угол рычага {i+1} = {cross_matrix[3]*180/pi} => не входит в допустимый диапазон'
        # Эти локальные координаты являются частью объекта, который мы и переносим
        global_cross_coordinates[i] =  matrix_move_lower_plate[i].dot(local_cross_coordinates[i])
#_____________________________________________________________________________________________________________________________________________________________

        """5. Поиск углов шаровых наконечников ног"""

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
#_____________________________________________________________________________________________________________________________________________________________

    """6. Поиск углов шаровых наконечников пружин"""

    for i in range(3):
        # Находим координаты верхней шаровой относительно нижней
        coordinates_upper_joint_of_gas_spring_from_lower[i] = linalg.inv(matrix_move_lower_plate[i+6]).dot(upper_points[i+6])
        coordinates_lower_joint_of_gas_spring_from_upper[i] = linalg.inv(matrix_move_upper_plate[i+6]).dot(lower_points[i+6])

        # Найдём угол между проекцией пружины (на YX) и ZY, чтобы повернуть XY на полученный угол по OZ (пружина няходится в 1-ей четверти)
        angles_between_spring_and_ZY_of_lower_joint[i] = atan2(coordinates_upper_joint_of_gas_spring_from_lower[i][0][0], coordinates_upper_joint_of_gas_spring_from_lower[i][1][0])
        # (пружина няходится в 3-ей четверти)
        angles_between_spring_and_ZY_of_upper_joint[i] = atan2(coordinates_lower_joint_of_gas_spring_from_upper[i][0][0], coordinates_lower_joint_of_gas_spring_from_upper[i][1][0])

        # Матрицы поворота СК (чтобы пружина лежала в плоскости ZY)
        matrix_rotate_cs_lower_joint_of_gas_spring[i] = rotation_matrix(0, 0, -angles_between_spring_and_ZY_of_lower_joint[i])
        # Матрицы поворота СК (чтобы пружина лежала в плоскости ZX)
        matrix_rotate_cs_upper_joint_of_gas_spring[i] = rotation_matrix(0, 0, -angles_between_spring_and_ZY_of_upper_joint[i])

        # Создадим общую матрицу перемещения с последующим поворотом
        matrix_move_to_new_cs_of_lower_joint_of_gas_spring[i] = matrix_move_lower_plate[i+6].dot(matrix_rotate_cs_lower_joint_of_gas_spring[i])
        # Создадим общую матрицу перемещения с последующим поворотом
        matrix_move_to_new_cs_of_upper_joint_of_gas_spring[i] = matrix_move_upper_plate[i+6].dot(matrix_rotate_cs_upper_joint_of_gas_spring[i]) 

        # Узнаем координаты верхнего шарнира точки пересечения в новой СК
        coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i] = linalg.inv(matrix_move_to_new_cs_of_lower_joint_of_gas_spring[i]).dot(upper_points[i+6])
        # Узнаем координаты нижнего шарнира точки пересечения в новой СК
        coordinates_lower_joint_gas_spring_from_upper_in_new_planes[i] = linalg.inv(matrix_move_to_new_cs_of_upper_joint_of_gas_spring[i]).dot(lower_points[i+6])

        # Найдём углы шаровой
        angle_lower_joint[i+6] = atan2(coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i][2][0], coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i][1][0])
        angle_upper_joint[i+6] = atan2(coordinates_lower_joint_gas_spring_from_upper_in_new_planes[i][2][0], coordinates_lower_joint_gas_spring_from_upper_in_new_planes[i][1][0])

        len_spring[i] = sqrt(coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i][0][0]**2 + coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i][1][0]**2 +
                        coordinates_upper_joint_gas_spring_from_lower_in_new_planes[i][2][0]**2)

        # Если длина пружины <> её max/min - отметаем решение
        if len_spring[i] >= moving_gas_spring[1]:
            return 'Длина пружины больше допустимой max'
        elif len_spring[i] <= moving_gas_spring[0]:
            return 'Длина пружины меньше допустимой min'

    # Если у одной шаровой угол > max_angle_spherical_joint - отметаем решение
    for i in range(9):
        if abs(angle_lower_joint[i]*180/pi) > max_angle_spherical_joint or abs(angle_upper_joint[i]*180/pi) > max_angle_spherical_joint:
            return f'Угол {i+1}-ой шаровой = {angle_lower_joint*180/pi} => превышает допустимый'
        
    return arm_angle


if __name__ == "__main__":
    print(solve(25, 25, 300, 5, 5, 5)*180/pi)