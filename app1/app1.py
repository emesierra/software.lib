import reflex as rx
import mysql.connector

# Conexión global (ideal usar pool o manejar bien conexión)
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bloq1234",
    database="bdmysql"
)
cursor = conexion.cursor()

class LoginState(rx.State):
    usuario: str = ""
    contrasena: str = ""
    mensaje: str = ""
    show_password: bool = False  # <-- Estado para mostrar u ocultar contraseña

    @rx.event
    def set_usuario(self, valor: str):
        self.usuario = valor

    @rx.event
    def set_contrasena(self, valor: str):
        self.contrasena = valor

    @rx.event
    def toggle_password(self):
        self.show_password = not self.show_password

    @rx.event
    def login(self):
        query = "SELECT usuario FROM usuarios WHERE usuario=%s AND contraseña=%s"
        cursor.execute(query, (self.usuario, self.contrasena))
        resultado = cursor.fetchone()

        if resultado:
            self.mensaje = f"✅ Bienvenido {self.usuario}!"
        else:
            self.mensaje = "❌ Usuario o contraseña incorrectos."


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Login Biblioteca", size="3"),  # Ojo: usar "3" como string válido
            rx.input(
                placeholder="Usuario",
                value=LoginState.usuario,
                on_change=LoginState.set_usuario,
                width="300px",
                margin_bottom="0.5rem"
            ),
            rx.hstack(  # Contenedor horizontal para input y botón
                rx.input(
                    placeholder="Contraseña",
                    type_=rx.cond(LoginState.show_password, "text", "password"),
                    value=LoginState.contrasena,
                    on_change=LoginState.set_contrasena,
                    width="240px",
                ),
                rx.button(
                    rx.cond(LoginState.show_password, "🙈", "👁️"),
                    on_click=LoginState.toggle_password,
                    size="1",
                    variant="ghost",
                ),
                spacing="2",
                margin_bottom="0.5rem"
            ),
            rx.button("Ingresar", on_click=LoginState.login, width="300px"),
            rx.text(LoginState.mensaje, color="red", margin_top="1rem"),
        ),
        height="100vh",
    )

app = rx.App()
app.add_page(index)
