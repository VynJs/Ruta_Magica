import flet as ft

from ui.login_view import login_view
from ui.register_view import register_view
from ui.home_view import home_view
from ui.establecimientos_view import establecimientos_view
from ui.eventos_view import eventos_view
from ui.entretenimiento_view import entretenimiento_view
from ui.establecimiento_ver_view import establecimiento_ver_view
from ui.evento_ver_view import evento_ver_view
from ui.entretenimiento_ver_view import entretenimiento_ver_view
from ui.admin_reportes_view import admin_reportes_view
from ui.admin_categorias_view import admin_categorias_view
from ui.categoria_form_view import categoria_form_view
from ui.admin_eventos_view import admin_eventos_view
from ui.evento_form_view import evento_form_view
from ui.evento_detalle_view import evento_detalle_view
from ui.admin_establecimientos_view import admin_establecimientos_view
from ui.establecimiento_form_view import establecimiento_form_view
from ui.establecimiento_detalle_view import establecimiento_detalle_view
from ui.admin_entretenimiento_view import admin_entretenimiento_view
from ui.entretenimiento_form_view import entretenimiento_form_view
from ui.entretenimiento_detalle_view import entretenimiento_detalle_view


def main_window(page: ft.Page):
    page.title = "Ruta Mágica"
    page.padding = 0
    page.bgcolor = "#173029"
    page.window_width = 1300
    page.window_height = 850
    page.window_min_width = 900
    page.window_min_height = 650
    page.scroll = ft.ScrollMode.AUTO

    # ------------------------------------------------------------------
    # Estado global muy sencillo de la app (sesión, selección actual, etc.)
    # No se guarda en archivo aparte para respetar "no crear otros archivos";
    # vive como atributo dinámico sobre el objeto page.
    # ------------------------------------------------------------------
    page.app_state = {
        "usuario": None,          # objeto Admin logueado
        "rol": None,               # "admin" u "organizador"
        "categoria_sel": None,      # id de categoría a editar
        "evento_sel": None,
        "establecimiento_sel": None,
        "entretenimiento_sel": None,
    }

    def route_change(route):
        page.views.clear()

        if page.route == "/login":
            page.views.append(login_view(page))

        elif page.route == "/register":
            page.views.append(register_view(page))

        elif page.route == "/home":
            page.views.append(home_view(page))

        elif page.route == "/establecimientos":
            page.views.append(establecimientos_view(page))

        elif page.route == "/eventos":
            page.views.append(eventos_view(page))

        elif page.route == "/entretenimiento":
            page.views.append(entretenimiento_view(page))

        elif page.route == "/establecimiento/ver":
            page.views.append(establecimiento_ver_view(page))

        elif page.route == "/evento/ver":
            page.views.append(evento_ver_view(page))

        elif page.route == "/entretenimiento/ver":
            page.views.append(entretenimiento_ver_view(page))

        elif page.route == "/admin/reportes":
            page.views.append(admin_reportes_view(page))

        elif page.route == "/admin/categorias":
            page.views.append(admin_categorias_view(page))

        elif page.route == "/admin/categorias/agregar":
            page.app_state["categoria_sel"] = None
            page.views.append(categoria_form_view(page, modo="agregar"))

        elif page.route == "/admin/categorias/editar":
            page.views.append(categoria_form_view(page, modo="editar"))

        elif page.route == "/admin/eventos":
            page.views.append(admin_eventos_view(page))

        elif page.route == "/admin/eventos/agregar":
            page.app_state["evento_sel"] = None
            page.views.append(evento_form_view(page, modo="agregar"))

        elif page.route == "/admin/eventos/editar":
            page.views.append(evento_form_view(page, modo="editar"))

        elif page.route == "/admin/eventos/ver":
            page.views.append(evento_detalle_view(page))

        elif page.route == "/admin/establecimientos":
            page.views.append(admin_establecimientos_view(page))

        elif page.route == "/admin/establecimientos/agregar":
            page.app_state["establecimiento_sel"] = None
            page.views.append(establecimiento_form_view(page, modo="agregar"))

        elif page.route == "/admin/establecimientos/editar":
            page.views.append(establecimiento_form_view(page, modo="editar"))

        elif page.route == "/admin/establecimientos/ver":
            page.views.append(establecimiento_detalle_view(page))

        elif page.route == "/admin/entretenimiento":
            page.views.append(admin_entretenimiento_view(page))

        elif page.route == "/admin/entretenimiento/agregar":
            page.app_state["entretenimiento_sel"] = None
            page.views.append(entretenimiento_form_view(page, modo="agregar"))

        elif page.route == "/admin/entretenimiento/editar":
            page.views.append(entretenimiento_form_view(page, modo="editar"))

        elif page.route == "/admin/entretenimiento/ver":
            page.views.append(entretenimiento_detalle_view(page))

        else:
            # ruta desconocida -> mandar a login
            page.views.append(login_view(page))

        page.update()

    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route if page.route else "/login")