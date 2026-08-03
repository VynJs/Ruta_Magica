import flet as ft

BG = "#173029"
CARD = "#28453A"
BORDER = "#4C6B5A"
GOLD = "#E3A94A"
BTN_GREEN = "#93BE72"
TEXT = "#ECECE3"
MUTED = "#AFC2B3"


def _tarjeta_categoria(icono: str, titulo: str, on_click) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.icons.IMAGE_OUTLINED, size=50, color="#666"),
                    bgcolor="#DDDDDD",
                    height=180,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Row([ft.Icon(icono, color=TEXT), ft.Text(titulo, color=TEXT, size=16)]),
                            ft.Icon(ft.icons.CHEVRON_RIGHT, color=GOLD),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=BG,
                    border=ft.border.all(1, GOLD),
                    padding=12,
                ),
            ],
            spacing=0,
        ),
        width=340,
        border=ft.border.all(1, BORDER),
    )


def home_view(page: ft.Page) -> ft.View:

    usuario = page.app_state.get("usuario")
    nombre_usuario = getattr(usuario, "nombre", "Invitado") if usuario else "Invitado"

    def cerrar_sesion(e):
        page.app_state["usuario"] = None
        page.app_state["rol"] = None
        page.go("/login")

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=10),
            ft.NavigationDrawerDestination(icon=ft.icons.HOME_OUTLINED, label="Inicio"),
            ft.NavigationDrawerDestination(icon=ft.icons.HELP_OUTLINE, label="Sobre Huamantla"),
            ft.NavigationDrawerDestination(icon=ft.icons.STOREFRONT_OUTLINED, label="Establecimientos"),
            ft.NavigationDrawerDestination(icon=ft.icons.CELEBRATION_OUTLINED, label="Entretenimiento"),
            ft.NavigationDrawerDestination(icon=ft.icons.EVENT_OUTLINED, label="Eventos"),
            ft.NavigationDrawerDestination(icon=ft.icons.ADD_CIRCLE_OUTLINE, label="Agregar"),
            ft.Divider(),
            ft.NavigationDrawerDestination(icon=ft.icons.SETTINGS_OUTLINED, label="Configuración"),
            ft.NavigationDrawerDestination(icon=ft.icons.LOGOUT, label="Cerrar sesión"),
        ],
        bgcolor=CARD,
    )

    def abrir_menu(e):
        page.open(drawer)

    def on_select_drawer(e):
        idx = e.control.selected_index
        rutas = {
            2: "/establecimientos",
            3: "/entretenimiento",
            4: "/eventos",
        }
        if idx == 8:
            cerrar_sesion(e)
        elif idx in rutas:
            page.go(rutas[idx])

    drawer.on_change = on_select_drawer

    encabezado = ft.Row(
        [
            ft.IconButton(ft.icons.MENU, icon_color=GOLD, on_click=abrir_menu),
            ft.Column(
                [
                    ft.Text("R⁘M", size=26, color=BTN_GREEN, weight=ft.FontWeight.BOLD),
                    ft.Text("Ruta Mágica", size=14, color=TEXT, italic=True),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.Column([ft.Icon(ft.icons.FAVORITE_BORDER, color=GOLD), ft.Text("Favoritos", color=TEXT, size=11)],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([ft.Icon(ft.icons.ACCOUNT_CIRCLE_OUTLINED, color=GOLD), ft.Text(nombre_usuario, color=TEXT, size=11)],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ],
                spacing=15,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    banner = ft.Container(
        content=ft.Stack(
            [
                ft.Container(bgcolor="#000000", height=280, border_radius=10),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Descubre la magia de", color=TEXT, size=16),
                            ft.Text("Huamantla", color=BTN_GREEN, size=34, weight=ft.FontWeight.BOLD),
                            ft.Text("Explora, disfruta y vive experiencias\ninolvidables.", color=MUTED, size=13),
                            ft.Container(height=8),
                            ft.ElevatedButton(
                                "Ver más  >",
                                style=ft.ButtonStyle(bgcolor=GOLD, color=BG, shape=ft.RoundedRectangleBorder(radius=20)),
                            ),
                        ],
                        spacing=4,
                    ),
                    padding=30,
                ),
            ]
        ),
        height=280,
    )

    tarjetas = ft.Row(
        [
            _tarjeta_categoria(ft.icons.STOREFRONT_OUTLINED, "Establecimientos", lambda e: page.go("/establecimientos")),
            _tarjeta_categoria(ft.icons.CELEBRATION_OUTLINED, "Entretenimiento", lambda e: page.go("/entretenimiento")),
            _tarjeta_categoria(ft.icons.EVENT_OUTLINED, "Eventos", lambda e: page.go("/eventos")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap=True,
    )

    footer = ft.Column(
        [
            ft.Divider(color=BORDER),
            ft.Row(
                [
                    ft.Text("Ruta Mágica", color=GOLD),
                    ft.Row([
                        ft.TextButton("Ayuda", style=ft.ButtonStyle(color=MUTED)),
                        ft.TextButton("Términos y condiciones", style=ft.ButtonStyle(color=MUTED)),
                        ft.TextButton("Privacidad", style=ft.ButtonStyle(color=MUTED)),
                        ft.TextButton("Contáctanos", style=ft.ButtonStyle(color=MUTED)),
                    ]),
                    ft.Row([
                        ft.IconButton(ft.icons.FACEBOOK, icon_color=GOLD),
                        ft.IconButton(ft.icons.CAMERA_ALT_OUTLINED, icon_color=GOLD),
                        ft.IconButton(ft.icons.EMAIL_OUTLINED, icon_color=GOLD),
                        ft.IconButton(ft.icons.CHAT_OUTLINED, icon_color=GOLD),
                    ]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ]
    )

    return ft.View(
        route="/home",
        bgcolor=BG,
        padding=25,
        drawer=drawer,
        controls=[
            encabezado,
            ft.Divider(color=GOLD),
            ft.Container(height=15),
            banner,
            ft.Container(height=20),
            tarjetas,
            ft.Container(height=20),
            footer,
        ],
        scroll=ft.ScrollMode.AUTO,
    )