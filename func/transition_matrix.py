from numpy import array


def transition_matrix(X, Y, Z):
    transition_matrix = array([[1, 0, 0, X], # Сюда записываем НА сколько перемещаемся
                               [0, 1, 0, Y],
                               [0, 0, 1, Z],
                               [0, 0, 0, 1]])
    return transition_matrix