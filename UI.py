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
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QFileDialog, QMessageBox, QScrollArea, QFrame, QGroupBox)
from PyQt6.QtGui import QGuiApplication, QAction, QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt, pyqtSignal
class ColoresConfig:
    def __init__(self):
        self.temas = {
                "claro": {
                    "fondo":         "#f4f6fa",
                    "fondo_tarjeta": "#ffffff",
                    "borde":         "#d9dee6",
                    "acento":        "#e0b93b",
                    "acento_hover":  "#c0532f",
                },
                "oscuro": {
                    "fondo":         "#1e2128",
                    "fondo_tarjeta": "#2a2e37",
                    "borde":         "#3a3f4b",
                    "acento":        "#d12121",
                    "acento_hover":  "#993131",
            },
        }
        self.color_menu = {"claro": "#DC00E0", "oscuro":"#004cff"}
        self.color_letra = {"claro": "#22262e", "oscuro":"#e6e8ec"}
        self.tamano_letra = 12

    def generar_qss(self, mode):
        colores = self.temas[mode]
        menu = self.color_menu[mode]
        texto = self.color_letra[mode]
        return f"""
        QMainWindow {{ background-color: {colores['fondo']}; }}

        QGroupBox {{
            background-color: {colores['fondo_tarjeta']};
            border: 1px solid {colores['borde']};
            border-radius: 10px;
            color: {colores['texto']};
        }}

        QPushButton {{
            background-color: {colores['acento']};
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
        }}

        QPushButton:hover {{ background-color: {colores['acento_hover']}; }}

        QLabel {{ color: {texto}; }}
        """


class Idiomas:
    def __init__(self):
        self.diccionario ={"es": {
                    "titulo_settings":    "Configuración",
                    "grupo_perfil":       "Perfil",
                    "label_nombre":       "Nombre de usuario",
                    "boton_cambiar_nom":  "Cambiar Nombre",
                    "placeholder_nombre": "Ingrese nuevo nombre...",
                    "menu_archivo":       "Archivo",
                    "menu_edicion":       "Edición",
                    "menu_ver":           "Ver",
                    "menu_config":        "Configuración",
                    "msg_exito_titulo":   "Éxito",
                    "msg_exito_texto":    "Nombre actualizado",
                    "msg_error_titulo":   "Error",
                    "msg_error_texto":    "El nombre no puede estar vacío ni superar los 40 caracteres",
                },
                "en": {
                    "titulo_settings":    "Settings",
                    "grupo_perfil":       "Profile",
                    "label_nombre":       "Username",
                    "boton_cambiar_nom":  "Change Name",
                    "placeholder_nombre": "Enter new name...",
                    "menu_archivo":       "File",
                    "menu_edicion":       "Edit",
                    "menu_ver":           "View",
                    "menu_config":        "Settings",
                    "msg_exito_titulo":   "Success",
                    "msg_exito_texto":    "Name updated",
                    "msg_error_titulo":   "Error",
                    "msg_error_texto":    "Name cannot be empty or exceed 40 characters",
                },
            }

    def devolver_diccionario(self, idioma):
        return self.diccionario[idioma]


class Sistema(QMainWindow):
    def __init__(self):
        super().__init__()

        # datos del cosito de PyQt
        self.setWindowTitle("Config Simulator")
        p = QGuiApplication.primaryScreen().geometry()
        x = 2*(p.width())//11
        y = (p.height())//6

        # poner el cosito de forma centrada
        self.move(x, y)
        self.setFixedSize(600, 400)

        # inicialización del contenedor
        self.contenedor = QStackedWidget()
        self.setCentralWidget(self.contenedor)

        #conexión con funciones encargadas de cada dato, para recuperarlos al momento de cerrar y al momento de cargar
        self.settings_page = settings_p()

        scroll = QScrollArea()
        scroll.setWidget(self.settings_page)
        scroll.setWidgetResizable(True)   

        # Asignación de distintas pestañas en función de la opción del menú elegida
        self.contenedor.addWidget(self.archivo_page())
        self.contenedor.addWidget(self.edicion_page())
        self.contenedor.addWidget(self.ver_page())
        self.contenedor.addWidget(scroll)

        #Barrita superior
        self.menu = self.menuBar()


        # --- BOTONES Y ACCIONES ---
        self.m_archivo = QAction("", self)
        self.m_archivo.triggered.connect(lambda: self.contenedor.setCurrentIndex(0))
        self.menu.addAction(self.m_archivo)

        self.m_edits = QAction("", self)
        self.m_edits.triggered.connect(lambda: self.contenedor.setCurrentIndex(1))
        self.menu.addAction(self.m_edits)

        self.m_ver = QAction("", self)
        self.m_ver.triggered.connect(lambda: self.contenedor.setCurrentIndex(2))
        self.menu.addAction(self.m_ver)

        self.m_settings = QAction("", self)
        self.m_settings.triggered.connect(lambda: self.contenedor.setCurrentIndex(3))
        self.menu.addAction(self.m_settings)

        # --- DATOS EDITABLES POR EL USUARIO ---
        # tema de la app
        self.tema_select = "claro"
        self.tema_manager = ColoresConfig()

        # nombre usuario
        self.username = None

        # idioma
        self.idioma = None
        self.idioma_manager = Idiomas()


    def color_upd(self, new_color):
        self.tema_select = new_color
        qss = self.tema_manager.generar_qss(new_color)
        QApplication.instance().setStyleSheet(qss)

    def idioma_upd(self, new_idioma): 
        self.idioma = new_idioma
        idioma_data = self.idioma_manager.devolver_diccionario(self.idioma)
        self.settings_page.t = self.idioma_manager.devolver_diccionario(self.idioma)
        self.m_archivo.setText(idioma_data["menu_archivo"])
        self.m_edits.setText(idioma_data["menu_edicion"])
        self.m_ver.setText(idioma_data["menu_ver"])
        self.m_settings.setText(idioma_data["menu_config"])
        self.settings_page.retraducir()


    def f_tamano_upd(self): pass
    def f_color_upd(self): pass
    def m_color_upd(self): pass

    
    # funciones patito para los layouts adicionales (solo para que esta madre no se ande crasheando)
    def _pagina_placeholder(self, texto):
        w = QWidget()
        l = QVBoxLayout()
        l.setContentsMargins(20, 20, 20, 20)
        lbl = QLabel(texto)
        lbl.setObjectName("TituloPagina")
        lbl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        l.addWidget(lbl)
        l.addStretch()
        w.setLayout(l)
        return w
 
    def archivo_page(self):
        return self._pagina_placeholder("Archivo (WIP)")
 
    def edicion_page(self):
        return self._pagina_placeholder("Edición (WIP)")
 
    def ver_page(self):
        return self._pagina_placeholder("Ver (WIP)")


