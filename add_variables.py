import sympy as sym

'''
Arreglo global que almacena los tipos de variables que tengo:
 x: variables iniciales de la funcion objeto
 slack: variables de holgura
 artificial: variables artificiales 
 excess: variables de exceso
La posicion de la variable en el arreglo corresponde al subindice de la misma,
es por esta razon que la posicion cero se rellena con 0.
'''
variables = []

def add_variables(matrix, minmax):
    global variables
    variables = []

    M = sym.Symbol('M')
    new_matrix = []

    col_len = len(matrix[0])
    row_len = len(matrix)

    add_initial_variables(col_len)

    #first row, quito los dos ultimos elementos de relleno
    zero_row = matrix[0]
    zero_row.pop()
    zero_row.pop()
    zero_row = multiply_row(-1, zero_row)

    '''
    Si es minimizacion tiene que multiplicar la M por -1, ya que es el valor de 
    la M después de haber igualado a 0 la funcion objeto
    '''
    minmax_val = 1
    if (minmax == "min"): 
        minmax_val = -1

    for row in range(1, row_len):
        new_row = []
        for col in range(col_len):
            if (col == col_len-2):
                ##holgura
                if (matrix[row][col] == "<="):
                    variables.append("slack")
                    zero_row.append(0)
                #artificial    
                elif (matrix[row][col] == "="):
                    variables.append("artificial")
                    zero_row.append(M * minmax_val)
                #exceso y artificial
                elif (matrix[row][col] == ">="):
                    variables.append("excess")
                    variables.append("artificial")
                    zero_row.append(0)
                    zero_row.append(M * minmax_val)
            else:
                new_row.append(matrix[row][col])
        new_matrix.append(new_row)
    zero_row.append(0)
    new_matrix.insert(0,zero_row)
    new_matrix = add_variables_aux(new_matrix)
    return new_matrix, variables

def multiply_row(scalar, row):
    M = sym.Symbol('M')
    res = []
    for n in row:
        res.append(n*scalar)
    return res

def add_initial_variables(col_len):
    global variables
    variables.append(0)

    for i in range(1,col_len-2): #no cuenta los dos ultimos ceros de relleno
        variables.append("x")
    return

'''
La funcion va agregando lo valores por columna y se va guiando con el arreglo "variables"
para saber si tiene que agregar un 1 o un -1 y un 1 por el >= 
'''
def add_variables_aux(matrix):
    global variables

    variables_len = len(variables)
    j = 1
    while (j < variables_len):
        excess = False
        i = 1
        while (i < len(matrix)):
            if (variables[j] == "slack" or variables[j] == "artificial"):
                if (j == i+2):
                    matrix[i].insert(j, 1)
                else:
                    matrix[i].insert(j, 0)
            elif (variables[j] == "excess"):
                if (j == i+2):
                    matrix[i].insert(j, -1)
                    matrix[i].insert(j+1, 1)
                else:
                    matrix[i].insert(j, 0)
                    matrix[i].insert(j+1, 0)
                excess = True
            i += 1
        if (excess):
            j += 2
        else:
            j += 1
    return matrix


def main():
    global variables
    test_matrix = [[0, 3, 5, 0, 0], [0, 1, 0, "<=", 4], [0, 0, 2, "<=", 12], [0, 3, 2, "=", 18]] #simbolo está en col_len - 2 
    test_matrix_excess = [[0, 0.4, 0.5, 0, 0], [0, 0.3, 0.1, "<=", 2.7], [0, 0.5, 0.5, "=", 6], [0, 0.6, 0.4, ">=", 6]]
    print("Prueba 1: ", add_variables(test_matrix, "max"))
    print(variables)
    print("\nPrueba 2: ", add_variables(test_matrix_excess, "min"))
    print(variables)

if __name__ == "__main__":
    main()