"""
config/tema.py
---------------
Paleta de colores y constantes visuales de Ruta Mágica, extraídas del
mockup oficial (fondo verde bosque oscuro, acentos dorados/ámbar y
botones verde oliva). Centralizar esto evita "colores mágicos" (hardcoded)
repetidos en cada vista y permite ajustar el tema desde un solo lugar.
"""

class Color:
    # Fondo general de la aplicación (verde bosque muy oscuro)
    FONDO = "#16311F"
    # Fondo de tarjetas / paneles, un tono más claro que el fondo general
    TARJETA = "#1F4029"
    TARJETA_HOVER = "#284D33"
    # Bordes sutiles
    BORDE = "#3A5C43"
    # Texto principal (crema/blanco cálido)
    TEXTO = "#F4F1E8"
    # Texto secundario (verde claro apagado)
    TEXTO_SECUNDARIO = "#A9C6A4"
    # Acento dorado/ámbar - títulos, links, botón primario de acción
    DORADO = "#E8A93D"
    DORADO_HOVER = "#F2BC5C"
    # Verde oliva - botón de acción principal (Guardar, Iniciar sesión)
    OLIVA = "#8FA662"
    OLIVA_HOVER = "#A1BA75"
    # Estados
    EXITO = "#6FBE73"
    ADVERTENCIA = "#D9B44A"
    ERROR = "#D9534F"
    INFO = "#5B9BD5"


class Tipografia:
    TITULO = 26
    SUBTITULO = 18
    TEXTO_BASE = 14
    TEXTO_PEQUENO = 12


class Espaciado:
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32