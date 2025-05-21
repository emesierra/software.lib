import reflex as rx
import mysql.connector

# Conexión global (puedes moverla a un módulo aparte si quieres)
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bloq1234",
    database="bdmysql"
)
cursor = conexion.cursor()

class RegistroState(rx.State):
    usuario: str = ""
    contrasena: str = ""
    confirmar_contrasena: str = ""
    mensaje: str = ""

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
        if self.contrasena != self.confirmar_contrasena:
            self.mensaje = "❌ Las contraseñas no coinciden."
            return
        
        # Validar si el usuario ya existe
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario=%s", (self.usuario,))
        if cursor.fetchone():
            self.mensaje = "❌ El usuario ya existe."
            return
        
        # Insertar nuevo usuario
        query = "INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s)"
        cursor.execute(query, (self.usuario, self.contrasena))
        conexion.commit()
        self.mensaje = "✅ Registro exitoso, ya puedes iniciar sesión."

@rx.page(route='/registro', title='Registrarse')
def registro() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Registro Biblioteca", size="3"),
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