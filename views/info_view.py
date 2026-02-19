"""
Pantalla de información sobre el juego.
"""

import arcade
from constants import *


class InfoView(arcade.View):
    """Vista con información sobre el juego y su propósito."""

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND)

    def on_draw(self):
        self.clear()

        # Panel de fondo
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 800, 650, (255, 255, 255, 220)
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 800, 650, COLOR_PRIMARY, 3
        )

        # Título
        arcade.draw_text(
            "Sobre NumWorld",
            SCREEN_WIDTH // 2,
            680,
            COLOR_PRIMARY,
            font_size=FONT_SIZE_SUBTITLE + 4,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        info_lines = [
            "NumWorld es una herramienta de observacion ludica disenada para ayudar",
            "a los educadores a identificar posibles indicadores tempranos de",
            "dificultades con los numeros en ninos pequenos.",
            "",
            "El juego consta de 5 niveles:",
            "  1. Subitizacion -- Reconocer cantidades de un vistazo",
            "  2. Conteo -- Contar objetos con precision",
            "  3. Comparacion -- Identificar cual grupo tiene mas",
            "  4. Estimacion -- Aproximar cantidades grandes",
            "  5. Secuenciacion -- Ordenar numeros de menor a mayor",
            "",
            "Al finalizar, se genera un resumen observacional con datos",
            "de precision, tiempo de respuesta y patrones de error.",
            "",
            "IMPORTANTE: Este juego NO es una herramienta de diagnostico.",
            "Los resultados deben ser interpretados por un profesional",
            "calificado en el contexto de una evaluacion completa.",
            "",
            "Haz clic en cualquier lugar para volver al menu.",
        ]

        for i, line in enumerate(info_lines):
            color = COLOR_ERROR if "IMPORTANTE" in line or "NO es" in line else COLOR_TEXT_DARK
            arcade.draw_text(
                line,
                SCREEN_WIDTH // 2,
                620 - i * 30,
                color,
                font_size=FONT_SIZE_SMALL,
                anchor_x="center",
                anchor_y="center",
            )

    def on_mouse_press(self, x, y, button, modifiers):
        from views.menu_view import MenuView
        self.window.show_view(MenuView())