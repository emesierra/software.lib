import reflex as rx
import mysql.connector

# Conexión global (ideal para ejemplo, pero en producción mejor pool)
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bloq1234",
    database="bdmysql"
)
cursor = conexion.cursor()

class RegistroState(rx.State):
    correo: str = ""
    usuario: str = ""
    contrasena: str = ""
    confirmar_contrasena: str = ""
    mensaje: str = ""

    @rx.event
    def set_correo(self, valor: str):
        self.correo = valor

    @rx.event
    def set_usuario(self, valor: str):
        self.usuario = valor

    @rx.event
    def set_contrasena(self, valor: str):
        self.contrasena = valor

    @rx.event
    def set_confirmar_contrasena(self, valor: str):
        self.confirmar_contrasena = valor

    @rx.event
    def registrar(self):
        if not self.correo or not self.usuario or not self.contrasena or not self.confirmar_contrasena:
            self.mensaje = "❌ Todos los campos son obligatorios."
            return

        if self.contrasena != self.confirmar_contrasena:
            self.mensaje = "❌ Las contraseñas no coinciden."
            return
        
        # Validar que el correo no exista
        cursor.execute("SELECT correo FROM usuarios WHERE correo=%s", (self.correo,))
        if cursor.fetchone():
            self.mensaje = "❌ El correo ya está registrado."
            return

        # Validar que el usuario no exista
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario=%s", (self.usuario,))
        if cursor.fetchone():
            self.mensaje = "❌ El usuario ya existe."
            return

        # Insertar nuevo usuario
        query = "INSERT INTO usuarios (correo, usuario, contraseña) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.correo, self.usuario, self.contrasena))
        conexion.commit()
        self.mensaje = "✅ Registro exitoso, ya puedes iniciar sesión."

@rx.page(route='/registro', title='Registrarse')
def registro() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Registro Biblioteca", size="3"),
            rx.input(
                placeholder="Correo",
                value=RegistroState.correo,
                on_change=RegistroState.set_correo,
                width="300px",
                margin_bottom="0.5rem",
                type_="email"
            ),
            rx.input(
                placeholder="Usuario",
                value=RegistroState.usuario,
                on_change=RegistroState.set_usuario,
                width="300px",
                margin_bottom="0.5rem"
            ),
            rx.input(
                placeholder="Contraseña",
                type_="password",
                value=RegistroState.contrasena,
                on_change=RegistroState.set_contrasena,
                width="300px",
                margin_bottom="0.5rem"
            ),
            rx.input(
                placeholder="Confirmar contraseña",
                type_="password",
                value=RegistroState.confirmar_contrasena,
                on_change=RegistroState.set_confirmar_contrasena,
                width="300px",
                margin_bottom="0.5rem"
            ),
            rx.button("Registrar", on_click=RegistroState.registrar, width="300px"),
            rx.text(RegistroState.mensaje, color="red", margin_top="1rem"),
            rx.link("Volver al login", href="/", color="blue", margin_top="1rem"),
        ),
        height="100vh",
    )


app = rx.App()
app.add_page(registro)
