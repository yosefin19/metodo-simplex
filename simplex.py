import math
from copy import copy

'''
Funcion principal del metodo simplex que maneja si la solucion es optima y si es multiple
'''
def simplex(matrix, variables):
    solution = []
    iteration = 1
    optima = False
    new_matrix = copy(matrix)
    #Agrego al archivo la solucion inicial
    write_initial(matrix)
    #Se itera hasta que la solucion sea optima
    while not optima:
        write_iteration(iteration)
        #Si la solucion es optima, se verifica si es multiple, en ambos casos se agrega la solucion y se retorna
        if optimo(new_matrix):
            multi, piv = multiple(new_matrix, variables)
            if multi:
                solution.append(new_matrix)                
                solution.append(simplex_aux(new_matrix,piv))
                optima = True
                return solution
            else:
                optima = True
                solution.append(new_matrix)
                return solution
        #Si la solucion no es optima se realiza una nueva iteracion del metodo simplex
        else:
            new_matrix = simplex_aux(new_matrix)
            iteration += 1
                   
'''
Funcion auxiliar del metodo simplex que 
'''   
def simplex_aux(matrix, pivote = 0):
    coefficients = []
    row, column, number, coefficients = pivot(matrix, pivote)            
    #dividir la fila del pivot entre el pivot
    for i in range(1,len(matrix[1])):
        if matrix[row][i]!=0:
            matrix[row][i] = matrix[row][i]/number
    for i in range(0, len(matrix)):
        if i != row:
            auxmat = matrix[i]
            matrix[i] = subtract_row(auxmat, multiply_row(matrix[row], matrix[i][column]))
        #variables[row] = column
        matrix[row][0] = column
    write_simplex(matrix, row, column, number)
    print_solution(matrix, row, column, number)
    return matrix

def print_solution(matrix, row, saliente, number):
    print("Matriz: \n")
    for i in range(0, len(matrix)):
        print(matrix[i] , "\n")
   
    print("VB Entrante:", saliente, "\n")
    print("VB Saliente:", row, "\n")
    print("Numero pivot:", number, "\n")
    print("Solucion:\n")
    sol = [0]*(len(matrix[0])-2)
    for i in range(1,len(matrix)):
        index = matrix[i][0] -1
        sol[index] = matrix[i][-1]
    print(sol)
    print("U: ", matrix[0][-1])

def multiply_row(row, escalar):
    n_row = []
    n_row.append(row[0])
    for i in range(1,len(row)):
        n_row.append(row[i]*escalar)
    return n_row


def subtract_row(row, row2):
    n_row = []
    n_row.append(row[0])
    for i in range(1,len(row)):
        n_row.append(row[i]-row2[i])
    
    return n_row

#retorna el numero de fila y columna, y el numero pivot
def pivot(matrix, pivot):
    coefficients = []
    lenm = len(matrix)
    lenc = len(matrix[0])
    value = 0
    column = 0
    if pivot>0:
        column = pivot
    else:
        for i in range(1, lenc):
            if matrix[0][i] < value:
                value = matrix[0][i]
                column = i

    min = float(1 << 61)
    row = 0
    for i in range (1, lenm):
        if(matrix[i][column] <= 0):
            continue
        else:
            x = matrix[i][lenc-1]/matrix[i][column]
            coefficients.append(x)
            if(min>x):
                min = x
                row = i

    return row, column, matrix[row][column], coefficients


#Revisa si existe numeros negativos en la fila de U para saber si es optima
def optimo(matrix):
    mini = min(matrix[0])
    if mini < 0 :
        return False
    else:
        return True

#Revisa si existe numeros negativos en la fila de U
def multiple(matrix, variables):
    for i in range(1, len(matrix[0])-1):
        if variables[i]!= 'slack':
            if matrix[0][i] == 0:
                return True, i
    return False, 0

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


def write_iteration(num):
    archivo = open('Solucion.txt','a')
    archivo.write("Iteracion")
    archivo.write(str(num))
    archivo.write("\n")
    archivo.close()

def write_simplex(matrix, row, saliente, number):
    archivo = open('Solucion.txt', 'a')

    archivo.write("Matriz: \n")
    for i in range(0, len(matrix)):
        archivo.write(str(matrix[i]))
        archivo.write("\n")
   
    archivo.write("VB Entrante:")
    archivo.write(str(saliente))
    archivo.write("\n")
    archivo.write("VB Saliente:")
    archivo.write(str(row))
    archivo.write("\n")
    archivo.write("Numero pivot:")
    archivo.write(str(number))
    archivo.write("\n")
    archivo.write("Solucion:\n")
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

def main():

    test_matrix = [[0, -3, -5, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 4], [0, 0, 2, 0, 1, 0, 12], [0, 3, 2, 0, 0, 1, 18]] 
    var2 = [0, 'x', 'x', 'slack', 'slack','slack']

    matrix2 = [[0, -5, -2, 0, 0, 0],[3, 3, 1, 1, 0, 2],[4, 4, 2, 0, 1 ,2]]

    matrix3 = [[0, -2, -4, 0, 0, 0], [3, 1, 2, 1, 0, 5], [4, 1, 1, 0, 1, 4]]
    var = [0, 'x', 'x', 'slack', 'slack']

    simplex(test_matrix, var2)
    #simplex(matrix3, var)

main()