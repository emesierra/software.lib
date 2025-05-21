import reflex as rx
import mysql.connector
from datetime import date

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bloq1234",
    database="bdmysql"
)
cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_libro FROM prestamos WHERE id = %s AND usuario = %s AND devuelto = 0",
        (id_prestamo, usuario)
    )
    resultado = cursor.fetchone()

    if resultado:
        id_libro = resultado[0]

        cursor.execute("UPDATE prestamos SET devuelto = 1 WHERE id = %s", (id_prestamo,))
        cursor.execute("UPDATE libros SET disponible = 1 WHERE id = %s", (id_libro,))
        conexion.commit()
        mensaje = "✅ Libro devuelto exitosamente."
    else:
        mensaje = "⚠️ Préstamo no válido o ya fue devuelto."

    cursor.close()
    conexion.close()
    return mensaje

# 🧠 Estado para devolución
class DevolucionState(rx.State):
    usuario: str = ""
    id_libro: str = ""
    mensaje: str = ""
    usuario: str = "usuario_demo"  # ⚠️ Temporal

    @rx.var
    def usuario_var(self) -> str:
        return self.usuario

    @rx.var
    def id_libro_var(self) -> str:
        return self.id_libro

    @rx.var
    def mensaje_var(self) -> str:
        return self.mensaje

    @rx.event
    def set_usuario(self, valor: str):
        self.usuario = valor

    @rx.event
    def set_id_libro(self, valor: str):
        self.id_libro = valor

    @rx.event
    def devolver_libro(self):
        query = "SELECT * FROM prestamos WHERE usuario=%s AND id_libro=%s AND devuelto=0"
        cursor.execute(query, (self.usuario, self.id_libro))
        prestamo = cursor.fetchone()

        if prestamo:
            update_query = "UPDATE prestamos SET devuelto=1 WHERE usuario=%s AND id_libro=%s AND devuelto=0"
            cursor.execute(update_query, (self.usuario, self.id_libro))
            conexion.commit()
            self.mensaje = "✅ Libro devuelto exitosamente."
        else:
            self.mensaje = "❌ No se encontró un préstamo activo con esos datos."

@rx.page(route="/devolucion", title="Devolver Libro")
def devolucion(state: DevolucionState) -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Devolver Libro", size="3"),
            rx.input(
                placeholder="Nombre del usuario",
                value=state.usuario,
                on_change=state.set_usuario,
                width="300px"
            ),
            rx.input(
                placeholder="ID del libro",
                value=state.id_libro,
                on_change=state.set_id_libro,
                width="300px"
            ),
            rx.button("Devolver", on_click=state.devolver_libro, width="300px"),
            rx.text(state.mensaje, margin_top="1rem", color="green"),
            rx.link("Volver al menú", href="/menu", color="blue", margin_top="1rem"),
        ),
        height="100vh"
    )

# 🚀 App Reflex
app = rx.App()
app.add_page(devolucion)
