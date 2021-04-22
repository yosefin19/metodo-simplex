import sympy as sym
import math
M = sym.Symbol('M')

#se debe llamar antes de la funcion que saca los pivotes
''' Si la U es no acotada, el MS termina, y se indica que la U es no acotada '''
def is_unbounded(matrix):
    pivot_column = get_pivot_column(matrix)
    len_matrix = len(matrix)
    ''' para sacar los coeficientes mínimos solo se utilizan las restricciones,
    por eso empieza en 1 '''
    for row in range(1, len_matrix):

        ''' si hay un número positivo, entonces es acotada '''
        if (matrix[row][pivot_column] > 0):
            return False
    return True
    

def get_pivot_column(matrix):
    zero_row = change_m_row(matrix[0])
    zero_row.pop()
    minimum = min(zero_row)
    pivot_column = zero_row.index(minimum)
    return pivot_column


''' establece el valor de las M en mil para poder comparar '''
def change_m_row(row):
    len_row = len(row)
    new_row = []
    for i in range(len_row):
        if(str(row[i]).count('M') > 0):
            new_row.append(row[i].subs(M,1000))
        else:
            new_row.append(row[i])
    return new_row


def change_m_value(value):
    if(str(value).count('M') > 0):
        temp = [value]
        value = temp[0].subs(M,1000)
    return value


def multiply_row(row, scalar):
    n_row = []
    n_row.append(row[0])
    for i in range(1,len(row)):
        if(str(row[i]).count('M') > 0 or str(scalar).count('M') > 0):
            n_row.append(row[i]*scalar)
        else:
            ''' n_row.append(float("{0:.4f}".format(float(row[i]) * float(scalar)))) devolver'''
            n_row.append(float(row[i]) * float(scalar))
    return n_row


def subtract_row(row, row2):
    n_row = []
    n_row.append(row[0])
    for i in range(1,len(row)):
        if(str(row[i]).count('M') > 0 or str(row2[i]).count('M') > 0):
            n_row.append(row[i]-row2[i])
        else:
            ''' n_row.append(float("{0:.4f}".format(float(row[i]) - float(row2[i])))) '''
            n_row.append(float(row[i]) - float(row2[i]))
    return n_row