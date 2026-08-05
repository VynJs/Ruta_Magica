import flet as ft

from dao.admin_dao import AdminDAO
from models.admin import Admin

BG = "#173029"
CARD = "#28453A"
SIDEBAR = "#0F2620"
BORDER = "#4C6B5A"
GOLD = "#E3A94A"
BTN_GREEN = "#93BE72"
TEXT = "#ECECE3"
MUTED = "#AFC2B3"
ROJO = "#C0564C"

# Paleta del tema claro/crema (opción de apariencia)
CREMA_BG = "#F5F1E6"
CREMA_CARD = "#FFFFFF"
CREMA_TEXT = "#2E2A22"
CREMA_MUTED = "#8A8270"
CREMA_BORDER = "#E0D9C4"


def _sidebar(page: ft.Page) -> ft.Container:
    def item(icono, texto, ruta, clave=None):
        activo = clave == "config"
        return ft.Container(
            content=ft.Row([ft.Icon(icono, color=TEXT if not activo else GOLD, size=18),
                             ft.Text(texto, color=TEXT if not activo else GOLD)]),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            bgcolor=CARD if activo else None,
            border_radius=6,
            on_click=(lambda e: page.go(ruta)) if ruta else None,
        )

    def cerrar_sesion(e):
        page.app_state["usuario"] = None
        page.go("/login")

    return ft.Container(
        width=210, bgcolor=SIDEBAR, padding=15,
        content=ft.Column(
            [
                ft.Row([ft.Image(src="logo.png", width=30, height=30), ft.Text("Ruta Mágica", color=BTN_GREEN, size=16, weight=ft.FontWeight.BOLD)], spacing=8),
                ft.Container(height=15),
                item(ft.Icons.HOME_OUTLINED, "Inicio", "/home"),
                item(ft.Icons.BAR_CHART_OUTLINED, "Reportes", "/admin/reportes"),
                item(ft.Icons.EVENT_OUTLINED, "Gestión Eventos", "/admin/eventos"),
                item(ft.Icons.STOREFRONT_OUTLINED, "Gestión Estable.", "/admin/establecimientos"),
                item(ft.Icons.CELEBRATION_OUTLINED, "Gestión Entre.", "/admin/entretenimiento"),
                item(ft.Icons.CATEGORY_OUTLINED, "Gestión Cat.", "/admin/categorias"),
                ft.Divider(color=BORDER),
                item(ft.Icons.STOREFRONT, "Establecimientos", "/establecimientos"),
                item(ft.Icons.EVENT, "Eventos", "/eventos"),
                item(ft.Icons.STAR_BORDER, "Entretenimiento", "/entretenimiento"),
                ft.Container(expand=True),
                item(ft.Icons.SETTINGS_OUTLINED, "Configuración", "/configuracion", "config"),
                ft.Divider(color=BORDER),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.LOGOUT, color=TEXT, size=18), ft.Text("Cerrar sesión", color=TEXT)]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10), on_click=cerrar_sesion,
                ),
            ],
            expand=True,
        ),
    )


