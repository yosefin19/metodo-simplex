from PyQt5 import QtCore, QtGui, QtWidgets

class monomial():
    def __init__(self,centralwidget):
        self.signo = QtWidgets.QComboBox(centralwidget)
        self.signo.addItem("+")
        self.signo.addItem("-")
        self.coefficient = QtWidgets.QLineEdit(centralwidget)
        self.literal = QtWidgets.QLabel(centralwidget)

class constrains():
    def __init__(self,centralwidget):
        self.monomials = []
        self.operator = QtWidgets.QComboBox(centralwidget)
        self.operator.addItem("<=")
        self.operator.addItem(">=")
        self.operator.addItem("=")
        self.value = monomial(centralwidget)
    
    def get_monomials(self):
        return self.monomials