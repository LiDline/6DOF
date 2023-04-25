from numpy import array


# Запись получаемых координат XYZ (из cross_normal_to_oz.py) в ортогональных координатах (добавляем 1 в конец списка)
def matrix_1_4(X,Y,Z):
    return array([[X],[Y],[Z],[1]])