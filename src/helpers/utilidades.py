import os

# Esta clase es de funciones auxiliares reutilizables del proyecto #
class Utilidades:
    @staticmethod
    def asegurar_carpeta(ruta):
        carpeta = os.path.dirname(ruta)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)

    @staticmethod
    def formatear_porcentaje(valor, decimales=2):
        return f"{round(valor, decimales)}%"

    @staticmethod
    def es_anio_valido(anio, anio_min=1930, anio_max=2026):
        try:
            anio_int = int(anio)
        except (TypeError, ValueError):
            return False
        return anio_min <= anio_int <= anio_max
