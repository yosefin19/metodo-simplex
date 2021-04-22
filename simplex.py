import sympy as sym
import math
from common import *
from copy import copy

M = sym.Symbol('M')

'''
Funcion principal del metodo simplex que maneja si la solucion es optima y si es multiple
Se tiene un arreglo de solucion por la posibilidad de soluciones multiples
'''
def simplex(matrix, variables):
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
                #print("acotada")
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
    #Escritura en archivo
    write_simplex(matrix, matrix[row][0], column, number)
    #Mostrar el progreso en consola
    #print_solution(matrix, matrix[row][0], column, number)
    #Cambio de las Variablas Basicas
    matrix[row][0] = column
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
    #Se verifica si es el pivote de una solucion multiple
    if pivot_second_optimal_solution>0:
        column = pivot_second_optimal_solution
    else:
        column = get_pivot_column(matrix)
        '''
        #Se busca el nuevo pivote
        for i in range(1, len_c):
            #Si el valor en la matriz es menor al guardado anteriormente se cambia y se guarda el numero de columna
            temp = change_m_value(matrix[0][i]) #hay que hacer lo mismo que en columna pivot o usar columna pivot
            if matrix[0][i] < value:
                value = matrix[0][i]
                column = i
        '''
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
            if(mini>x):
                mini = x
                row = i
    #Se retorna la fila, columna y numero pivote
    return row, column, matrix[row][column]



def print_solution(matrix, old, new, number):
    print("Matriz: \n")
    for i in range(0, len(matrix)):
        print(matrix[i] , "\n")
   
    print("VB Entrante:", new, "\n")
    print("VB Saliente:", old, "\n")
    print("Numero pivot:", number, "\n")
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
Verifica si la solucion optima actual es multiple, utiliza el conjunto de variables para asegurar que verifique estrictamente las que se deben
'''
def multiple_solutions(matrix, variables):
    x = variables.count('x') + 2
    for i in range(x, len(matrix[0])-1):
        if matrix[0][i] == 0:
            return True, i
    return False, 0

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



'''
Pruebas
'''
#def main():

 #   test_matrix = [[0, -3, -5, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 4], [0, 0, 2, 0, 1, 0, 12], [0, 3, 2, 0, 0, 1, 18]] 
  #  var2 = [0, 'x', 'x', 'slack', 'slack','slack']

   # matrix2 = [[0, -5, -2, 0, 0, 0],[3, 3, 1, 1, 0, 2],[4, 4, 2, 0, 1 ,2]]

    #matrix3 = [[0, -2, -4, 0, 0, 0], [3, 1, 2, 1, 0, 5], [4, 1, 1, 0, 1, 4]] var = [0, 'x', 'x', 'slack', 'slack']

  #  m = [[0, -1.1, -0.9, 0, 0, 1, 0, -12],[3, 0.3, 0.1, 1, 0, 0, 0, 2.7],[4, 0.5, 0.5, 0, 1, 0, 0, 6],[6, 0.6, 0.4, 0, 0, -1, 1, 6]]
   # v = [0, 'x', 'x','slack','artificial', 'excess', 'artificial']
    
    #mat, sol = simplex(m, v)
    #print("--------------------")
    #print(mat)
    #simplex(test_matrix, var2)
    #simplex(matrix3, var)

#main()