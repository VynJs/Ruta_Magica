import flet as ft

from dao.admin_dao import AdminDAO

# Colorimetría compartida por todas las interfaces de Ruta Mágica
BG = "#173029"
CARD = "#28453A"
BORDER = "#4C6B5A"
GOLD = "#E3A94A"
BTN_GREEN = "#93BE72"
TEXT = "#ECECE3"
MUTED = "#AFC2B3"


def _footer() -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Divider(color=BORDER),
                ft.Row(
                    [
                        ft.Text("Ruta Mágica", color=GOLD, size=14, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.TextButton("Ayuda", style=ft.ButtonStyle(color=MUTED)),
                                ft.TextButton("Términos y Condiciones", style=ft.ButtonStyle(color=MUTED)),
                                ft.TextButton("Privacidad", style=ft.ButtonStyle(color=MUTED)),
                                ft.TextButton("Contáctanos", style=ft.ButtonStyle(color=MUTED)),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.FACEBOOK, icon_color=GOLD),
                                ft.IconButton(ft.icons.CAMERA_ALT_OUTLINED, icon_color=GOLD),
                                ft.IconButton(ft.icons.EMAIL_OUTLINED, icon_color=GOLD),
                                ft.IconButton(ft.icons.CHAT_OUTLINED, icon_color=GOLD),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ]
        ),
        padding=ft.padding.symmetric(horizontal=30, vertical=10),
    )


def login_view(page: ft.Page) -> ft.View:

    correo_field = ft.TextField(
        hint_text="ejemplo@gmail.com",
        prefix_icon=ft.icons.MAIL_OUTLINE,
        bgcolor=BG,
        border_color=BORDER,
        color=TEXT,
        border_radius=8,
    )

    password_field = ft.TextField(
        hint_text="••••••••••••",
        prefix_icon=ft.icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        bgcolor=BG,
        border_color=BORDER,
        color=TEXT,
        border_radius=8,
    )

    recordar_check = ft.Checkbox(label="Recordar contraseña", value=False)
    mensaje = ft.Text("", color=ft.colors.RED_300, size=12)

    def iniciar_sesion(e):
        correo = (correo_field.value or "").strip()
        password = (password_field.value or "").strip()

        if not correo or not password:
            mensaje.value = "Escribe tu correo y contraseña."
            page.update()
            return

        try:
            admin_dao = AdminDAO()
            encontrado = admin_dao.autenticar(correo, password)

            if encontrado is None:
                mensaje.value = "Correo o contraseña incorrectos."
                page.update()
                return

            page.app_state["usuario"] = encontrado
            page.app_state["rol"] = "admin"
            page.go("/admin/reportes")

        except Exception as ex:
            mensaje.value = f"Error de conexión: {ex}"
            page.update()

    contenido = ft.Column(
        [
            ft.Container(height=10),
            ft.Row(
                [
                    ft.IconButton(ft.icons.MENU, icon_color=GOLD),
                    ft.Column(
                        [
                            ft.Text("R⁘M", size=30, color=BTN_GREEN, weight=ft.FontWeight.BOLD),
                            ft.Text("Ruta Mágica", size=16, color=TEXT, italic=True),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(width=40),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(color=GOLD),
            ft.Container(height=20),
            ft.Text("Iniciar sesión", size=26, color=GOLD, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Correo", color=TEXT),
                        correo_field,
                        ft.Text("Contraseña", color=TEXT),
                        password_field,
                        ft.Row(
                            [
                                recordar_check,
                                ft.TextButton("Olvidé mi contraseña", style=ft.ButtonStyle(color=GOLD)),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        mensaje,
                    ],
                    spacing=8,
                ),
                bgcolor=CARD,
                border_radius=14,
                border=ft.border.all(1, BORDER),
                padding=25,
                width=450,
            ),
            ft.Container(height=15),
            ft.ElevatedButton(
                "Iniciar sesión",
                width=450,
                height=45,
                style=ft.ButtonStyle(bgcolor=BTN_GREEN, color="#173029", shape=ft.RoundedRectangleBorder(radius=8)),
                on_click=iniciar_sesion,
            ),
            ft.Container(height=5),
            ft.TextButton(
                "Registrarse aquí",
                style=ft.ButtonStyle(color=GOLD),
                on_click=lambda e: page.go("/register"),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.View(
        route="/login",
        bgcolor=BG,
        padding=30,
        controls=[contenido, _footer()],
    )