

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