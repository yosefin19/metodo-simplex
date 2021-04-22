import numpy as np
from simplex import simplex



test_matrix = [[0,0.4,0.5,0,0],[0,0.3,0.1,'<=',2.7],[0,0.5,0.5,'=',6],[0,0.6,0.4,'>=',6]]

test =[[0,2,3,4,0,0],[0,3,2,1,'<=',10],[0,2,3,3,'<=',15],[0,1,1,-1,'>=',4]]

def two_phases_method(matrix,minmax):
    original_u = matrix[0] ## se necesita la funcion objetivo original para la segunda fase
    vars_ = []
    variables = add_variables(matrix)
    #print(variables)
    for i in range(0,len(variables)):
        if(type(variables[i])==list):
            vars_.append(variables[i][0])
        else:
            vars_.append(variables[i])

    values = get_values(matrix)
    new_matrix = define_matrix_res(variables,matrix)
    final_matrix = operate_function(new_matrix,variables,values)
    #print_matrix(final_matrix)
    #print('------------------------------')
    matrix_first_phase = simplex(final_matrix,vars_)
    matrix_first_phase = matrix_first_phase[0]
    #print_matrix(matrix_first_phase)
    #print('------------------------------')
    final,sol = second_phase(matrix_first_phase,vars_,original_u,minmax)

    #print_matrix(final)
    #print(sol)
    return final,sol

    ###Hasta aca prepara la fase 1, se debe hacer simplex ahora
    ###se debe retornar la ultima iteracion para hacer la fase 2,  FALTA HACER FASE 2

def second_phase(matrix,variables,u_function,minmax):
    x = variables.count('x') ##cantidad de 'X'
    artificial_vars = variables.count('artificial') ##cantidad de artificiales
    total_variables = len(variables)-1
    other_variables = total_variables - artificial_vars - x ##
    u_function.pop()
    u_function.pop()
    for i in range(0,other_variables):
        u_function.append(0)
    u_function.append(0)
    aux_vars = variables
    aux=0
    final_vars = []
    for i in range(0,len(aux_vars)):
            if(variables[i]=='artificial'):
                for j in matrix:
                    #print(i-aux)
                    j.pop(i-aux)
                aux+=1
            else:
                final_vars.append(i)
    matrix.pop(0)
    matrix = [u_function] + matrix
    variables_second_phase = variables
    variables_second_phase = list(filter(lambda a: a != 'artificial', variables))
    matrix = operate_basic_variables(matrix,variables_second_phase)
    matrix_second_phase = simplex(matrix,variables_second_phase)
    basics = []
    for i in matrix:
        basics.append(i[0])
    basics = basics[1:]
    sol = solution(matrix_second_phase[0],variables,final_vars,basics,artificial_vars,minmax)

    return matrix_second_phase,sol


def solution(matrix,variables,final_vars,basic,artificials,minmax):
    vars = len(variables)-1 ##variables originales
    res = len(matrix)-1
    degrees = vars - res
    degrees -= artificials
    zeros = []
    for i in range(1,len(variables)):
        if(variables[i]=='artificial'):
            zeros.append(i)
  
    for i in range(degrees):
        for row in range(1,len(matrix[0])-1):
            if(exists(basic,row)==False):
                zeros.append(row)

    sol = []
    for i in range(vars):
        sol.append(0)
   
    aux = matrix[1:]
    for i in aux:
        sol[final_vars[i[0]]-1] = i[-1]

    u = matrix[0][-1]
    u *= -1
    sol = [sol] + [u]
    return sol
                
def exists(basic,value):
    for i in basic:
        if(i == value):
            return True
    else:
        return False
  
         

def get_values(matrix):
    values=[0]
    aux_matrix = matrix[1:]
    lent = len(aux_matrix[0])
    for row in aux_matrix:
        values.append(row[lent-1])
    return values

def add_variables(matrix):
    var = len(matrix[0])-3 #restar la columna 0 y la del signo y ultimo valor (-3)
    res = len(matrix) # cantidad de restricciones
    variables = [0] 
    for i in range(var): #vamos a iterar hasta agregar todas las variables X
        variables.append('x')
    #agregamos ahora las variables de holgura, exceso y artificiales
    col = len(matrix[0])-2 # indice columna de operadores para acceder a este facilmente
    for i in range(1,res):
        if (matrix[i][col]=='<='):
            variables.append(['slack',i])
        elif (matrix[i][col]=='='):
            variables.append(['artificial',i])
        elif (matrix[i][col]=='>='):
            variables.append(['excess',i])
            variables.append(['artificial',i])
    return variables


