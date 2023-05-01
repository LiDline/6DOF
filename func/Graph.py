from datetime import date
from math import pi
import plotly.graph_objects as go


from func.added_first_number import a_f_n


class Graph():
    def __init__(self, fig, lower_points, upper_points, move_upper_CS,
                 ):
        self.fig = fig
        self.color = ['black', 'purple', 'brown', 'green', 'orange', 'wheat']
        self.lower_points = lower_points
        self.upper_points = upper_points
        self.move_upper_CS = move_upper_CS

    #  Отрисовка тяг и рычагов
    def legs(self, i, group, arm_angle, global_cross_coordinates):
        self.fig.add_trace(go.Scatter3d(x=[a_f_n(self.lower_points, 0)[i], a_f_n(global_cross_coordinates, 0)[i]],
                                        y=[a_f_n(self.lower_points, 1)[i], a_f_n(
                                            global_cross_coordinates, 1)[i]],
                                        z=[a_f_n(self.lower_points, 2)[i], a_f_n(
                                            global_cross_coordinates, 2)[i]],
                                        showlegend=True, name=f'Рычаг ({round(arm_angle[i]*180/pi, 2)})',
                                        opacity=1, legendgroup=group, marker=dict(size=5, color=self.color[i], colorscale='Viridis'), line=dict(width=2)))
        self.fig.add_trace(go.Scatter3d(x=[a_f_n(global_cross_coordinates, 0)[i], a_f_n(self.upper_points, 0)[i]],
                                        y=[a_f_n(global_cross_coordinates, 1)[
                                            i], a_f_n(self.upper_points, 1)[i]],
                                        z=[a_f_n(global_cross_coordinates, 2)[
                                            i], a_f_n(self.upper_points, 2)[i]],
                                        showlegend=False, opacity=1, legendgroup=group, marker=dict(size=5, color=self.color[i], colorscale='Viridis'), line=dict(width=2)))

    # Отрисовка СК
    def coordinate_system(self, coordinate_system, i, base=None):
        width = 4
        opacity = 1

        if base:
            width = 8

        self.fig.add_trace(go.Scatter3d(x=[a_f_n(coordinate_system, 0)[3]],
                                        y=[a_f_n(coordinate_system, 1)[3]],
                                        z=[a_f_n(coordinate_system, 2)[3]],
                                        showlegend=False, opacity=1, legendgroup=f"group{i}", marker=dict(size=width-1, color='gray', colorscale='Viridis',)))

        self.fig.add_trace(go.Scatter3d(x=[a_f_n(coordinate_system, 0)[3], a_f_n(coordinate_system, 0)[0]],
                                        y=[a_f_n(coordinate_system, 1)[3],
                                           a_f_n(coordinate_system, 1)[0]],
                                        z=[a_f_n(coordinate_system, 2)[3],
                                           a_f_n(coordinate_system, 2)[0]],
                                        showlegend=False, opacity=opacity, legendgroup=f"group{i}", marker=dict(size=1, color='red', colorscale='Viridis',), line=dict(width=width)))
        self.fig.add_trace(go.Scatter3d(x=[a_f_n(coordinate_system, 0)[3], a_f_n(coordinate_system, 0)[1]],
                                        y=[a_f_n(coordinate_system, 1)[3],
                                           a_f_n(coordinate_system, 1)[1]],
                                        z=[a_f_n(coordinate_system, 2)[3],
                                           a_f_n(coordinate_system, 2)[1]],
                                        showlegend=False, opacity=opacity, legendgroup=f"group{i}", marker=dict(size=1, color='green', colorscale='Viridis',), line=dict(width=width)))
        self.fig.add_trace(go.Scatter3d(x=[a_f_n(coordinate_system, 0)[3], a_f_n(coordinate_system, 0)[2]],
                                        y=[a_f_n(coordinate_system, 1)[3],
                                           a_f_n(coordinate_system, 1)[2]],
                                        z=[a_f_n(coordinate_system, 2)[3],
                                           a_f_n(coordinate_system, 2)[2]],
                                        showlegend=False, opacity=opacity, legendgroup=f"group{i}", marker=dict(size=1, color='blue', colorscale='Viridis',), line=dict(width=width)))

    # Отрисовка верхней плиты
    def upper_plate(self):
        self.fig.add_trace(go.Scatter3d(x=a_f_n(self.upper_points[:6], 0), y=a_f_n(self.upper_points[:6], 1), z=a_f_n(self.upper_points[:6], 2),
                                        showlegend=True, name='Верхняя плита', surfaceaxis=2,  opacity=0.3, legendgroup="group7", marker=dict(size=1, color='royalblue', colorscale='Viridis',)))
        self.fig.add_trace(go.Scatter3d(x=a_f_n(self.upper_points[:6], 0), y=a_f_n(self.upper_points[:6], 1), z=a_f_n(self.upper_points[:6], 2),
                                        showlegend=False, surfaceaxis=-1, opacity=0.8, legendgroup="group7", marker=dict(size=1, color='black', colorscale='Viridis',)))

    # Отрисовка нижней плиты
    def lower_plate(self):
        self.fig.add_trace(go.Scatter3d(x=a_f_n(self.lower_points[:6], 0), y=a_f_n(self.lower_points[:6], 1), z=a_f_n(self.lower_points[:6], 2),
                                        showlegend=True, name='Нижняя плита', surfaceaxis=2,  opacity=0.3, legendgroup="group8", marker=dict(size=1, color='red', colorscale='Viridis',)))
        self.fig.add_trace(go.Scatter3d(x=a_f_n(self.lower_points[:6], 0), y=a_f_n(self.lower_points[:6], 1), z=a_f_n(self.lower_points[:6], 2),
                                        showlegend=False, surfaceaxis=-1, opacity=0.8, legendgroup="group8", marker=dict(size=1, color='black', colorscale='Viridis',)))


    # локальная СК нижней плиты (верхняя отрисовывается от матрицы перемещений)
    def coordinate_system_lower_plate(self):
        self.fig.add_trace(go.Scatter3d(x=[0, 100], y=[0, 0], z=[0, 0],
                                        showlegend=False, opacity=1, legendgroup="group8", marker=dict(size=1, color='red', colorscale='Viridis',), line=dict(width=7)))
        self.fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 100], z=[0, 0],
                                        showlegend=False, opacity=1, legendgroup="group8", marker=dict(size=1, color='green', colorscale='Viridis',), line=dict(width=7)))
        self.fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, 100],
                                        showlegend=False, opacity=1, legendgroup="group8", marker=dict(size=1, color='blue', colorscale='Viridis',), line=dict(width=7)))
        self.fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0],
                                        showlegend=False, opacity=1, legendgroup="group8", marker=dict(size=7, color='gray', colorscale='Viridis',)))

    # Легенда
    def title(self):
        self.fig.update_layout(title={'text': f"Δ = [{self.move_upper_CS[0]}, {self.move_upper_CS[1]}, {self.move_upper_CS[2]}, {self.move_upper_CS[3]}, {self.move_upper_CS[4]}, {self.move_upper_CS[5]}]; {date.today()}",
                                      'y': 0.97, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    # Оформление
    def decor(self):
        tickf = 12

        self.fig.update_layout(legend=dict(
            yanchor="top", y=0.99, xanchor="left", x=0.7))

        self.fig.update_layout(autosize=True, scene={'camera_eye': {"x": -2, "y": 2, "z": 1.65}, 
                                                     'camera_center': {"x": -0.3, "y": 0, "z": 0}, },
                            #    width=950, height=500, 
                               margin=dict(l=10, r=0, b=10, t=50))

        self.fig.update_layout(scene=dict(xaxis=dict(title="X", backgroundcolor="rgb(200, 200, 230)", gridcolor="white",
                                                     showbackground=True, zerolinecolor="white", tickfont=dict(size=tickf)),
                                          yaxis=dict(title="Y", backgroundcolor="rgb(230, 200,230)", gridcolor="white",
                                                     showbackground=True, tickfont=dict(size=tickf), zerolinecolor="white"),
                                          zaxis=dict(title="Z", backgroundcolor="rgb(200, 200,200)", gridcolor="white",
                                                     showbackground=True, tickfont=dict(size=tickf), zerolinecolor="white",)))

        self.fig.update_layout(scene=dict(
            xaxis_showspikes=False, yaxis_showspikes=False),)
        self.fig.update_scenes(camera_projection_type="orthographic")
