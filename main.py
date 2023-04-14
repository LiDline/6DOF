from numpy import array, pi


from func.plate_coordinates import plate_coordinates
from func.leg_ball_corners import leg_ball_corners
from func.spring_ball_corners import spring_ball_corners
from constants import constants


# Константы
max_angle_spherical_joint, border_of_arm_angle, R, r, moving_gas_spring, offset_lower, offset_upper, rotate_local_cs, local_lower_CS, local_upper_CS = constants()

#_____________________________________________________________________________________________________________________________________________________________


def solve(x, y, z, alpha, beta, gamma):

    move_upper_CS = array((x, y, z, alpha, beta, gamma))    # Смещение центра верхней плиты

    """"3. Координаты плит"""

    matrix_move_lower_plate, matrix_move_upper_plate, lower_points, upper_points = plate_coordinates(move_upper_CS, offset_lower, rotate_local_cs, local_lower_CS, offset_upper, local_upper_CS)
  
    """4. Точки пересечения"""
    arm_angle, angle_lower_joint, angle_upper_joint = leg_ball_corners(matrix_move_lower_plate, upper_points, matrix_move_upper_plate, border_of_arm_angle, R, r)

    """5. Поиск углов шаровых наконечников пружин"""

    angle_lower_joint, angle_upper_joint = spring_ball_corners(upper_points, lower_points, matrix_move_lower_plate, matrix_move_upper_plate, angle_lower_joint, angle_upper_joint, moving_gas_spring)

    """6. Проверка углов шаровых опор"""
    # Если у одной шаровой угол > max_angle_spherical_joint - отметаем решение
    for i in range(9):
        if abs(angle_lower_joint[i]*180/pi) > max_angle_spherical_joint or abs(angle_upper_joint[i]*180/pi) > max_angle_spherical_joint:
            return f'Угол {i+1}-ой шаровой = {angle_lower_joint*180/pi} => превышает допустимый'
        
    return arm_angle


if __name__ == "__main__":
    print(solve(25, 25, 300, 5, 5, 5)*180/pi)