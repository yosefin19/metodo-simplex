import math
from copy import copy

def simplex(matrix):
    iteration = 1
    optima = False

    while not optima:
        if optimo(matrix) == True:
            optima = True
        else:
            coefficients = [] #-----------------no es necesario declarar esto primero
            #--------------aqui llama a is_unbounded(), hay que terminar programa y lanzar resultado de U no acotada si lo es
            row, column, number, coefficients = pivot(matrix)            
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
            iteration += 1
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
def pivot(matrix):
    coefficients = []
    lenm = len(matrix)
    lenc = len(matrix[0])
    value = 0
    column = 0
    for i in range(1, lenc):
        if matrix[0][i] < value:
            value = matrix[0][i]
            column = i

    min = float(1 << 61)
    row = 0
    for i in range (1, lenm):
        if(matrix[i][column] <= 0):
            continue
        #-------------------si hace un continue me parece que el else no hace falta 
        else:
            x = matrix[i][lenc-1]/matrix[i][column]
            coefficients.append(x)
            if(min>x):
                min = x
                row = i

    return row, column, matrix[row][column], coefficients


#Revisa si existe numeros negativos en la fila de U
def optimo(matrix):
    mini = min(matrix[0])
    if mini < 0 :
        return False
    else:
        return True

def main():

    test_matrix = [[0, 3, 5, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 4], [0, 0, 2, 0, 1, 0, 12], [0, 3, 2, 0, 0, 1, 18]] 
    
    matrix2 = [[0, -5, -2, 0, 0, 0],[3, 3, 1, 1, 0, 2],[4, 4, 2, 0, 1 ,2]]
    
    matrix3 = [[0, -3, -5, 0, 0, 0, 0],[3, 1, 0, 1,0, 0 , 4],[4, 0, 2, 0, 1, 0 ,12],[5, 3, 2,0, 0, 1, 18]]
    
    simplex(matrix2)

main()