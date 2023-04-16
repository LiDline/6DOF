from numpy import array, float64
import numba as nb

@nb.njit()
def matrix_1_4(X,Y,Z):
       
    return array(([X],[Y],[Z],[1]), dtype = float64)  # Сюда записываем куда переносим