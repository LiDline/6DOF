import numpy as np


# Запись данных для go.Scatter3d
def a_f_n(string, i):
    return np.append((string[:, i])[:, 0], (string[:, i])[0])  