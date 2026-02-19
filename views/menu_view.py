"""
Pantalla de menú principal del juego.
"""

import arcade
import math
from constants import *


class FloatingGem:
    """Una gema decorativa que flota en el fondo del menú."""

    def __init__(self, x, y, color, size, speed, phase):
        self.x = x
        self.y = y
        self.base_y = y
        self.color = color
        self.size = size
        self.speed = speed
        self.phase = phase
        self.time = 0

    def update(self, delta_time):
        self.time += delta_time
        self.y = self.base_y + math.sin(self.time * self.speed + self.phase) * GEM_FLOAT_RANGE

    def draw(self):
        # Dibujar una gema como un diamante (rombo)
        points = [
            (self.x, self.y + self.size),
            (self.x + self.size * 0.6, self.y),
            (self.x, self.y - self.size * 0.4),
            (self.x - self.size * 0.6, self.y),
        ]
        arcade.draw_polygon_filled(points, self.color)
        # Brillo
        highlight_color = (
            min(255, self.color[0] + 80),
            min(255, self.color[1] + 80),
            min(255, self.color[2] + 80),
        )
        small_points = [
            (self.x, self.y + self.size * 0.6),
            (self.x + self.size * 0.3, self.y + self.size * 0.1),
            (self.x, self.y - self.size * 0.1),
            (self.x - self.size * 0.3, self.y + self.size * 0.1),
        ]
        arcade.draw_polygon_filled(small_points, highlight_color)


class Button:
    """Botón clickeable simple."""

    def __init__(self, x, y, width, height, text, color, hover_color, text_color=COLOR_TEXT_LIGHT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self):
        current_color = self.hover_color if self.is_hovered else self.color
        # Sombra
        arcade.draw_rectangle_filled(
            self.x + 3, self.y - 3, self.width, self.height, (0, 0, 0, 50)
        )
        # Botón
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, current_color)
        arcade.draw_rectangle_outline(
            self.x, self.y, self.width, self.height, (255, 255, 255, 100), 2
        )
        # Texto
        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            self.text_color,
            font_size=FONT_SIZE_BODY,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

    def check_hover(self, mouse_x, mouse_y):
        self.is_hovered = (
            abs(mouse_x - self.x) <= self.width / 2
            and abs(mouse_y - self.y) <= self.height / 2
        )
        return self.is_hovered

    def is_clicked(self, mouse_x, mouse_y):
        return (
            abs(mouse_x - self.x) <= self.width / 2
            and abs(mouse_y - self.y) <= self.height / 2
        )


class MenuView(arcade.View):
    """Vista del menú principal."""

    def __init__(self):
        super().__init__()
        self.floating_gems = []
        self.title_time = 0

        # --- Definir geometría del panel ---
        self.panel_center_y = SCREEN_HEIGHT // 2
        self.panel_height = 560
        self.panel_width = 600
        self.panel_top = self.panel_center_y + self.panel_height // 2
        self.panel_bottom = self.panel_center_y - self.panel_height // 2

        # --- Posiciones Y de contenido (de arriba hacia abajo) ---
        self.title_y = self.panel_top - 60
        self.subtitle_y = self.title_y - 55
        self.desc_start_y = self.subtitle_y - 65
        self.play_btn_y = self.panel_bottom + 130
        self.info_btn_y = self.panel_bottom + 55

        # --- Botones (sin emojis) ---
        self.play_button = Button(
            SCREEN_WIDTH // 2, self.play_btn_y,
            250, 60, "Jugar", COLOR_SUCCESS, (80, 200, 120)
        )
        self.info_button = Button(
            SCREEN_WIDTH // 2, self.info_btn_y,
            250, 60, "Informacion", COLOR_PRIMARY, (90, 150, 200)
        )

        # --- Crear gemas flotantes decorativas ---
        import random
        for _ in range(12):
            gem = FloatingGem(
                x=random.randint(50, SCREEN_WIDTH - 50),
                y=random.randint(100, SCREEN_HEIGHT - 100),
                color=random.choice(GEM_COLORS),
                size=random.randint(15, 30),
                speed=random.uniform(0.5, 1.5),
                phase=random.uniform(0, math.pi * 2),
            )
            self.floating_gems.append(gem)

    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND)

    def on_draw(self):
        self.clear()

        # Dibujar fondo degradado
        for i in range(SCREEN_HEIGHT):
            ratio = i / SCREEN_HEIGHT
            r = int(COLOR_BACKGROUND[0] * (1 - ratio * 0.15))
            g = int(COLOR_BACKGROUND[1] * (1 - ratio * 0.1))
            b = int(COLOR_BACKGROUND[2] * (1 - ratio * 0.05))
            arcade.draw_line(0, i, SCREEN_WIDTH, i, (r, g, b))

        # Dibujar gemas flotantes
        for gem in self.floating_gems:
            gem.draw()

        # Panel central semi-transparente (centrado)
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, self.panel_center_y,
            self.panel_width, self.panel_height,
            (255, 255, 255, 180)
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH // 2, self.panel_center_y,
            self.panel_width, self.panel_height,
            COLOR_PRIMARY, 3
        )

        # Título con efecto de onda
        title_y = self.title_y + math.sin(self.title_time * 2) * 5
        arcade.draw_text(
            "NumWorld",
            SCREEN_WIDTH // 2,
            title_y,
            COLOR_PRIMARY,
            font_size=FONT_SIZE_TITLE,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # Subtítulo
        arcade.draw_text(
            "Aventura Numerica",
            SCREEN_WIDTH // 2,
            self.subtitle_y,
            COLOR_ACCENT,
            font_size=FONT_SIZE_SUBTITLE,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # Descripción
        desc_lines = [
            "Bienvenido a una aventura llena de",
            "gemas magicas y numeros divertidos!",
            "",
            "Explora 5 mundos diferentes y",
            "demuestra tus habilidades numericas.",
        ]
        for i, line in enumerate(desc_lines):
            arcade.draw_text(
                line,
                SCREEN_WIDTH // 2,
                self.desc_start_y - i * 28,
                COLOR_TEXT_DARK,
                font_size=FONT_SIZE_BODY,
                anchor_x="center",
                anchor_y="center",
            )

        # Botones
        self.play_button.draw()
        self.info_button.draw()

        # Pie de página
        arcade.draw_text(
            "Herramienta de observacion educativa - No es un instrumento de diagnostico",
            SCREEN_WIDTH // 2,
            30,
            (150, 150, 170),
            font_size=FONT_SIZE_SMALL - 2,
            anchor_x="center",
            anchor_y="center",
        )

    def on_update(self, delta_time):
        self.title_time += delta_time
        for gem in self.floating_gems:
            gem.update(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        self.play_button.check_hover(x, y)
        self.info_button.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_button.is_clicked(x, y):
            from views.player_info_view import PlayerInfoView
            self.window.show_view(PlayerInfoView())
        elif self.info_button.is_clicked(x, y):
            from views.info_view import InfoView
            self.window.show_view(InfoView())