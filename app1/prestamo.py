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

# 📚 Lógica para prestar un libro
def prestar_libro(id_libro, usuario):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT disponible FROM libros WHERE id = %s", (id_libro,))
    resultado = cursor.fetchone()

    if not resultado:
        mensaje = "❌ Libro no encontrado."
    elif resultado[0] == 0:
        mensaje = "⚠️ El libro no está disponible para préstamo."
    else:
        cursor.execute(
            "INSERT INTO prestamos (id_libro, usuario, devuelto) VALUES (%s, %s, 0)",
            (id_libro, usuario),
        )
        cursor.execute("UPDATE libros SET disponible = 0 WHERE id = %s", (id_libro,))
        conexion.commit()
        mensaje = "✅ Préstamo realizado exitosamente."

    cursor.close()
    conexion.close()
    return mensaje

# 🧠 Estado de la interfaz
class PrestamoState(rx.State):
    id_libro: int = 0
    usuario: str = ""
    mensaje: str = ""

    def hacer_prestamo(self):
        self.mensaje = prestar_libro(self.id_libro, self.usuario)

# 🖼 Interfaz gráfica
def vista_prestamo():
    return rx.center(
        rx.vstack(
            rx.heading("📚 Realizar Préstamo de Libro"),
            rx.input(
                placeholder="ID del libro",
                on_change=lambda e: PrestamoState.set_id_libro(int(e)),
            ),
            rx.input(
                placeholder="Usuario",
                on_change=PrestamoState.set_usuario,
            ),
            rx.button("Prestar", on_click=PrestamoState.hacer_prestamo),
            rx.text(PrestamoState.mensaje, color="#000000", font_weight="bold"),
            spacing="4",
        ),
        padding="40px",
    )

# 🚀 App Reflex
app = rx.App()
app.add_page(vista_prestamo)
