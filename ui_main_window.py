from PyQt5 import QtCore, QtGui, QtWidgets


class ui_main_window(object): 

    matrix = []

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
            #label method
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setText("Metodo: ")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        
            #methods
        self.method = QtWidgets.QComboBox(self.centralwidget)
        self.method.setObjectName("method")
        self.method.addItem("")
        self.method.setItemText(0, "Gran M")
        self.method.addItem("")
        self.method.setItemText(1, "Dual")
        self.gridLayout.addWidget(self.method, 0, 1, 1, 1)
        
            #check file
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setText("Generar Archivo")
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 2, 1, 1)

            #text constraints
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setText("Restricciones")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        
            #add number constraints
        self.constraints = QtWidgets.QLineEdit(self.centralwidget)
        self.constraints.setObjectName("constraints")
        self.gridLayout.addWidget(self.constraints, 1, 1, 1, 1)
        
            #options
        self.options = QtWidgets.QComboBox(self.centralwidget)
        self.options.setObjectName("options")
        self.options.addItem("")
        self.options.setItemText(0, "Maximizar")
        self.options.addItem("")
        self.options.setItemText(1, "Minimizar")
        self.gridLayout.addWidget(self.options, 1, 2, 1, 1)
            
            #text variables
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("Variables")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        
            #add number variables
        self.variables = QtWidgets.QLineEdit(self.centralwidget)
        self.variables.setObjectName("variables")
        self.gridLayout.addWidget(self.variables, 2, 1, 1, 1)
            
            #button 
        self.pushButton = QtWidgets.QToolButton(self.centralwidget)
        self.pushButton.setText("Agregar constraints")
        self.pushButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget) 
        
    
    def get_method(self):
        return self.method.currentText()
    
    def get_option(self):
        return self.options.currentText()
    
    def get_bool_file(self):
        return self.checkBox.isChecked()

    def get_constraints(self):
        return int(self.constraints.text())

    def get_variables(self):  
        return int(self.variables.text())
    
    def get_matrix(self):
        return self.matrix

    def add_constrains(self):
        constraints = self.get_constraints()
        variables = self.get_variables()
        #U
        self.variable = QtWidgets.QLabel(self.centralwidget)
        self.variable.setObjectName("u")
        self.variable.setText("U")
        self.gridLayout.addWidget(self.variable, 5 , 0 , 1, 1)

        self.variable = QtWidgets.QLabel(self.centralwidget)
        self.variable.setObjectName("=")
        self.variable.setText("=")
        self.gridLayout.addWidget(self.variable, 5 , 1 , 1, 1)

        combo = "combo5_0"
        self.combo = QtWidgets.QComboBox(self.centralwidget)
        self.combo.setObjectName(combo)
        self.combo.addItem("+")
        self.combo.addItem("-")
        self.gridLayout.addWidget(self.combo, 5 , 2, 1, 1)

        var = 1  
        column = 3
        for u in range (1, variables+1):
            name = "U" + str(u) 
            self.name = QtWidgets.QLineEdit(self.centralwidget)
            self.name.setObjectName(name)
            self.gridLayout.addWidget(self.name, 5 , column, 1, 1)
            column += 1
            variable = "x" + str(u) 
            self.variable = QtWidgets.QLabel(self.centralwidget)
            self.variable.setObjectName("variable")
            self.variable.setText(variable)
            self.gridLayout.addWidget(self.variable, 5 , column , 1, 1)
            column += 1
            if var == variables:
                continue
            else:
                combo = "combo" + str(5) + "_" + str(u)  
                self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
                self.comboBox_4.setObjectName("comboBox")
                self.comboBox_4.addItem("+")
                self.comboBox_4.addItem("-")
                self.gridLayout.addWidget(self.comboBox_4, 5 , column, 1, 1)
                column += 1
                var += 1     

        row = 6

        #constraints
        for i in range (1, constraints+1):

            combo = "combo" + str(i) + "_" + "0" 
            self.combo = QtWidgets.QComboBox(self.centralwidget)
            self.combo.setObjectName(combo)
            self.combo.addItem("+")
            self.combo.addItem("-")
            self.gridLayout.addWidget(self.combo, row , 0, 1, 1)

            x = 1
            column = 1
            for j in range (1, variables+1):
                name = "dato" + str(i) + "_" + str(j) 
                self.name = QtWidgets.QLineEdit(self.centralwidget)
                self.name.setObjectName(name)
                self.gridLayout.addWidget(self.name, row , column, 1, 1)

                column += 1
                variable = "x" + str(j) 
                self.variable = QtWidgets.QLabel(self.centralwidget)
                self.variable.setObjectName(variable)
                self.variable.setText(variable)
                self.gridLayout.addWidget(self.variable, row , column , 1, 1)
                column += 1
                if x == variables:
                    continue
                else:
                    combo = "combo" + str(i) + "_" + str(j) 
                    self.combo = QtWidgets.QComboBox(self.centralwidget)
                    self.combo.setObjectName(combo)
                    self.combo.addItem("+")
                    self.combo.addItem("-")
                    self.gridLayout.addWidget(self.combo, row , column, 1, 1)

                    column += 1
                x += 1
            combo = "combo" + str(i) + "_" + str(j) 
            self.combo = QtWidgets.QComboBox(self.centralwidget)
            self.combo.setObjectName(combo)
            self.combo.addItem(">")
            self.combo.addItem("<")
            self.combo.addItem("=")
            self.gridLayout.addWidget(self.combo, row , column, 1,  1)
            column += 1
            
            combo = "combo" + str(i) + "_" + str(j)
            self.combo = QtWidgets.QComboBox(self.centralwidget)
            self.combo.setObjectName(combo)
            self.combo.addItem("+")
            self.combo.addItem("-")
            self.gridLayout.addWidget(self.combo, row , column, 1, 1)
            column += 1

            name = "dato" + str(i) + "_" + str(j) 
            self.name = QtWidgets.QLineEdit(self.centralwidget)
            self.name.setObjectName(name)
            self.gridLayout.addWidget(self.name, row, column, 1, 1)
            row +=1

        self.pushButton2 = QtWidgets.QToolButton(self.centralwidget)
        self.pushButton2.setText("Resolver")
        self.pushButton2.setObjectName("toolButton")
        self.gridLayout.addWidget(self.pushButton2, row, 1, 1, 1)        


 


        

