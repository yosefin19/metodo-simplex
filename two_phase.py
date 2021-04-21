import numpy as np



test_matrix = [[0,0.4,0.5,0,0],[0,0.3,0.1,'<=',2.7],[0,0.5,0.5,'=',6],[0,0.6,0.4,'>=',6]]

def two_phases_method(matrix,minmax):
    vars_ = []
    variables = add_variables(matrix)
    for i in range(0,len(variables)):
        if(type(variables[i])==list):
            if(variables[i][0]!='excess'):
                vars_.append(variables[i][0])
        else:
            vars_.append(variables[i])

    values = get_values(matrix)
    new_matrix = define_matrix_res(variables,matrix)
    final_matrix = operate_function(new_matrix,variables,values)
    print(vars_)
    print_matrix(final_matrix)

    ###Hasta aca prepara la fase 1, se debe hacer simplex ahora

    ###se debe retornar la ultima iteracion para hacer la fase 2,  FALTA HACER FASE 2

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


two_phases_method(test_matrix,'max')

