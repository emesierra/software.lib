import reflex as rx
import mysql.connector


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

    @rx.event
    def set_usuario(self, valor: str):
        self.usuario = valor

    @rx.event
    def set_contrasena(self, valor: str):
        self.contrasena = valor

    @rx.event
    def login(self):
        query = "SELECT usuario FROM usuarios WHERE usuario=%s AND contraseña=%s"
        cursor.execute(query, (self.usuario, self.contrasena))
        resultado = cursor.fetchone()

        if resultado:
            
            self.mensaje = f"✅ Bienvenido {self.usuario}!"
            return rx.redirect("/menu")
        else:
            self.mensaje = "❌ Usuario o contraseña incorrectos."

def index() -> rx.Component:
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading("Entrada Biblioteca", size="5", color="black"),
                rx.input(
                    placeholder="Usuario",
                    value=LoginState.usuario,
                    on_change=LoginState.set_usuario,
                    width="300px",
                    margin_bottom="0.5rem",
                    color="black"
                ),
                rx.input(
                    placeholder="Contraseña",
                    type_="password",
                    value=LoginState.contrasena,
                    on_change=LoginState.set_contrasena,
                    width="300px",
                    margin_bottom="0.5rem",
                    color="black"
                ),
                rx.button("Ingresar", on_click=LoginState.login, width="300px"),
                rx.text(LoginState.mensaje, color="red", margin_top="1rem"),

                
                rx.link(
                    "or, sign up",
                    on_click=rx.redirect("/registro"),
                    color="#0059FF",
                    margin_top="1rem",
                    style={"cursor": "pointer", "textDecoration": "underline"}
                ),
                
        
            ),
            background_color="#FFFFFF",  # Azul oscuro
            border_radius="16px",
            padding="32px",
            shadow="lg",
            width="350px", 
        ),
        height="100vh",  # Centrado vertical
        background="#011E26" 
    )

app = rx.App()
app.add_page(index)