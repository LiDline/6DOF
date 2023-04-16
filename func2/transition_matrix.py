from numpy import array, float64
import numba as nb

@nb.njit()
def transition_matrix(X, Y, Z):
    

    transition_matrix = array(([1, 0, 0, X], # Сюда записываем НА сколько перемещаемся
                               [0, 1, 0, Y],
                               [0, 0, 1, Z],
                               [0, 0, 0, 1]), dtype = float64)
    return transition_matrix 