import sys
"""
Modo claro: sección de strings donde se contengan los colores usados para este modo, y que en el guardado se mantenga, así igual con el modo oscuro
Selección de colores: una serie de códigos de color que se implementarán en función del seleccionado por el usuario, y se actualizarán como tal
TODOS los datos de configuración se guardarán el selfs clave de donde el sistema tomará la información y actualizará la UI acorde a las selecciones
Al momento de guardar la información, el sistema primero duplicará la carpeta previa de configuración y luego intentará guardar la info en la
carpeta original, pero si algo falla se volverá a los datos por defecto por medio de la carpeta duplicada.
Para el idioma, se almacenará en una serie de strings la información elegida, y se usará booleano para determinar si es español (True) o inglés (False)
Se usarán botones y no entradas de texto para simplificar la selección de datos.
Para el nombre de usuario se podrá escribir texto, que no sea ni NULO ni de un largo superior a 40 caracteres.
El guardado se hará en JSON con el fin de conservar los tipos de valor almacenados.

"""
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit)
from PyQt6.QtGui import QGuiApplication

class Sistema(QMainWindow):
    def __init__(self):
        super().__init__()

        # datos del cosito de PyQt
        self.setWindowTitle("Config Simulator")
        p = QGuiApplication.primaryScreen().geometry()
        x = 2*(p.width())//11
        y = (p.height())//6
        self.setGeometry(x, y, 600, 400)

        # inicialización del contenedor
        self.contenedor = QStackedWidget()
        self.setCentralWidget(self.contenedor)

        #Barrita superior
        self.menu = self.menuBar()
        self.m_archivo = self.menu.addMenu("Archivo")
        self.m_edits = self.menu.addMenu("Edición")
        self.m_ver = self.menu.addMenu("Ver")
        self.m_settings = self.menu.addMenu("Configuración")


        # --- DATOS EDITABLES POR EL USUARIO ---
        # tema de la app
        self.tema_select = "claro"
        self.tema_config = {"claro": {"u"}, "oscuro":{"a"}}
        self.tema = self.tema_config[self.tema_select]
        

        # nombre usuario
        self.username = None

        # idioma
        self.idioma = None

        # fuente
        self.f_tamano = 12
        self.f_color = "#000000"

        #barra menú
        self.m_color = "#777777"


    def settings_page(self): pass


app = QApplication(sys.argv)
system = Sistema()
system.show()
sys.exit(app.exec())