import reflex as rx

@rx.page(route="/menu", title="Menú Biblioteca")
def menu() -> rx.Component:
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading("¿Qué deseas hacer?", size="5", margin_bottom="2rem", text_align="center", color="black"),

                rx.link(
                    rx.button("Alquilar un libro", width="300px", height="50px", margin_bottom="1rem", color="white", background_color="#128ADA"),
                    href="/prestamo"
                ),
                rx.link(
                    rx.button("Devolver un libro", width="300px", height="50px", margin_bottom="1rem", color="white", background_color="#128ADA"),
                    href="/devolucion"
                ),

                rx.link(
                    "Volver al login",
                    href="/",
                    color="#0059FF",
                    margin_top="1rem"
                ),
            ),
            background_color="#FFFFFF",  # Azul oscuro
            border_radius="16px",
            padding="32px",
            shadow="lg",
            width="350px",  # Caja más pequeña y centrada
        ),
        height="100vh",  # Centrado vertical
        background="#011E26"  # Fondo general (azul oscuro más moderno)
    )

app = rx.App()
app.add_page(menu)
