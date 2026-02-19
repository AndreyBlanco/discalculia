"""
NumWorld - Aventura Numérica

"""

import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from views.menu_view import MenuView


def main():
    """Función principal que inicia el juego."""
    # Crear ventana del juego
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
    window.set_location(100, 50)

    # Inicializar el tracker como atributo de la ventana (se configurará al iniciar partida)
    window.tracker = None

    # Mostrar el menú principal
    menu_view = MenuView()
    window.show_view(menu_view)

    # Iniciar el bucle del juego
    arcade.run()


if __name__ == "__main__":
    main()