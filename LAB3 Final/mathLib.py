import math

def matMatMult(m1, m2):
    result = [[0 for _ in range(len(m2[0]))] for _ in range(len(m1))]
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                result[i][j] += m1[i][k] * m2[k][j]
    return result


def matMult(m1, m2):
    return [[sum(m1[x][i] * m2[i][y] for i in range(4)) for y in range(4)] for x in range(4)]

def matVectMult(mat, vect):
    return [sum(mat[x][y] * vect[y] for y in range(4)) for x in range(4)]

def barycentricCoordinates(A, B, C, P):

    areaPCB = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])
    areaABC = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
    areaACP = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])
    
    try:
        u = areaPCB / areaABC
        v = areaACP / areaABC
        w = 1 - u - v
    except:
        u = v = w = -1
    return u, v, w

# inverso de matrices

def sub_matrix(mat, row, col):
    return [row[:col] + row[col + 1:] for row in (mat[:row] + mat[row + 1:])]

def mat_cofactor(mat, row, col):
    return (-1) ** (row + col) * mat_determinant(sub_matrix(mat, row, col))

def mat_determinant(mat):
    n = len(mat)
    # 2x2 
    if n == 1:
        return mat[0][0]
    # 3x3
    if n == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    det = 0
    # Arriba de 3
    for col in range(n):
        det += mat[0][col] * mat_cofactor(mat, 0, col)
    return det

def mat_transpose(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]

def normalMatMult(mats):
    res = [[1,0,0,0],
           [0,1,0,0],
           [0,0,1,0],
           [0,0,0,1]]
    
    for mat in mats:
        res = matMult(res,mat)
    return res

def inverse_matrix(mat):
    det = mat_determinant(mat)
 
    if det == 0:
        raise ValueError("Can't find inverse of singular matrix (Determinant is 0)")
    n = len(mat)

    adj_matrix = [[mat_cofactor(mat, i, j) for j in range(n)] for i in range(n)]
    adj_matrix = mat_transpose(adj_matrix)
   
    inv_matrix = [[adj_matrix[i][j] / det for j in range(n)] for i in range(n)]
    return inv_matrix

def sub_vector(v0, v1):
    
    return (v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2])

def norm_vector(v):
    vector_list = list(v)
    
    mag = math.sqrt(sum(comp ** 2 for comp in vector_list))
    
    if mag == 0:
        raise ValueError("Can't normalize the zero vector")
    
    norm_vector = [comp / mag for comp in vector_list]
   
    norm_vector = tuple(norm_vector)
    return norm_vector

def VectorMag(v):
    vectorList = list(v)
    return math.sqrt(sum(comp ** 2 for comp in vectorList))

def cross_product(v0, v1):
    x = v0[1] * v1[2] - v0[2] * v1[1]
    y = v0[2] * v1[0] - v0[0] * v1[2]
    z = v0[0] * v1[1] - v0[1] * v1[0]
    return x, y, z

def producto_punto(v0, v1):
    return sum(a * b for a, b in zip(v0, v1))

def negative_tuple(t):
    return tuple(-x for x in t)

def MultVectorEsc(s, v):
    result = [s * x for x in v]
    return result
    
def DivVectorEsc(v, s):
    result = [x / s for x in v]
    return result

def AddVec(v0, v1):
    return (v0[0]+v1[0], v0[1]+v1[1], v0[2]+v1[2])

def rotate_vector(vec, angle):
    x, y, z = vec
    rx = math.radians(angle[0])
    ry = math.radians(angle[1])
    rz = math.radians(angle[2])
    sinx, cosx = math.sin(rx), math.cos(rx)
    siny, cosy = math.sin(ry), math.cos(ry)
    sinz, cosz = math.sin(rz), math.cos(rz)

    y, z = y * cosx - z * sinx, y * sinx + z * cosx

    x, z = x * cosy + z * siny, x * -siny + z * cosy

    x, y = x * cosz - y * sinz, x * sinz + y * cosz

    return (x, y, z)