##no es relevante por el momento si es MAX o MIN,
#  ya que siempre se MINIMIZA en ambas fases
#def matrix_first_phase(test_matrix,variables,minmax):

#agregar a la matriz los valores de cada variable para cada restriccion: row: restricciones + 1 col: variables totales + 1
def define_matrix_res(variables,test_matrix):
    var = 0
    res = len(test_matrix)-1
    row = len(test_matrix)
    col = len(variables)
    for i in variables:
        if(type(i)!= list):
            if(i=='x'):
                var+=1 #cantidad de variables
        else:
            break
    new_matrix = []
    for i in range(row):
        new_row = []
        for j in range(col):
            new_row.append(0)
        new_matrix.append(new_row)
    for i in range(1,res+1):
        for j in range(1,var+1):
            new_matrix[i][j]=test_matrix[i][j]
    lent = len(variables)
    for i in range(var+1,lent):
            if(variables[i][0]=='slack' or variables[i][0]=='artificial'):
                new_matrix[variables[i][1]][i] = 1
                
            elif(variables[i][0]=='excess'):
                new_matrix[variables[i][1]][i] = -1
    return new_matrix


###operaciones gauss-jordan para eliminar las variables artificiales de la funcion objetivo
def operate_function(matrix,variables,values):
    lent = len(values)

    for i in range(0,lent):
        matrix[i].append(values[i])

    #print_matrix(matrix)
    vars = variables[1:]
    new_row = [0]
    for var in vars:
        if(var[0]=='artificial'):
            new_row.append(1)
        else:
            new_row.append(0)
    new_row.append(0)
    matrix[0] = new_row
    for var in vars:
        if(var[0]=='artificial'):
            lent = len(variables)
            for i in range(1,lent+1):
                matrix[0][i] += -1*matrix[var[1]][i]
    return add_variables_to_matrix(matrix,variables)


def operate_basic_variables(matrix,variables):
    #basic = []
    #print('0000000000000000000000000000000000000000')
    #print_matrix(matrix)
    #for i in matrix:
    #    basic.append(i[0])
    #basic = basic[1:] ##guardo variables basicas
    #print('bbbb' +str(basic))
    #basics = basic

    aux_matrix = matrix[1:] #dejo solo las restricciones
    for i in aux_matrix:
        basic = i[0] 
        if(matrix[0][basic]!=0):
            escalar = matrix[0][basic]
            for row in range(1,len(variables)+1):
                matrix[0][row] += -1*escalar*i[row]
    
    return matrix
            







def add_variables_to_matrix(matrix,variables):
    for i in range(0,len(variables)):
        if(type(variables[i])==list):
            if(variables[i][0]!='excess'):
                row = variables[i][1]
                matrix[row][0] = i
    return matrix

def print_matrix(matrix):
    for i in matrix:
        print(i)


two_phases_method(test,'max')

#test_matrix = [[0, -3, -5, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 4], [0, 0, 2, 0, 1, 0, 12], [0, 3, 2, 0, 0, 1, 18]] 
#var2 = [0, 'x', 'x', 'slack', 'slack','slack']

#matrix2 = [[0, -5, -2, 0, 0, 0],[3, 3, 1, 1, 0, 2],[4, 4, 2, 0, 1 ,2]]

#matrix3 = [[0, -2, -4, 0, 0, 0], [3, 1, 2, 1, 0, 5], [4, 1, 1, 0, 1, 4]]
#var = [0, 'x', 'x', 'slack', 'slack']

#m = [[0, -1.1, -0.9, 0, 0, 1, 0, -12],[3, 0.3, 0.1, 1, 0, 0, 0, 2.7],[4, 0.5, 0.5, 0, 1, 0, 0, 6],[6, 0.6, 0.4, 0, 0, -1, 1, 6]]
#v = [0, 'x', 'x','slack','artificial', 'excess', 'artificial']
    
#mat, sol = simplex(m, v)
#print(mat)