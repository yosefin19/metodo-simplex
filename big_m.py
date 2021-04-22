import sympy as sym
from add_variables import add_variables
from add_variables import multiply_row
from simplex import simplex

M = sym.Symbol('M')

''' Se encarga de resolver un problema por medio del método
de la gran M '''
def big_m(matrix, minmax):
    matrix, variables = add_variables(matrix, minmax)
    
    variables_amount = len(matrix[0]) -2
    restrictions_amount = len(matrix) -1
    degrees_freedom = variables_amount - restrictions_amount

    if (minmax == "min"):
        ''' transforma a maximizacion para el metodo simplex tabular '''
        matrix[0] = multiply_row(-1, matrix[0]) 
    
    len_zero_row = len(matrix[0])
    ''' si tengo variables de exceso, cada una hace que tenga una columna más que filas,
    entonces tengo que restar esa posicion para saber en cual fila esta la artificial
    que corresponde a la M encontrada '''
    amount_excess_variables = 0

    ''' quitar las variables artificiales de la fila cero utilizando operaciones gauss-jordan 
        al rango le quito 1 porque sé que la última columna no interesa '''
    for index in range(len_zero_row-1):
        zero_row = matrix[0]
        if (variables[index] == "excess"):
            amount_excess_variables += 1
            continue
        if (zero_row[index] ==  M):
            '''
            Multiplico por M la fila donde esta la variable artificial.
            Esto como parte de la operacion gauss-jordan.
            '''
            multiplied_row = multiply_row(M, matrix[index-2-amount_excess_variables])

            '''
            Le resto a la fila 0 la fila con la variable artificial, esto
            para eliminar la variable artificial acompañada por M en la fila 0
            '''
            subtracted_row = subtract_rows(matrix[0], multiplied_row)
            matrix.insert(0, subtracted_row)

            ''' elimino la antigua fila cero '''
            matrix.pop(1) 

    matrix = add_basic_variables(matrix, degrees_freedom, variables)
    optimal_solution_matrixes = simplex(matrix, variables)
 
    ''' arreglo de la forma [ [[x1, x2,..., xn], U], [[x1, x2,..., xn], U] ] pueden ser max dos soluciones optimas'''
    optimal_solutions = extract_optimal_solutions(optimal_solution_matrixes)

    if (minmax == "min"):
        ''' transformar a minimización de vuelta la U '''
        for i in range(len(optimal_solutions)):
            optimal_solutions[i][1] *= -1

    return optimal_solution_matrixes, optimal_solutions
 
            
''' Resta dos filas'''
def subtract_rows(row1, row2):
    res_row = []
    for i in range(len(row1)):
        res_row.append(row1[i] - row2[i])
    return res_row


'''Agrega las variables basicas a la columna cero '''
def add_basic_variables(matrix, degrees_freedom, variables):
    row_basic_variable = 1
    
    for index_variables in range(degrees_freedom, len(variables)):
        if (variables[index_variables] != "excess" and variables[index_variables] != "x"):
            ''' lo almacenado en esa columna es cero, entonces le suma el numero de variable '''
            matrix[row_basic_variable][0] += index_variables 
            row_basic_variable += 1
        index_variables += 1
    return matrix


''' Extrae la solucion optima con un formato determinado para ser mostrado'''
def extract_optimal_solutions(optimal_solution_matrixes):
    optimal_solutions = []

    for matrix in optimal_solution_matrixes:
        len_matrix = len(matrix)
        columns = len(matrix[0])
        solution = []

        variables_amount = columns-2
        xn = [0] * (variables_amount+1)

        for row in range(1,len_matrix):
            basic_variable = matrix[row][0]
            right_side = matrix[row][columns-1]
            xn.pop(basic_variable)
            xn.insert(basic_variable, right_side)
        '''elimino el cero que sobra al inicio'''
        xn.pop(0) 
        solution.append(xn)
        U = matrix[0][columns-1]
        solution.append(U)
        optimal_solutions.append(solution)
    return optimal_solutions
