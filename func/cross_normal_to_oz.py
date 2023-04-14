from numpy import array, sqrt
from math import atan2


# Точки пересечения между окружностью (редуктором) и сферой (тяга)
def cross_normal_to_oz(matrix, R, r):   # https://hedgedoc.auto-sys.su/JAqGGd3JRn-qmUJVMdjODg

    X = matrix[0][0] # Нахожу смещение между координатами окружности и проекции сферы 
    Y = matrix[1][0]
    Z = matrix[2][0]

    A = -(r**2-Z**2-R**2-X**2-Y**2)/2

    a = X**2+Y**2
    b = -2*A*X
    c = A**2 - (Y**2) * (R**2)
        
    D = b**2 - 4*a*c    # Дискриминант

    if D >= 0:
        x_1, x_2 = (-b+sqrt(D))/(2*a), (-b-sqrt(D))/(2*a)
        y_1, y_2 = (A-X*x_1)/Y, (A-X*x_2)/Y
        t_1, t_2 = atan2(x_1, y_1), atan2(x_2, y_2) # Получаю угол относительно OY

        if t_2 >= t_1:
            return  array([x_1, y_1, 0, t_1])   # X = 0, т.к. считаем, что окружность лежит в плоскости ZX 
        elif t_1 > t_2:
            return  array([x_2, y_2, 0, t_2])
    else:
        return 'Превышена длина ноги'        