

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
    len_c = len(matrix[0])
    value = 0
    pivot_column = 0
    for column in range(1, len_c):
        if (matrix[0][column] < value):
            value = matrix[0][column]
            pivot_column = column
    return pivot_column

def multiply_row(row, scalar):
    n_row = []
    n_row.append(row[0])
    for i in range(1,len(row)):
        n_row.append(float("{0:.4f}".format(row[i]*scalar)))
    return n_row


def subtract_row(row, row2):
    n_row = []
    n_row.append(row[0])
    for i in range(1,len(row)):
        n_row.append(float("{0:.4f}".format(row[i]-row2[i])))
    return n_row

def change_m_row(row):
    len_row = len(row)
    new_row = []
    for i in range(len_row):
        if(str(row[i]).count('M') > 0):
            new_row.append(row[i].subs(M,1000))
        else:
            new_row.append(row[i])
    return new_row