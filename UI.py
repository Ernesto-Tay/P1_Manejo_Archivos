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
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QFileDialog)
from PyQt6.QtGui import QGuiApplication, QAction, QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt

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

        # Asignación de distintas pestañas en función de la opción del menú elegida
        self.contenedor.addWidget(self.archivo_page())
        self.contenedor.addWidget(self.edicion_page())
        self.contenedor.addWidget(self.ver_page())
        self.contenedor.addWidget(settings_p)

        #Barrita superior
        self.menu = self.menuBar()


        # --- BOTONES Y ACCIONES ---
        self.m_archivo = QAction("Archivo", self)
        self.m_archivo.triggered.connect(self.contenedor.setCurrentIndex[0])
        self.menu.addAction(self.m_archivo)

        self.m_edits = QAction("Edición", self)
        self.m_edits.triggered.connect(self.contenedor.setCurrentIndex[1])
        self.menu.addAction(self.m_edits)

        self.m_ver = QAction("Ver", self)
        self.m_ver.triggered.connect(self.contenedor.setCurrentIndex[2])
        self.menu.addAction(self.m_ver)

        self.m_settings = QAction("Configuración", self)
        self.m_settings.triggered.connect(self.contenedor.setCurrentIndex[3])
        self.menu.addAction(self.m_settings)


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

    def color_upd(self): pass
    def user_upd(self): pass
    def idioma_upd(self): pass
    def f_tamano_upd(self): pass
    def f_color_upd(self): pass
    def m_color_upd(self): pass

    def archivo_page(self): pass
    def edicion_page(self): pass
    def ver_page(self): pass


class settings_p(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # SECCIÓN DEL PERFIL
        perfil = QHBoxLayout()
        layout.addWidget(perfil)

        # IZQUIERDA - foto de perfil y selector de esta
        foto_layout = QVBoxLayout()
        self.foto_shaper = ImagenPerfil()
        self.foto_archivo = SubidorArchivos()
        foto_layout.addWidget(self.foto_shaper)
        foto_layout.addWidget(self.foto_archivo)

        p_userData = QVBoxLayout()
        p_userData.addWidget(QLabel("Nombre de usuario"))
        self.nombre_user = QLabel("wasa")
        nombre_upd = QPushButton("Cambiar Nombre")
        nombre_upd.clicked.connect(self.cambianombre)

    def cambianombre(self):
        nom_upd = QLineEdit("Ingrese nuevo nombre...")
        nom_upd.returnPressed.connect(self.nom_upd)

    def nom_upd(self, newName):
        self.nombre_user = QLabel(str(newName).strip())


class SubidorArchivos(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Texto debajo
        self.t_perfil = QLabel("Cambiar foto de perfil")
        layout.addWidget(self.t_perfil)

        boton = QPushButton("Seleccionar foto")
        boton.clicked.connect(self.foto_select)
        layout.addWidget(boton)
        self.ruta = None


    def foto_select(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "seleccionar archivo", "", "Imágenes (*.png *.jpg *jpeg);;")
        if ruta:
            self.ruta = ruta


class ImagenPerfil(QLabel):
    def __init__(self, ruta_imagen, diametro=100, parent=None):
        super().__init__(parent)
        self.diametro = diametro
        self.setFixedSize(diametro, diametro)

        pixmap_original = QPixmap(ruta_imagen)
        self.setPixmap(self.recortar_circulo(pixmap_original))

    def recortar_circulo(self, pixmap):
        # Escala la imagen para llenar el círculo
        pixmap = pixmap.scaled(
            self.diametro, self.diametro,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        # Crea un pixmap nuevo con fondo transparente
        circular = QPixmap(self.diametro, self.diametro)
        circular.fill(Qt.GlobalColor.transparent)

        painter = QPainter(circular)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Define la forma circular como "molde" de recorte
        path = QPainterPath()
        path.addEllipse(0, 0, self.diametro, self.diametro)
        painter.setClipPath(path)

        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return circular

app = QApplication(sys.argv)
system = Sistema()
system.show()
sys.exit(app.exec())