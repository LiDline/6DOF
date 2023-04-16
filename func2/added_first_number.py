def a_f_n(string, i):
    import numpy as np

    return np.append((string[:, i])[:, 0], (string[:, i])[0])  # для отрисовки графика