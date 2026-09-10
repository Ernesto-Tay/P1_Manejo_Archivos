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

class Sistema(QMainWindow):
    def __init__(self):
        super().__init__()
        # Fondo de la app
        self.contenedor = QWidget()
        self.SetCentralWidget(self.contenedor)

        #Barrita superior
        self.menu = self.menuBar()
        