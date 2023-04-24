from numpy import array, sqrt, arccos


# Функция нахождения точки пересечения окружности и сферы
def cross_point(matrix, R, r):
    X = matrix[0][0] # Нахожу смещение между координатами окружности и проекции сферы 
    Y = matrix[1][0]
    Z = matrix[2][0]

    A = -(r**2-X**2-R**2-Y**2-Z**2)/2

    a = Y**2+Z**2
    b = -2*A*Y
    c = A**2 - (Z**2) * (R**2)

    D = b**2 - 4*a*c
    y_1 = (-b+sqrt(D))/(2*a)
    y_2 = (-b-sqrt(D))/(2*a)

    z_1 = sqrt(R**2-y_1**2)
    z_2 = sqrt(R**2-y_2**2)

    t_1, t_2 = arccos(y_1/R), arccos(y_2/R)

    return array([[0, y_1, z_1, t_1], 
                [0, y_2, z_2, t_2]])   # X = 0, т.к. считаем, что окружность лежит в плоскости ZX 