import flet as ft

from config.tema import Color
from ui.establecimiento_form import establecimiento_form
from ui.establecimiento_list import establecimiento_list
from ui.evento_form import evento_form
from ui.eventos_list import eventos_list
from ui.entretenimiento_form import entretenimiento_form
from ui.entretenimiento_list import entretenimiento_list

def main_window(page: ft.Page):

    #Conf Pag.
    page.title = "Ruta Magica - Panel Administrativo"
    page.window_width = 1100
    page.window_height = 700
    page.padding = 0
    page.bgcolor = Color.FONDO

    #Elementos del contenedor principal
    titulo = ft.Text(
        "Ruta Magica - Panel Administrativo",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=Color.TEXTO
    )

    subtitulo = ft.Text(
        "Seleccione una opcion del menu",
        size=16,
        color=Color.TEXTO_SECUNDARIO
    )

    #Creacion del contenedor principal
    contenido = ft.Container(
        padding=30,
        expand=True,
        bgcolor=Color.FONDO
    )

    #Pantalla Principal
    def inicio():
        return ft.Column(
            controls=[
                titulo,
                subtitulo
            ],
            spacing=10,
        )

    def mostrar_inicio(e=None):
        contenido.content = inicio()
        page.update()

    # ---------------- Establecimientos ----------------
    def mostrar_lista_establecimientos(e=None):
        contenido.content = establecimiento_list(
            regresar=mostrar_inicio,
            editar=mostrar_formulario_establecimiento_editar,
            agregar=mostrar_formulario_establecimiento_nuevo
        )
        page.update()

    def mostrar_formulario_establecimiento_nuevo(e=None):
        contenido.content = establecimiento_form(mostrar_lista_establecimientos)
        page.update()

    def mostrar_formulario_establecimiento_editar(establecimiento):
        contenido.content = establecimiento_form(mostrar_lista_establecimientos, establecimiento)
        page.update()

    # ---------------- Eventos ----------------
    def mostrar_lista_eventos(e=None):
        contenido.content = eventos_list(
            regresar=mostrar_inicio,
            editar=mostrar_formulario_evento_editar,
            agregar=mostrar_formulario_evento_nuevo
        )
        page.update()

    def mostrar_formulario_evento_nuevo(e=None):
        contenido.content = evento_form(mostrar_lista_eventos)
        page.update()

    def mostrar_formulario_evento_editar(evento):
        contenido.content = evento_form(mostrar_lista_eventos, evento)
        page.update()

    # ---------------- Entretenimiento ----------------
    def mostrar_lista_entretenimiento(e=None):
        contenido.content = entretenimiento_list(
            regresar=mostrar_inicio,
            editar=mostrar_formulario_entretenimiento_editar,
            agregar=mostrar_formulario_entretenimiento_nuevo
        )
        page.update()

    def mostrar_formulario_entretenimiento_nuevo(e=None):
        contenido.content = entretenimiento_form(mostrar_lista_entretenimiento)
        page.update()

    def mostrar_formulario_entretenimiento_editar(entretenimiento):
        contenido.content = entretenimiento_form(mostrar_lista_entretenimiento, entretenimiento)
        page.update()

    # Estilo compartido de los botones del menu lateral (fondo oscuro,
    # texto claro, se resaltan en dorado al pasar el mouse)
    estilo_boton_menu = ft.ButtonStyle(
        bgcolor=Color.FONDO,
        color=Color.TEXTO,
        overlay_color=Color.TARJETA_HOVER,
        shape=ft.RoundedRectangleBorder(radius=8),
    )

    #Creacion menu lateral
    menu_lateral = ft.Container(
        width=220,
        bgcolor=Color.TARJETA,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Ruta Magica",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=Color.DORADO
                ),
                ft.Text(
                    "Panel Administrativo",
                    size=12,
                    color=Color.TEXTO_SECUNDARIO
                ),
                ft.Divider(color=Color.BORDE),
                #Botones
                ft.ElevatedButton(
                    "Inicio",
                    icon=ft.Icons.HOME,
                    icon_color=Color.DORADO,
                    width=180,
                    style=estilo_boton_menu,
                    on_click=mostrar_inicio
                ),
                ft.ElevatedButton(
                    "Establecimientos",
                    icon=ft.Icons.STOREFRONT,
                    icon_color=Color.DORADO,
                    width=180,
                    style=estilo_boton_menu,
                    on_click=mostrar_lista_establecimientos
                ),
                ft.ElevatedButton(
                    "Eventos",
                    icon=ft.Icons.EVENT,
                    icon_color=Color.DORADO,
                    width=180,
                    style=estilo_boton_menu,
                    on_click=mostrar_lista_eventos
                ),
                ft.ElevatedButton(
                    "Entretenimiento",
                    icon=ft.Icons.HIKING,
                    icon_color=Color.DORADO,
                    width=180,
                    style=estilo_boton_menu,
                    on_click=mostrar_lista_entretenimiento
                ),
                ft.ElevatedButton(
                    "Categorias",
                    icon=ft.Icons.CATEGORY,
                    icon_color=Color.DORADO,
                    width=180,
                    style=estilo_boton_menu,
                ),
            ],
            spacing=15
        )
    )

    #Layout de la pag
    layout = ft.Row(
        controls=[
            menu_lateral,
            contenido
        ],
        expand=True,
        spacing=0
    )

    page.add(layout)

    mostrar_inicio()


if __name__ == "__main__":
    ft.app(target=main_window)