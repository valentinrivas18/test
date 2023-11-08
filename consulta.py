import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QTextBrowser, QTableView
import psycopg2
from PyQt5.QtGui import QStandardItemModel

# Conexión a la base de datos PostgreSQL

conn = psycopg2.connect(
host="localhost",
database="postgres",
user="postgres",
password="valentin"
)
# Función para insertar un subproyecto en la base de datos
def insertar_subproyecto(semestre, nombre_subproyecto):
    try:
        cursor = conn.cursor()
        query = f"INSERT INTO {semestre} (nombre_subproyecto) VALUES (%s)"
        cursor.execute(query, (nombre_subproyecto,))
        conn.commit()
        cursor.close()
        print("Subproyecto insertado correctamente.")
    except (Exception, psycopg2.Error) as error:
        print("Error al insertar el subproyecto:", error)

# Función para consultar la tabla del semestre seleccionado
def consultar_tabla(semestre):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id_subproyecto, nombre_subproyecto FROM {semestre}")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al consultar la tabla:", error)
        return []

# Clase principal de la interfaz gráfica
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Añadir y Consultar Subproyectos")
        self.setGeometry(42, 65, 800, 600)

        self.label_semestre = QLabel("Semestre:", self)
        self.input_semestre = QLineEdit(self)
        self.label_subproyecto = QLabel("Nombre Subproyecto:", self)
        self.input_subproyecto = QLineEdit(self)
        self.btn_insertar = QPushButton("Insertar", self)
        self.btn_insertar.clicked.connect(self.insertar_subproyecto)



        self.combo_semestre = QComboBox(self)
        self.combo_semestre.addItem("semestre_1")
        self.combo_semestre.addItem("semestre_2")
        self.combo_semestre.addItem("semestre_3")
        self.combo_semestre.addItem("semestre_4")
        self.combo_semestre.addItem("semestre_5")
        self.combo_semestre.addItem("semestre_6")
        self.combo_semestre.addItem("semestre_7")
        self.combo_semestre.addItem("semestre_8")
        self.combo_semestre.addItem("semestre_9")

        self.btn_consultar = QPushButton("Consultar Tabla", self)
        self.btn_consultar.clicked.connect(self.mostrar_tabla)

        self.label_resultado = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.label_semestre)
        layout.addWidget(self.input_semestre)
        layout.addWidget(self.label_subproyecto)
        layout.addWidget(self.input_subproyecto)
        layout.addWidget(self.btn_insertar)
        layout.addWidget(self.combo_semestre)
        layout.addWidget(self.btn_consultar)
        layout.addWidget(self.label_resultado)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def insertar_subproyecto(self):
        semestre = self.input_semestre.text()
        nombre_subproyecto = self.input_subproyecto.text()

        if semestre and nombre_subproyecto:
            insertar_subproyecto(semestre, nombre_subproyecto)
            self.input_semestre.setText("")
            self.input_subproyecto.setText("")
        else:
            print("Debes ingresar el semestre y el nombre del subproyecto.")

    def mostrar_tabla(self):
        semestre = self.combo_semestre.currentText()
        data = consultar_tabla(semestre)

        resultado = "ID\t\tNombre del Subproyecto\n"
        resultado += "------------------------------------------\n"
        for row in data:
            resultado += f"{row[0]}\t\t{row[1]}\n"

        self.label_resultado.setText(resultado)

# Código de ejecución principal
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())