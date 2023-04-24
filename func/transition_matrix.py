from numpy import array


# Сюда записываем конечные координаты точки (На сколько переместимся)
def transition_matrix(X, Y, Z):
    transition_matrix = array([[1, 0, 0, X], 
                               [0, 1, 0, Y],
                               [0, 0, 1, Z],
                               [0, 0, 0, 1]])
    return transition_matrix