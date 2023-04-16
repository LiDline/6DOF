from numpy import array, zeros

def zero_matrix(a):
    if a == 1:
        return array([zeros((4,4)), zeros((4,4)), zeros((4,4)), zeros((4,4)), zeros((4,4)), zeros((4,4)), zeros((4,4)), zeros((4,4)), zeros((4,4))])
    elif a == 2:
        return array([zeros((4,1)), zeros((4,1)), zeros((4,1)), zeros((4,1)), zeros((4,1)), zeros((4,1)), zeros((4,1)), zeros((4,1)), zeros((4,1))])