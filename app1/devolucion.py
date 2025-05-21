import reflex as rx
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="bloq1234",
        database="bdmysql",
        port=3306
    )

# 🔁 Lógica para devolver un libro
def devolver_libro(id_prestamo, usuario):
    conexion = get_connection()
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
    id_prestamo: int = 0
    usuario: str = ""
    mensaje: str = ""

    def hacer_devolucion(self):
        self.mensaje = devolver_libro(self.id_prestamo, self.usuario)

# 🖼 Interfaz gráfica
def vista_devolucion():
    return rx.center(
        rx.vstack(
            rx.heading("🔁 Devolver Libro"),
            rx.input(
                placeholder="ID del préstamo",
                on_change=lambda e: DevolucionState.set_id_prestamo(int(e)),
            ),
            rx.input(
                placeholder="Usuario",
                on_change=DevolucionState.set_usuario,
            ),
            rx.button("Devolver", on_click=DevolucionState.hacer_devolucion),
            rx.text(DevolucionState.mensaje, color="#000000", font_weight="bold"),
            spacing="4",
        ),
        padding="40px",
    )

# 🚀 App Reflex
app = rx.App()
app.add_page(vista_devolucion)
