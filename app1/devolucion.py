import reflex as rx
import mysql.connector
from datetime import date

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="bloq1234",
        database="bdmysql",
        port=3306
    )

class DevolucionState(rx.State):
    id_libro: str = ""
    mensaje: str = ""
    usuario: str = "usuario_demo"  # ⚠️ Temporal

    @rx.var
    def color_mensaje(self) -> str:
        return "green.600" if self.mensaje.startswith("✅") else "red.600"

    async def devolver_libro(self):
        if not self.id_libro.isdigit():
            self.mensaje = "❌ El ID del libro debe ser un número."
            return

        conexion = None
        cursor = None

        try:
            conexion = get_connection()
            cursor = conexion.cursor()

            # Verificar si hay préstamo activo
            cursor.execute("""
                SELECT p.id, l.titulo FROM prestamos p
                JOIN libros l ON p.id_libro = l.id
                WHERE p.id_libro = %s AND p.usuario = %s AND p.devuelto = FALSE
            """, (self.id_libro, self.usuario))

            resultado = cursor.fetchone()

            if not resultado:
                self.mensaje = "❌ No hay préstamo activo para este usuario y libro."
            else:
                id_prestamo, titulo = resultado
                hoy = date.today()

                # Actualizar estado del préstamo y del libro
                cursor.execute("""
                    UPDATE prestamos
                    SET devuelto = TRUE, fecha_devolucion = %s
                    WHERE id = %s
                """, (hoy, id_prestamo))

                cursor.execute("UPDATE libros SET disponible = TRUE WHERE id = %s", (self.id_libro,))
                conexion.commit()
                self.mensaje = f"✅ Libro '{titulo}' devuelto exitosamente el {hoy}."

        except mysql.connector.Error as err:
            self.mensaje = f"❌ Error en la base de datos: {err}"

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

@rx.page(route="/devolucion", title="Devolver Libro")
def devolucion() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("📚 Devolver Libro", size="5"),
            rx.input(
                placeholder="Ingrese el ID del libro",
                on_change=DevolucionState.set_id_libro,
                value=DevolucionState.id_libro,
                width="300px"
            ),
            rx.button(
                "Devolver",
                on_click=DevolucionState.devolver_libro,
                color_scheme="green"
            ),
            rx.text(
                DevolucionState.mensaje,
                color=DevolucionState.color_mensaje,
                font_weight="bold"
            ),
            spacing="4",
            padding="6",
            box_shadow="md",
            border_radius="xl",
            bg="white",
            width="100%",
            max_width="400px"
        ),
        min_height="100vh",
        bg="gray.50"
    )

app = rx.App()
app.add_page(devolucion)
