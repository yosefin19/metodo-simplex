import numpy as np



def primal_to_dual(matrix,vars,minmax):
    #se procede a transponer la matriz
    new_matrix = [] #matriz para retornar la matriz
    new_constraints = matrix[0][1:-2] #la fila 0 representa la funcion objetivo, estos valores seran el nuevo lado derecho de las restricciones
    values = [0] ##arreglo de la nueva funcion objetivo
    cons = [] ##se guardan los operadores de las restricciones 
    aux = matrix[1:] #se quita la fila 0 para iterar sobre las filas de restricciones unicamente
    aux1 = [] #se van a guardar los valores que van antes del operador <,>, = para hacer la transpuesta.
    for row in aux: #para cada restriccion:
        values.append(row[-1]) #el ultimo elemento de cada restriccion pasa a la NUEVA fila 0
        cons.append(row[-2]) # se agrega el operador de cada restriccion
        aux1.append(row[1:-2]) # se guardan los valores de cada variable de cada restriccion
    a = np.array(aux1) #se transpone la matriz de valores
    a = a.transpose()
    values.append(0) #se agregan los dos ceros del final de acuerdo al formato definido
    values.append(0)

    new_operators = [] 
    ####----------------------
    for i in vars: ##se realizan los cambios de acuerdo a la tabla de operadores
            if(minmax == 'min'):
                if(i == '=>'):
                    new_operators.append('<=')
                elif(i == '-'):
                    new_operators.append('=')
                elif(i == '<='):
                    new_operators.append('=>')
            else:
                if(i == '=>'):
                    new_operators.append('=>')
                elif(i == '-'):
                    new_operators.append('=')
                elif(i == '<='):
                    new_operators.append('<=')
     ####----------------------
    new_vars = []
    for i in cons:
        if(minmax == 'min'):
            if(i == '=>'):
                new_vars.append('=>')
            if(i == '='):
                new_vars.append('-')
            elif(i =='<='):
                new_vars.append('<=')
        else:
            if(i == '=>'):
                new_vars.append('<=')
            elif(i =='='):
                new_vars.append('-')
            elif(i =='<='):
                new_vars.append('=>')

    new_matrix.append(values) ##se crea cada nueva restriccion de acuerdo a la camtidad de variables
    for i in range(0,len(new_operators)):
        new_constraint = [0]
        for j in a[i]:
            new_constraint.append(j)
        new_constraint.append(new_operators[i])
        new_constraint.append(new_constraints[i])
        new_matrix.append(new_constraint)

    print('fila 0 nueva')
    print(values)
    print('columna ultima nueva:')
    print(new_constraints)
    print('transpuesta')
    print(a)
    print('operadores de variables nuevas')
    print(new_vars)
    print('operadores de restricciones nuevas')
    print(new_operators)


    print('MATRIX')
           
    ###Se debe utilizar Dos Fases o La Gran M
    print(new_matrix)

    ###OJO las soluciones se encuentran en la fila 0 de la ultima iteracion, hablar con las chiquillas


