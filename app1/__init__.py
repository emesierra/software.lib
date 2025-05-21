from reflex import App
from .app1 import index  # tu página principal de login
from .registro import registro  # la página de registro que creamos

app = App()

# Agregar páginas
app.add_page(index, route="/")          # ruta principal para login
app.add_page(registro, route="/registro")  # ruta para registro

# Definir la página inicial (opcional, normalmente la principal es '/')

