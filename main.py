from ui_main_window import *
from add_variables import *
from big_m import *
from two_phase import *
from dual_method import *
import sys

matrix = []
method = ""
variables = 0
constraints = 0
bool_file =  False
option = ""
position = 0

def set_global():
    global method 
    method = application.get_method()
    global variables 
    variables = application.get_variables()
    global constraints 
    constraints = application.get_constraints()
    global bool_file 
    bool_file = application.get_bool_file()
    global option
    option = application.get_option()
    if option == "Maximizar":
        option = "max"
    elif option == "Minimizar" :
        option = "min"

def add_constrains():
    global position
    position =  application.add_constrains()+1
    application.pushButton2.clicked.connect(solve)



def solve():
    global matrix 
    matrix = application.solve()
    set_global()
    new_matrix = []
    global position
    
    if method == "Gran M":
        new_matrix , solution=  big_m(matrix, option)
    elif method == "Dual":
        vars = []
        for i in range(1, len(matrix)):
            vars.append(matrix[i][-2])
            print(vars)
        new_matrix , solution =  primal_to_dual(matrix, vars, option)
    elif method == "Dos Fases":
        new_matrix, solution =  two_phases_method(matrix,option)
    else:
        new_matrix, variables =  add_variables(matrix)
        simplex(new_matrix, variables)
    
    application.solution(new_matrix, solution, position)
    



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = ui_main_window()
    w = QtWidgets.QMainWindow()

    application.setup_ui(w)
    application.pushButton.clicked.connect(add_constrains)
    w.show()

    sys.exit(app.exec_())