class settings_p(QWidget):
    def __init__(self, parent = None, idioma = "es"):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        self.titulo = QLabel("Configuración")
        self.titulo.setObjectName("TituloPagina")
        layout.addWidget(self.titulo)

        # SECCIÓN DEL PERFIL
        perfil = QHBoxLayout()
        layout.addLayout(perfil)

        # IZQUIERDA - foto de perfil y selector de esta
        self.foto_layout = QVBoxLayout()
        self.foto_shaper = ImagenPerfil()
        self.foto_shaper.setObjectName("FotoPerfil")
        self.foto_archivo = SubidorArchivos()
        self.foto_layout.addWidget(self.foto_shaper, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.foto_layout.addWidget(self.foto_archivo)
        perfil.addLayout(self.foto_layout)

        self.foto_archivo.arch.connect(self.foto_shaper.carga_imagen)

        self.p_userData = QVBoxLayout()
        self.nombreHeader = QLabel("")
        self.p_userData.addWidget(self.nombreHeader)
        self.nombre_user = QLabel()
        self.nombre_user.setObjectName("NombreUsuarioLabel")
        self.nombre_upd = QPushButton("")
        self.p_userData.addWidget(self.nombre_user)
        self.p_userData.addWidget(self.nombre_upd)
        self.nombre_upd.clicked.connect(self.cambianombre)
        perfil.addLayout(self.p_userData)

        self.nom_upd_input = QLineEdit(self.nombre_user.text())
        self.nom_upd_input.setFixedWidth(self.width()//2 - 35)
        self.p_userData.addWidget(self.nom_upd_input)
        self.nom_upd_input.returnPressed.connect(lambda: self.nom_upd(self.nom_upd_input.text(), self.nom_upd_input))
        self.nom_upd_input.hide()

        layout.addWidget(self.linea_division())
        self.t = None

        # SECCIÓN DE EDICIÓN

    def cambianombre(self):
        self.nom_upd_input.show()
        self.nombre_upd.hide()

    def nom_upd(self, newName, input_place):
        if 1 < len(newName.strip()) < 40:
            self.nombre_user.setText(newName.strip())
            input_place.hide()
            self.nombre_upd.show()
            QMessageBox.information(self, self.t["msg_exito_titulo"], self.t["msg_exito_texto"])
        else:
            QMessageBox.warning(self, self.t["msg_error_titulo"], self.t["msg_error_texto"])


    def retraducir(self):
        self.titulo.setText(self.t["titulo_settings"])
        self.grupo_perfil.setTitle(self.t["grupo_perfil"])
        self.label_nombre_titulo.setText(self.t["label_nombre"])
        self.nombre_upd.setText(self.t["boton_cambiar_nom"])
        self.nom_upd_input.setPlaceholderText(self.t["placeholder_nombre"])


    def linea_division(self):
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)      
        linea.setFrameShadow(QFrame.Shadow.Sunken)   
        return linea

class SubidorArchivos(QWidget):
    arch = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Texto debajo
        self.t_perfil = QLabel("")
        layout.addWidget(self.t_perfil)

        boton = QPushButton("")
        boton.clicked.connect(self.foto_select)
        layout.addWidget(boton) 
        self.ruta = None


    def foto_select(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "seleccionar archivo", "", "Imágenes (*.png *.jpg *jpeg);;")
        if ruta:
            if ruta and ruta.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.ruta = ruta
                self.arch.emit(ruta)
            elif ruta:
                print("")

class ImagenPerfil(QLabel):
    def __init__(self, diametro=100, parent=None):
        super().__init__(parent)
        self.diametro = diametro
        self.setFixedSize(diametro, diametro)
        self.pixmap_o = None

    def carga_imagen(self, ruta_imagen):
        self.pixmap_o = QPixmap(ruta_imagen)
        self.setPixmap(self.recortar_circulo(self.pixmap_o))

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