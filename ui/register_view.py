import flet as ft

from dao.admin_dao import AdminDAO
from models.admin import Admin

BG = "#173029"
CARD = "#28453A"
BORDER = "#4C6B5A"
GOLD = "#E3A94A"
BTN_GREEN = "#93BE72"
TEXT = "#ECECE3"
MUTED = "#AFC2B3"


def register_view(page: ft.Page) -> ft.View:

    nombre_field = ft.TextField(hint_text="Ej. José Luis", prefix_icon=ft.Icons.PERSON_OUTLINE,
                                 bgcolor=BG, border_color=BORDER, color=TEXT, border_radius=8)
    apellido_p_field = ft.TextField(hint_text="Ej. Ortiz", prefix_icon=ft.Icons.PERSON_OUTLINE,
                                     bgcolor=BG, border_color=BORDER, color=TEXT, border_radius=8)
    apellido_m_field = ft.TextField(hint_text="Ej. Montaño", prefix_icon=ft.Icons.PERSON_OUTLINE,
                                     bgcolor=BG, border_color=BORDER, color=TEXT, border_radius=8)
    correo_field = ft.TextField(hint_text="ejemplo@gmail.com", prefix_icon=ft.Icons.MAIL_OUTLINE,
                                 bgcolor=BG, border_color=BORDER, color=TEXT, border_radius=8)
    password_field = ft.TextField(hint_text="••••••••••••", prefix_icon=ft.Icons.LOCK_OUTLINE,
                                   password=True, can_reveal_password=True,
                                   bgcolor=BG, border_color=BORDER, color=TEXT, border_radius=8)

    mensaje = ft.Text("", color=ft.Colors.RED_300, size=12)

    def registrarme(e):
        nombre = (nombre_field.value or "").strip()
        apellido_p = (apellido_p_field.value or "").strip()
        apellido_m = (apellido_m_field.value or "").strip()
        correo = (correo_field.value or "").strip()
        password = (password_field.value or "").strip()

        if not nombre or not correo or not password:
            mensaje.value = "Nombre, correo y contraseña son obligatorios."
            page.update()
            return

        try:
            admin_dao = AdminDAO()
            ultimo_id = admin_dao.obtener_ultimo_id() + 1
            nuevo_admin = Admin(ultimo_id, nombre, apellido_p, apellido_m, correo, password)

            # NOTA: AdminDAO todavía no tiene un método insertar(). Hace falta
            # agregarlo (INSERT INTO admin ...) para que este registro se
            # guarde de verdad en la base de datos.
            admin_dao.insertar(nuevo_admin)

            page.go("/login")

        except AttributeError:
            mensaje.value = "Falta el método insertar() en AdminDAO para completar el registro."
            page.update()
        except Exception as ex:
            mensaje.value = f"Error al registrar: {ex}"
            page.update()

    contenido = ft.Column(
        [
            ft.Container(height=10),
            ft.Row(
                [
                    ft.IconButton(ft.Icons.MENU, icon_color=GOLD),
                    ft.Column(
                        [
                            ft.Text("R⁘M", size=26, color=BTN_GREEN, weight=ft.FontWeight.BOLD),
                            ft.Text("Ruta Mágica", size=14, color=TEXT, italic=True),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(width=40),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(color=GOLD),
            ft.Container(height=15),
            ft.Text("Crea una cuenta", size=24, color=GOLD, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Nombre", color=TEXT), nombre_field,
                        ft.Text("Apellido Paterno", color=TEXT), apellido_p_field,
                        ft.Text("Apellido Materno", color=TEXT), apellido_m_field,
                        ft.Text("Correo electrónico", color=TEXT), correo_field,
                        ft.Text("Contraseña", color=TEXT), password_field,
                        mensaje,
                    ],
                    spacing=6,
                ),
                bgcolor=CARD,
                border_radius=14,
                border=ft.border.all(1, BORDER),
                padding=25,
                width=450,
            ),
            ft.Container(height=15),
            ft.ElevatedButton(
                "Registrarme",
                width=450,
                height=45,
                style=ft.ButtonStyle(bgcolor=BTN_GREEN, color="#173029", shape=ft.RoundedRectangleBorder(radius=8)),
                on_click=registrarme,
            ),
            ft.TextButton("Ya tengo cuenta, iniciar sesión", style=ft.ButtonStyle(color=GOLD),
                          on_click=lambda e: page.go("/login")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )

    footer = ft.Row(
        [
            ft.Row([
                ft.TextButton("Ayuda", style=ft.ButtonStyle(color=MUTED)),
                ft.TextButton("Términos y condiciones", style=ft.ButtonStyle(color=MUTED)),
                ft.TextButton("Privacidad", style=ft.ButtonStyle(color=MUTED)),
                ft.TextButton("Contáctanos", style=ft.ButtonStyle(color=MUTED)),
            ]),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return ft.View(
        route="/register",
        bgcolor=BG,
        padding=30,
        controls=[contenido, ft.Divider(color=BORDER), footer],
    )