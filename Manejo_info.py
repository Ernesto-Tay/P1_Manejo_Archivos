"""
Nombre del archivo: config.json
Nombre del backup: config.json.bak
cuando se ejecuta el programa:
1. se obtiene toda la información del json
2. si el archivo no existe o no se puede obtener info de el (está corrupto), se arranca desde valores predeterminados
2. se evalúa si la ruta para la imagen sigue siendo válida
3. de no serlo, se establece la ruta de imagen como None (no hay cambios)
4. se intenta establecer la configuración
5. de haber configuración faltante, se evalúa qué hace falta o no funciona en el archivo json. Lo que funciona se ejecuta, lo que no ps se establece con valores predetermiandos
"""
import json
import os
class info_mng:
    def __init__(self):
        self.info = None

    def cargar_info(self, route = "info_sys.json"):
        backup = route + ".bak"
        if os.path.exists(route):
            try:
                with open(route, "r", encoding="utf-8") as a:
                    info = json.load(a)
                    return "Éxito", "Datos extraídos correctamente.", info

            except (json.JSONDecodeError, OSError):
                pass

        if os.path.exists(backup):
            try:
                with open(backup, "r", encoding="utf-8") as a:
                    info = json.load(a)
                    return "Advertencia", "El archivo original está corrupto o no hay permisos de lectura. Se usará la información del backup.", info
            except (json.JSONDecodeError, OSError):
                pass
        return "Error", "No se pudo obtener la información, se inicializará con valores por defecto.", None


    def guardar_info(self, info, route = "info_sys.json"):
        backup = route + ".bak"
        try:
           with open(backup, "w", enconding="utf-8") as a:
               with open(route, "r" , encoding="utf-8") as b:
                   a.write(b.read())
        except OSError:
            pass

        try:
            with open(route, "w", encoding="utf-8") as a:
                json.dump(info, a, indent=4)
            return "Éxito", "Información guardada correctamente."
        except OSError:
            return "Error", "No se pudo guardar la información."
