from ui_main_window import *
import sys

matrix = []
method = ""
variables = 0
constraints = 0
bool_file =  False
option = ""

def set_global():
    global matrix 
    matrix = application.get_matrix()
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

def add_constrains():
    application.add_constrains()
    application.pushButton2.clicked.connect(solve) 


def solve():
    application.solve()
    set_global()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = ui_main_window()
    w = QtWidgets.QMainWindow()

    application.setup_ui(w)
    application.pushButton.clicked.connect(add_constrains)
    w.show()

    sys.exit(app.exec_())


