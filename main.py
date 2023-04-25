from numpy import array, pi


from func.plate_coordinates import plate_coordinates
from func.leg_ball_corners import leg_ball_corners
from func.spring_ball_corners import spring_ball_corners
import constants
from func.coordinate_system import coordinate_system


max_angle_spherical_joint = constants.MAX_ANGLE_SPHERICAL_JOINT


def solve(x, y, z, alpha, beta, gamma):

    # Смещение центра верхней плиты
    move_upper_CS = array((x, y, z, alpha, beta, gamma))

    """"2. Координаты плит"""

    matrix_move_lower_plate, matrix_move_upper_plate, lower_points, upper_points, matrix_move_upper_CS = plate_coordinates(
        move_upper_CS)

    """3. Точки пересечения"""
    arm_angle, angle_lower_joint, angle_upper_joint, global_cross_coordinates, local_cross_coordinates, local_coordinate_system_upper_point, local_coordinate_system_crosspoints_after_rotate = leg_ball_corners(
        matrix_move_lower_plate, upper_points, matrix_move_upper_plate)

    """4. Поиск углов шаровых наконечников пружин"""

    angle_lower_joint, angle_upper_joint, local_coordinate_system_cs_lower_joint_of_gas_spring, local_coordinate_system_cs_upper_joint_of_gas_spring = spring_ball_corners(
        upper_points, lower_points, matrix_move_lower_plate, matrix_move_upper_plate, angle_lower_joint, angle_upper_joint)

    """5. Проверка углов шаровых опор"""

    # Если у одной шаровой угол > max_angle_spherical_joint - отметаем решение
    for i in range(9):
        if abs(angle_lower_joint[i]*180/pi) > max_angle_spherical_joint or abs(angle_upper_joint[i]*180/pi) > max_angle_spherical_joint:
            return f'Угол {i+1}-ой шаровой = {angle_lower_joint*180/pi} => превышает допустимый'

    global_coordinate_system_upper_plate, local_coordinate_system_lower_point, local_coordinate_system_crosspoints = coordinate_system(
        matrix_move_lower_plate, matrix_move_upper_CS, local_cross_coordinates, constants.GLOBAL_COORDINATE_SYSTEM)

    return move_upper_CS, lower_points, upper_points, arm_angle, global_cross_coordinates, angle_lower_joint, angle_upper_joint, matrix_move_lower_plate, matrix_move_upper_CS, local_cross_coordinates, global_coordinate_system_upper_plate, local_coordinate_system_lower_point, local_coordinate_system_crosspoints, local_coordinate_system_cs_lower_joint_of_gas_spring, local_coordinate_system_cs_upper_joint_of_gas_spring, local_coordinate_system_upper_point, local_coordinate_system_crosspoints_after_rotate
