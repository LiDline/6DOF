from func.Graph import Graph
from main import solve
import plotly.graph_objects as go


# return с main.py немного вырос
move_upper_CS, lower_points, upper_points, arm_angle, global_cross_coordinates, angle_lower_joint, angle_upper_joint, matrix_move_lower_plate, matrix_move_upper_CS, local_cross_coordinates, global_coordinate_system_upper_plate, local_coordinate_system_lower_point, local_coordinate_system_crosspoints, local_coordinate_system_cs_lower_joint_of_gas_spring, local_coordinate_system_cs_upper_joint_of_gas_spring, local_coordinate_system_upper_point, local_coordinate_system_crosspoints_after_rotate = solve(
    0, 0, 300, 0, 0, 0)


fig = go.Figure()
graph = Graph(fig, lower_points, upper_points, arm_angle, global_cross_coordinates,
              angle_lower_joint, angle_upper_joint,
              move_upper_CS)


# Отрисовка плит
graph.upper_plate()
graph.lower_plate()

# СК верхней и нижней плиты
graph.coordinate_system(global_coordinate_system_upper_plate, 7, 1)
graph.coordinate_system_lower_plate()

# Отрисовка рычагов, тяг и их СК
for i in range(6):
    graph.legs(i, f"group{i}")
    graph.coordinate_system(local_coordinate_system_lower_point[i], i)
    graph.coordinate_system(local_coordinate_system_upper_point[i], i)
    graph.coordinate_system(
        local_coordinate_system_crosspoints_after_rotate[i], i)

# Отрисовка пружин и их СК
for i in range(3):
    graph.springs(i)
    graph.coordinate_system(
        local_coordinate_system_cs_lower_joint_of_gas_spring[i], i+10)
    graph.coordinate_system(
        local_coordinate_system_cs_upper_joint_of_gas_spring[i], i+10)

# Оформление
graph.title()
graph.decor()

fig.show()
