import sympy as sym
import math
from common import *
from copy import copy

M = sym.Symbol('M')
''' 0 si no es degenerada, 1 si lo es '''
degenerate = 0

'''
Funcion principal del metodo simplex que maneja si la solucion es optima y si es multiple
Se tiene un arreglo de solucion por la posibilidad de soluciones multiples
'''
def simplex(matrix, variables):
    global degenerate
    degenerate = False
    solution = []
    iteration = 1
    optimal = False
    new_matrix = copy(matrix)
    #Agrego al archivo la solucion inicial
    write_initial(matrix)
    
    #Se itera hasta que la solucion sea optima 
    while not optimal:
        
        #Si la solucion es optima, se verifica si es multiple, en ambos casos se agrega la solucion y se retorna 
        if optimal_solution(new_matrix, variables): 
            multi, pivot_second_optimal_solution = multiple_solutions(new_matrix, variables)
            if multi:
                #Se agrega la solucion optima al lista de soluciones
                solution.append(new_matrix) 
                #Se escriba la nueva iteracion
                write_iteration(iteration)    
                #Se agrega la solucion extra a la lista de soluciones           
                solution.append(simplex_aux(new_matrix,pivot_second_optimal_solution))
                optimal = True
                return solution
            else:
                optimal = True
                #Se agrega la solucion a la lista de soluciones 
                solution.append(new_matrix)
                return solution
        #Si la solucion no es optima se verifica si es acotada, de no serlo se realiza una nueva iteracion del metodo simplex 
        else:
            #Si la solucion es acotada se termina el procedimiento y se retorna la matriz 
            if is_unbounded(new_matrix):
                write_unbounded(new_matrix)
                return solution
            else:
                #Se escriba la nueva iteracion
                write_iteration(iteration)
                #Se procede a la nueva iteracion del simplex
                new_matrix = simplex_aux(new_matrix)
                iteration += 1
    
                   
'''
Funcion auxiliar del metodo simplex que inicialmente calcula el numero pivote, la columna y la fila apartir de la funcion pivot
Luego se realizan las modificaciones en la tabla con las operaciones necesarias
Por ultimo, se agregan la tabla con los cambios en el archivo si este es solicitado
En caso de existir multiples soluciones se utiliza un segundo parametro opcional para indicar la columna pivot de la segunda solucion
'''   
def simplex_aux(matrix, pivot_second_optimal_solution = 0):
    row, column, number = pivot(matrix, pivot_second_optimal_solution)   
    #print(row, column, number)  
           
    #dividir la fila del pivot entre el pivot
    for i in range(1,len(matrix[1])):
        if matrix[row][i]!=0:
            '''matrix[row][i] = float("{0:.3f}".format(matrix[row][i]/number)) devolver'''
            matrix[row][i] = matrix[row][i]/number
    #Transformacion de la matriz
    for i in range(0, len(matrix)):
        if i != row:
            auxmat = matrix[i]
            matrix[i] = subtract_row(auxmat, multiply_row(matrix[row], matrix[i][column]))
    old = matrix[row][0],
    #Cambio de las Variablas Basicas
    matrix[row][0] = column
    #Escritura en archivo
    write_simplex(matrix, old, column, number)
    #Mostrar el progreso en consola
    #print_solution(matrix, matrix[row][0], column, number)

    return matrix


'''
Funcion que calcula el numero de fila, columna y el numero pivot
En caso de existir multiples soluciones se utiliza un segundo parametro para indicar la columna pivot
'''
def pivot(matrix, pivot_second_optimal_solution):
    len_m = len(matrix)
    len_c = len(matrix[0])-1
    value = 0
    column = -1
    coefficients = []
    coefficients_aux = []
    #Se verifica si es el pivote de una solucion multiple
    if pivot_second_optimal_solution>0:
        column = pivot_second_optimal_solution
    else:
        column = get_pivot_column(matrix)
    #Se inicializa el minimo con un numero pequeno                
    mini = float(1 << 61)
    row = 0
    #Se calculan los coeficientes de los valores mayores a 0, se toma el menor junto a la fila al que pertenece
    for i in range (1, len_m):
        if(matrix[i][column] <= 0):
            continue
        else:
            ''' x = float("{0:.4f}".format(matrix[i][len_c]/matrix[i][column])) devolver'''
            x = float(matrix[i][len_c]/matrix[i][column])
            coefficients.append(x)
            coefficients_aux.append([i,matrix[i][column]])
            if(mini>x):
                mini = x
                row = i
    degenerate_row = is_degenerate(coefficients, coefficients_aux)
    if (degenerate == 1):
        row = degenerate_row
    #Se retorna la fila, columna y numero pivote
    return row, column, matrix[row][column]


'''Imprime la solucion en consola '''
def print_solution(matrix, old, new, number):
    print("Matriz: \n")
    for i in range(0, len(matrix)):
        print(matrix[i] , "\n")
   
    print("VB Entrante:", new, "\n")
    print("VB Saliente:", old, "\n")
    print("Numero pivot:", number, "\n")
    if (degenerate == 1):
        print("Solucion degenerada:\n")
    else:
        print("Solucion:\n")
    sol = [0]*(len(matrix[0])-2)
    for i in range(1,len(matrix)):
        index = matrix[i][0] -1
        sol[index] = matrix[i][-1]
    print(sol)
    print("U: ", matrix[0][-1])



