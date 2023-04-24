from numpy import array


# Сюда записываем локальные начальные координаты точки
def init_points(X,Y,Z):
    return array([[X],[Y],[Z],[1]])  