def configuracion_view(page: ft.Page) -> ft.View:

    usuario = page.app_state.get("usuario")
    admin_dao = AdminDAO()

    seccion_activa = {"actual": "cuenta"}
    panel_derecho = ft.Container(expand=True)

    mensaje_cuenta = ft.Text("", color=ft.Colors.RED_300)
    mensaje_pass = ft.Text("", color=ft.Colors.RED_300)

    # ---------------------- Sección: Cuenta ----------------------
    def panel_cuenta():
        nombre_field = ft.TextField(label="Nombre", value=getattr(usuario, "nombre", ""),
                                     bgcolor=BG, border_color=BORDER, color=TEXT)
        apellido_p_field = ft.TextField(label="Apellido paterno", value=getattr(usuario, "apellido_p", "") or "",
                                         bgcolor=BG, border_color=BORDER, color=TEXT)
        apellido_m_field = ft.TextField(label="Apellido materno", value=getattr(usuario, "apellido_m", "") or "",
                                         bgcolor=BG, border_color=BORDER, color=TEXT)
        correo_field = ft.TextField(label="Correo electrónico", value=getattr(usuario, "correo", ""),
                                     bgcolor=BG, border_color=BORDER, color=TEXT)

        def guardar_datos(e):
            if not usuario:
                mensaje_cuenta.value = "No hay una sesión activa."
                page.update()
                return
            try:
                actualizado = Admin(usuario.id, nombre_field.value, apellido_p_field.value,
                                     apellido_m_field.value, correo_field.value, getattr(usuario, "password", None))
                admin_dao.actualizar(actualizado)
                page.app_state["usuario"] = actualizado
                mensaje_cuenta.value = "Datos actualizados correctamente."
                mensaje_cuenta.color = BTN_GREEN
            except Exception as ex:
                mensaje_cuenta.value = f"Error al guardar: {ex}"
                mensaje_cuenta.color = ft.Colors.RED_300
            page.update()

        actual_field = ft.TextField(label="Contraseña actual", password=True, can_reveal_password=True,
                                     bgcolor=BG, border_color=BORDER, color=TEXT)
        nueva_field = ft.TextField(label="Nueva contraseña", password=True, can_reveal_password=True,
                                    bgcolor=BG, border_color=BORDER, color=TEXT)
        confirmar_field = ft.TextField(label="Confirmar nueva contraseña", password=True, can_reveal_password=True,
                                        bgcolor=BG, border_color=BORDER, color=TEXT)

        def cambiar_password(e):
            if not usuario:
                mensaje_pass.value = "No hay una sesión activa."
                page.update()
                return
            if getattr(usuario, "password", None) and actual_field.value != usuario.password:
                mensaje_pass.value = "La contraseña actual no coincide."
                mensaje_pass.color = ft.Colors.RED_300
                page.update()
                return
            if not nueva_field.value or nueva_field.value != confirmar_field.value:
                mensaje_pass.value = "La nueva contraseña y su confirmación no coinciden."
                mensaje_pass.color = ft.Colors.RED_300
                page.update()
                return
            try:
                actualizado = Admin(usuario.id, usuario.nombre, getattr(usuario, "apellido_p", ""),
                                     getattr(usuario, "apellido_m", ""), usuario.correo, nueva_field.value)
                admin_dao.actualizar(actualizado)
                page.app_state["usuario"] = actualizado
                mensaje_pass.value = "Contraseña actualizada correctamente."
                mensaje_pass.color = BTN_GREEN
                actual_field.value = nueva_field.value = confirmar_field.value = ""
            except Exception as ex:
                mensaje_pass.value = f"Error al cambiar la contraseña: {ex}"
                mensaje_pass.color = ft.Colors.RED_300
            page.update()

        avatar = ft.Container(
            content=ft.CircleAvatar(
                content=ft.Text((getattr(usuario, "nombre", "?") or "?")[:1].upper(), size=28, color=BG),
                bgcolor=BTN_GREEN, radius=45,
            ),
        )

        return ft.Column(
            [
                ft.Text("Cuenta", color=GOLD, size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Administra tu nombre, correo, foto de perfil y contraseña.", color=MUTED, size=12),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Row(
                        [
                            avatar,
                            ft.Column(
                                [
                                    ft.Text("Foto de perfil", color=TEXT, weight=ft.FontWeight.BOLD),
                                    ft.Text("JPG o PNG, máx. 2MB", color=MUTED, size=11),
                                    ft.Row([
                                        ft.ElevatedButton("Cambiar foto", icon=ft.Icons.UPLOAD_FILE,
                                                          style=ft.ButtonStyle(bgcolor=GOLD, color=BG)),
                                        ft.OutlinedButton("Quitar foto", style=ft.ButtonStyle(color=TEXT)),
                                    ]),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=20, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Información personal", color=TEXT, weight=ft.FontWeight.BOLD),
                            ft.Row([nombre_field, apellido_p_field, apellido_m_field], spacing=12),
                            correo_field,
                            mensaje_cuenta,
                            ft.ElevatedButton("Guardar cambios", style=ft.ButtonStyle(bgcolor=GOLD, color=BG),
                                              on_click=guardar_datos),
                        ],
                        spacing=10,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Cambiar contraseña", color=TEXT, weight=ft.FontWeight.BOLD),
                            actual_field,
                            ft.Row([nueva_field, confirmar_field], spacing=12),
                            mensaje_pass,
                            ft.ElevatedButton("Actualizar contraseña", style=ft.ButtonStyle(bgcolor=GOLD, color=BG),
                                              on_click=cambiar_password),
                        ],
                        spacing=10,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
            ],
            spacing=6, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ---------------------- Sección: Apariencia ----------------------
    def panel_apariencia():
        tema_actual = page.app_state.get("tema", "oscuro")

        def elegir_tema(nuevo_tema):
            page.app_state["tema"] = nuevo_tema
            if nuevo_tema == "claro":
                page.bgcolor = CREMA_BG
            else:
                page.bgcolor = BG
            page.go("/configuracion")

        def tarjeta_tema(nombre, etiqueta, color_fondo, color_texto, valor):
            seleccionado = tema_actual == valor
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Container(bgcolor=color_fondo, height=70, border_radius=8,
                                     border=ft.border.all(2, GOLD if seleccionado else BORDER),
                                     content=ft.Text("Aa", color=color_texto, size=20, weight=ft.FontWeight.BOLD),
                                     alignment=ft.alignment.center),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE if seleccionado else ft.Icons.RADIO_BUTTON_UNCHECKED,
                                    color=BTN_GREEN if seleccionado else MUTED, size=18),
                            ft.Text(etiqueta, color=TEXT),
                        ]),
                    ],
                    spacing=8,
                ),
                width=180, padding=10, border_radius=10,
                on_click=lambda e: elegir_tema(valor),
            )

        tamano_texto = page.app_state.get("tamano_texto", "Mediano")

        def cambiar_tamano(nuevo_valor):
            page.app_state["tamano_texto"] = nuevo_valor
            page.go("/configuracion")

        return ft.Column(
            [
                ft.Text("Apariencia", color=GOLD, size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Personaliza cómo se ve Ruta Mágica para ti.", color=MUTED, size=12),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Tema", color=TEXT, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                tarjeta_tema("oscuro", "Oscuro (actual)", BG, TEXT, "oscuro"),
                                tarjeta_tema("claro", "Claro crema", CREMA_BG, CREMA_TEXT, "claro"),
                            ], spacing=15),
                            ft.Text(
                                "Nota: por ahora el tema claro se aplica a esta pantalla como vista previa. "
                                "Para que se aplique en toda la app, cada interfaz necesita leer este mismo ajuste "
                                "en vez de sus colores fijos — avísame si quieres que lo dejemos funcionando en todas.",
                                color=MUTED, size=11, italic=True,
                            ),
                        ],
                        spacing=10,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Tamaño de texto", color=TEXT, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.Chip(label=ft.Text("Pequeño"), selected=tamano_texto == "Pequeño",
                                        on_select=lambda e: cambiar_tamano("Pequeño")),
                                ft.Chip(label=ft.Text("Mediano"), selected=tamano_texto == "Mediano",
                                        on_select=lambda e: cambiar_tamano("Mediano")),
                                ft.Chip(label=ft.Text("Grande"), selected=tamano_texto == "Grande",
                                        on_select=lambda e: cambiar_tamano("Grande")),
                            ], spacing=10),
                        ],
                        spacing=10,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
            ],
            spacing=6, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ---------------------- Sección: Notificaciones ----------------------
    def panel_notificaciones():
        def fila_switch(titulo, subtitulo, valor_inicial=True):
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Column([ft.Text(titulo, color=TEXT), ft.Text(subtitulo, color=MUTED, size=11)], spacing=2, expand=True),
                        ft.Switch(value=valor_inicial, active_color=BTN_GREEN),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.symmetric(vertical=8),
            )

        return ft.Column(
            [
                ft.Text("Notificaciones", color=GOLD, size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Elige qué avisos quieres recibir de la plataforma.", color=MUTED, size=12),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        [
                            fila_switch("Nuevas solicitudes pendientes", "Cuando un establecimiento o evento entra en revisión"),
                            ft.Divider(color=BORDER),
                            fila_switch("Aprobaciones y rechazos", "Cuando se aprueba o rechaza un registro que administras"),
                            ft.Divider(color=BORDER),
                            fila_switch("Resumen semanal por correo", "Estadísticas de la plataforma cada semana", False),
                            ft.Divider(color=BORDER),
                            fila_switch("Notificaciones dentro de la app", "Avisos emergentes mientras usas Ruta Mágica"),
                        ],
                        spacing=4,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
            ],
            spacing=6, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ---------------------- Sección: Privacidad y seguridad ----------------------
    def panel_privacidad():
        return ft.Column(
            [
                ft.Text("Privacidad y seguridad", color=GOLD, size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Controla la visibilidad de tu información y el acceso a tu cuenta.", color=MUTED, size=12),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Column([ft.Text("Mostrar mi nombre en los registros que apruebo", color=TEXT),
                                           ft.Text("Los propietarios y organizadores verán quién revisó su contenido", color=MUTED, size=11)],
                                          spacing=2, expand=True),
                                ft.Switch(value=True, active_color=BTN_GREEN),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(color=BORDER),
                            ft.Row([
                                ft.Column([ft.Text("Verificación en dos pasos", color=TEXT),
                                           ft.Text("Agrega una capa extra de seguridad al iniciar sesión (próximamente)", color=MUTED, size=11)],
                                          spacing=2, expand=True),
                                ft.Switch(value=False, disabled=True),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ],
                        spacing=4,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Sesión", color=TEXT, weight=ft.FontWeight.BOLD),
                            ft.OutlinedButton("Cerrar sesión en todos los dispositivos", icon=ft.Icons.DEVICES_OTHER,
                                              style=ft.ButtonStyle(color=ROJO)),
                        ],
                        spacing=10,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
            ],
            spacing=6, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ---------------------- Sección: Ayuda y soporte ----------------------
    def panel_ayuda():
        def fila_link(icono, texto):
            return ft.Container(
                content=ft.Row([ft.Icon(icono, color=GOLD, size=18), ft.Text(texto, color=TEXT), ft.Container(expand=True),
                                 ft.Icon(ft.Icons.CHEVRON_RIGHT, color=MUTED)]),
                padding=ft.padding.symmetric(vertical=10),
            )

        return ft.Column(
            [
                ft.Text("Ayuda y soporte", color=GOLD, size=22, weight=ft.FontWeight.BOLD),
                ft.Text("¿Necesitas ayuda usando Ruta Mágica?", color=MUTED, size=12),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        [
                            fila_link(ft.Icons.HELP_OUTLINE, "Centro de ayuda"),
                            ft.Divider(color=BORDER, height=1),
                            fila_link(ft.Icons.MAIL_OUTLINE, "Contactar soporte"),
                            ft.Divider(color=BORDER, height=1),
                            fila_link(ft.Icons.BUG_REPORT_OUTLINED, "Reportar un problema"),
                            ft.Divider(color=BORDER, height=1),
                            fila_link(ft.Icons.DESCRIPTION_OUTLINED, "Términos y condiciones"),
                            ft.Divider(color=BORDER, height=1),
                            fila_link(ft.Icons.PRIVACY_TIP_OUTLINED, "Aviso de privacidad"),
                        ],
                        spacing=0,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
            ],
            spacing=6, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ---------------------- Sección: Acerca de ----------------------
    def panel_acerca_de():
        return ft.Column(
            [
                ft.Text("Acerca de", color=GOLD, size=22, weight=ft.FontWeight.BOLD),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([ft.Image(src="logo.png", width=50, height=50),
                                    ft.Column([ft.Text("Ruta Mágica", color=GOLD, size=18, weight=ft.FontWeight.BOLD),
                                               ft.Text("Versión 1.0.0", color=MUTED, size=12)], spacing=2)], spacing=15),
                            ft.Divider(color=BORDER),
                            ft.Text("Plataforma para la difusión y gestión turística de Huamantla, Tlaxcala.", color=TEXT),
                            ft.Text("Desarrollado como proyecto integrador.", color=MUTED, size=12),
                        ],
                        spacing=10,
                    ),
                    bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
                ),
            ],
            spacing=6, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    secciones = {
        "cuenta": ("Cuenta", ft.Icons.PERSON_OUTLINE, panel_cuenta),
        "apariencia": ("Apariencia", ft.Icons.PALETTE_OUTLINED, panel_apariencia),
        "notificaciones": ("Notificaciones", ft.Icons.NOTIFICATIONS_OUTLINED, panel_notificaciones),
        "privacidad": ("Privacidad y seguridad", ft.Icons.SHIELD_OUTLINED, panel_privacidad),
        "ayuda": ("Ayuda y soporte", ft.Icons.HELP_OUTLINE, panel_ayuda),
        "acerca": ("Acerca de", ft.Icons.INFO_OUTLINE, panel_acerca_de),
    }

    menu_izquierdo = ft.Column(spacing=2)

    def seleccionar_seccion(clave):
        seccion_activa["actual"] = clave
        panel_derecho.content = secciones[clave][2]()
        construir_menu()
        page.update()

    def construir_menu():
        menu_izquierdo.controls.clear()
        for clave, (etiqueta, icono, _) in secciones.items():
            activo = seccion_activa["actual"] == clave
            menu_izquierdo.controls.append(
                ft.Container(
                    content=ft.Row([ft.Icon(icono, color=GOLD if activo else TEXT, size=18),
                                     ft.Text(etiqueta, color=GOLD if activo else TEXT)]),
                    bgcolor=CARD if activo else None,
                    padding=ft.padding.symmetric(horizontal=14, vertical=10),
                    border_radius=8,
                    on_click=lambda e, c=clave: seleccionar_seccion(c),
                )
            )

    construir_menu()
    panel_derecho.content = secciones[seccion_activa["actual"]][2]()

    encabezado = ft.Row(
        [
            ft.Text("Configuración", color=GOLD, size=26, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, color=GOLD, size=32),
                ft.Text(getattr(usuario, "nombre", "Usuario") if usuario else "Usuario", color=TEXT),
            ]),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    contenido = ft.Column(
        [
            encabezado,
            ft.Divider(color=GOLD),
            ft.Row(
                [
                    ft.Container(content=menu_izquierdo, width=250, bgcolor=CARD, border_radius=10,
                                 border=ft.border.all(1, BORDER), padding=10),
                    panel_derecho,
                ],
                spacing=20, vertical_alignment=ft.CrossAxisAlignment.START, expand=True,
            ),
        ],
        spacing=15, expand=True,
    )

    return ft.View(
        route="/configuracion",
        bgcolor=BG,
        padding=0,
        controls=[
            ft.Row(
                [_sidebar(page), ft.Container(content=contenido, padding=25, expand=True)],
                expand=True, vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ],
    )