'''
Verifica si la solucion actual es la optima, utiliza el conjunto de variables para asegurar que verifique estrictamente las que se deben
'''
def optimal_solution(matrix, variables):
    zero_row = change_m_row(matrix[0])
    zero_row.pop()
    minimum = min(zero_row)
    if minimum < 0 :
        return False
    else:
        return True

'''
Verifica si la solucion optima actual es multiple, utiliza el conjunto 
de variables para asegurar que verifique estrictamente las que se deben
'''
def multiple_solutions(matrix, variables):
    len_c = len(matrix[0])
    basic_variables = get_basic_variables(matrix)

    for column in range(1,len_c):
        if (matrix[0][column] == 0 and basic_variables[column] != 'basic'):
            return True, column
    return False, 0


''' Retorna un arreglo que indica las variables básicas '''
def get_basic_variables(matrix):
    len_c = len(matrix[0])
    len_matrix = len(matrix)
    basic_variables = [' '] * (len_c-1)
    for row in range(1,len_matrix):
        basic_variable = matrix[row][0]
        basic_variables.pop(basic_variable)
        basic_variables.insert(basic_variable, 'basic')
    return basic_variables


''' Determina si una solución es degenerada '''
def is_degenerate(coefficients, coefficients_aux):
    len_coefficients = len(coefficients)
    global degenerate

    mini = min(coefficients)
    indexes = [i for i, x in enumerate(coefficients) if x == mini]

    len_indexes = len(indexes)
    if (len_indexes == 1):
        degenerate = 0
        return coefficients_aux[indexes[0]][0]
    degenerate = 1
    max_divider = coefficients_aux[indexes[0]][1]
    pivot_row = coefficients_aux[indexes[0]][0]
    for i in range(1,len_indexes):
        temp = coefficients_aux[indexes[i]][1]
        if (temp > max_divider):
            max_divider = temp
            pivot_row = coefficients_aux[indexes[i]][0]
    return pivot_row


'''
Escribe en el archivo de texto la solucion inicial
'''
def write_initial(matrix):
    archivo = open('Solucion.txt','w') 
    #archivo = open('Solucion')
    archivo.write('Iteracion 0 \n')
    archivo.write("Matriz: \n")
    for i in range(0, len(matrix)):
        archivo.write(str(matrix[i]))
        archivo.write("\n")
    archivo.write("Solucion Inicial:\n")
    sol = [0]*(len(matrix[0])-2)
    for i in range(1,len(matrix)):
        index = matrix[i][0] -1
        sol[index] = matrix[i][-1]
    archivo.write(str(sol))
    archivo.write("\n")
    archivo.write("U: ") 
    archivo.write(str(matrix[0][-1]))
    archivo.write("\n\n")
    archivo.close()

'''
Escribe en el archivo de texto la solucion acotada
'''
def write_unbounded(matrix):
    file = open('Solucion.txt','w') 
    #archivo = open('Solucion')
    file.write('Iteracion 0 \n')
    file.write("Matriz: \n")
    for i in range(0, len(matrix)):
        file.write(str(matrix[i]))
        file.write("\n")
    file.write("Solucion acotada:\n")
    sol = [0]*(len(matrix[0])-2)
    for i in range(1,len(matrix)):
        index = matrix[i][0] -1
        sol[index] = matrix[i][-1]
    file.write(str(sol))
    file.write("\n")
    file.write("U: ") 
    file.write(str(matrix[0][-1]))
    file.write("\n\n")
    file.close()


'''
Escribe en el archivo de texto el numerode iteracion
'''
def write_iteration(num):
    file = open('Solucion.txt','a')
    file.write("Iteracion")
    file.write(str(num))
    file.write("\n")
    file.close()

'''
Escribe en el archivo de texto la matriz actual y su solucion
'''
def write_simplex(matrix, old, new, number):
    file = open('Solucion.txt', 'a')

    file.write("Matriz: \n")
    for i in range(0, len(matrix)):
        file.write(str(matrix[i]))
        file.write("\n")
   
    file.write("VB Entrante:")
    file.write(str(new))
    file.write("\n")
    file.write("VB Saliente:")
    file.write(str(old))
    file.write("\n")
    file.write("Numero pivot:")
    file.write(str(number))
    file.write("\n")
    if (degenerate == 1):
        file.write("Solucion degenerada:\n")
    else:
        file.write("Solucion:\n")
    sol = [0]*(len(matrix[0])-2)
    for i in range(1,len(matrix)):
        index = matrix[i][0] -1
        sol[index] = matrix[i][-1]
    file.write(str(sol))
    file.write("\n")
    file.write("U: ")
    file.write(str(matrix[0][-1]))

    file.write("\n\n")
    file.close()
