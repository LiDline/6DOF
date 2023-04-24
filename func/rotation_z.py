# i - строка, j - столбец (3, т.к. xyz), xyz_0 - матрица с коорд. xyz, где 1-ый стобец - это x, 3-ий - z
def R_z(angle, xyz_0): 

    from numpy import cos, sin, array, pi, zeros
     
    yaw = (angle/180) * pi
    R_matrix = array([[cos(yaw), -sin(yaw), 0],        
                    [sin(yaw),  cos(yaw), 0],
                    [0, 0, 1]])    
 
    xyz = zeros((3, len(xyz_0[0])))

    for i in range(0, len(xyz_0[0])):   
        R0_matrix = array([[xyz_0[0][i]], 
                        [xyz_0[1][i]],
                        [xyz_0[2][i]]])                   
        xyz[:, i] = R_matrix.dot(R0_matrix)[:, 0]               

    return xyz