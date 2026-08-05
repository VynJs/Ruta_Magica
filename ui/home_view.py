import flet as ft

# Paletas de color según el tema elegido en Configuración (solo afecta esta pantalla)
PALETAS = {
    "oscuro": {
        "BG": "#173029", "CARD": "#28453A", "BORDER": "#4C6B5A",
        "GOLD": "#E3A94A", "BTN_GREEN": "#93BE72", "TEXT": "#ECECE3",
        "MUTED": "#AFC2B3", "PLACEHOLDER": "#DDDDDD",
    },
    "claro": {
        "BG": "#F5F1E6", "CARD": "#FFFFFF", "BORDER": "#E0D9C4",
        "GOLD": "#B9791E", "BTN_GREEN": "#4F7A3D", "TEXT": "#2E2A22",
        "MUTED": "#8A8270", "PLACEHOLDER": "#E5E0D2",
    },
}

# Factor de escala según el tamaño de texto elegido en Configuración
ESCALAS = {"Pequeño": 0.85, "Mediano": 1.0, "Grande": 1.2}


def home_view(page: ft.Page) -> ft.View:

    usuario = page.app_state.get("usuario")
    nombre_usuario = getattr(usuario, "nombre", "Invitado") if usuario else "Invitado"

    # --- Tema y tamaño de texto elegidos en Configuración (solo aplica aquí) ---
    tema = page.app_state.get("tema", "oscuro")
    paleta = PALETAS.get(tema, PALETAS["oscuro"])
    BG, CARD, BORDER = paleta["BG"], paleta["CARD"], paleta["BORDER"]
    GOLD, BTN_GREEN, TEXT, MUTED = paleta["GOLD"], paleta["BTN_GREEN"], paleta["TEXT"], paleta["MUTED"]
    PLACEHOLDER = paleta["PLACEHOLDER"]

    escala = ESCALAS.get(page.app_state.get("tamano_texto", "Mediano"), 1.0)

    def sz(base: float) -> float:
        return round(base * escala, 1)

    def _tarjeta_categoria(icono: str, titulo: str, on_click) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=sz(50), color="#888"),
                        bgcolor=PLACEHOLDER,
                        height=180,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Row([ft.Icon(icono, color=TEXT), ft.Text(titulo, color=TEXT, size=sz(16))]),
                                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GOLD),
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
            expand=1,
            border=ft.border.all(1, BORDER),
            on_click=on_click,
            ink=True,
        )

    def cerrar_sesion(e):
        page.app_state["usuario"] = None
        page.app_state["rol"] = None
        page.go("/login")

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Row(
                    [ft.Image(src="logo.png", width=34, height=34), ft.Text("Ruta Mágica", color=GOLD, size=sz(16), weight=ft.FontWeight.BOLD)],
                    spacing=10,
                ),
                padding=ft.padding.only(left=15, top=15, bottom=10),
            ),
            ft.Divider(color=BORDER, height=1),
            ft.NavigationDrawerDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicio"),
            ft.NavigationDrawerDestination(icon=ft.Icons.HELP_OUTLINE, label="Sobre Huamantla"),
            ft.NavigationDrawerDestination(icon=ft.Icons.STOREFRONT_OUTLINED, label="Establecimientos"),
            ft.NavigationDrawerDestination(icon=ft.Icons.CELEBRATION_OUTLINED, label="Entretenimiento"),
            ft.NavigationDrawerDestination(icon=ft.Icons.EVENT_OUTLINED, label="Eventos"),
            ft.NavigationDrawerDestination(icon=ft.Icons.ADD_CIRCLE_OUTLINE, label="Agregar"),
            ft.Divider(),
            ft.NavigationDrawerDestination(icon=ft.Icons.SETTINGS_OUTLINED, label="Configuración"),
            ft.NavigationDrawerDestination(icon=ft.Icons.LOGOUT, label="Cerrar sesión"),
        ],
        bgcolor=CARD,
    )

    def abrir_menu(e):
        page.open(drawer)

    def on_select_drawer(e):
        idx = e.control.selected_index
        # Índices reales de cada NavigationDrawerDestination (los Divider/Container
        # no cuentan): 0 Inicio, 1 Sobre Huamantla, 2 Establecimientos,
        # 3 Entretenimiento, 4 Eventos, 5 Agregar, 6 Configuración, 7 Cerrar sesión
        if idx == 0:
            page.go("/home")
        elif idx == 2:
            page.go("/establecimientos")
        elif idx == 3:
            page.go("/entretenimiento")
        elif idx == 4:
            page.go("/eventos")
        elif idx == 5:
            page.go("/admin/reportes")
        elif idx == 6:
            page.go("/configuracion")
        elif idx == 7:
            cerrar_sesion(e)
        # idx 1 (Sobre Huamantla): no funciona aun AXEL

    drawer.on_change = on_select_drawer

    encabezado = ft.Row(
        [
            ft.IconButton(ft.Icons.MENU, icon_color=GOLD, on_click=abrir_menu),
            ft.Column(
                [
                    ft.Image(src="logo.png", width=39, height=39),
                    ft.Text("Ruta Mágica", size=sz(14), color=TEXT, italic=True),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.Column([ft.Icon(ft.Icons.FAVORITE_BORDER, color=GOLD), ft.Text("Favoritos", color=TEXT, size=sz(11))],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Container(
                        content=ft.Column([ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, color=GOLD), ft.Text(nombre_usuario, color=TEXT, size=sz(11))],
                                           horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        on_click=lambda e: page.go("/configuracion"), ink=True,
                    ),
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
                            ft.Text("Descubre la magia de", color=TEXT, size=sz(16)),
                            ft.Text("Huamantla", color=BTN_GREEN, size=sz(34), weight=ft.FontWeight.BOLD),
                            ft.Text("Explora, disfruta y vive experiencias\ninolvidables.", color=MUTED, size=sz(13)),
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
            _tarjeta_categoria(ft.Icons.STOREFRONT_OUTLINED, "Establecimientos", lambda e: page.go("/establecimientos")),
            _tarjeta_categoria(ft.Icons.CELEBRATION_OUTLINED, "Entretenimiento", lambda e: page.go("/entretenimiento")),
            _tarjeta_categoria(ft.Icons.EVENT_OUTLINED, "Eventos", lambda e: page.go("/eventos")),
        ],
        spacing=20,
    )

    footer = ft.Column(
        [
            ft.Divider(color=BORDER),
            ft.Row(
                [
                    ft.Row([ft.Image(src="logo.png", width=20, height=20), ft.Text("Ruta Mágica", color=GOLD, size=sz(14))], spacing=6),
                    ft.Row([
                        ft.TextButton("Ayuda", style=ft.ButtonStyle(color=MUTED)),
                        ft.TextButton("Términos y condiciones", style=ft.ButtonStyle(color=MUTED)),
                        ft.TextButton("Privacidad", style=ft.ButtonStyle(color=MUTED)),
                        ft.TextButton("Contáctanos", style=ft.ButtonStyle(color=MUTED)),
                    ]),
                    ft.Row([
                        ft.IconButton(ft.Icons.FACEBOOK, icon_color=GOLD),
                        ft.IconButton(ft.Icons.CAMERA_ALT_OUTLINED, icon_color=GOLD),
                        ft.IconButton(ft.Icons.EMAIL_OUTLINED, icon_color=GOLD),
                        ft.IconButton(ft.Icons.CHAT_OUTLINED, icon_color=GOLD),
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