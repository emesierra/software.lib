import reflex as rx

@rx.page(route="/menu", title="Menú Biblioteca")
def menu() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("¿Qué deseas hacer?", size="2", margin_bottom="2rem"),
            
            
            rx.link(
                rx.button("📚 Alquilar un libro", width="300px", height="50px", margin_bottom="1rem"),
                href="/devolucion"
            ),
            rx.link(
                rx.button("🔄 Devolver un libro", width="300px", height="50px"),
                href="/devolucion"
            ),
            
            rx.link("Volver al login", href="/devolucion", color="blue", margin_top="2rem"),
        ),
        height="100vh"
    )

app = rx.App()
app.add_page(menu)