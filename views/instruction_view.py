"""
Pantalla de instrucciones antes de cada nivel.
"""

import arcade
import math
from constants import *


class InstructionView(arcade.View):
    """Vista que muestra las instrucciones antes de comenzar un nivel."""

    def __init__(self, level):
        super().__init__()
        self.level = level
        self.animation_time = 0
        self.ready = False
        self.ready_timer = 0

        # --- Panel ---
        self.panel_cx = SCREEN_WIDTH // 2
        self.panel_cy = SCREEN_HEIGHT // 2
        self.panel_w = 650
        self.panel_h = 520
        self.panel_top = self.panel_cy + self.panel_h // 2
        self.panel_bottom = self.panel_cy - self.panel_h // 2

        # --- Posiciones de contenido ---
        self.level_number_y = self.panel_top - 35
        self.level_name_y = self.panel_top - 75
        self.instructions_start_y = self.panel_top - 130
        self.button_y = self.panel_bottom + 50

    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND)

    def on_draw(self):
        self.clear()

        # Fondo decorativo (círculos)
        for i in range(0, SCREEN_WIDTH, 60):
            y_offset = math.sin(self.animation_time * 2 + i * 0.05) * 20
            color_top = GEM_COLORS[i % len(GEM_COLORS)]
            color_bot = GEM_COLORS[(i + 3) % len(GEM_COLORS)]
            arcade.draw_circle_filled(
                i, 50 + y_offset, 8, (*color_top, 80)
            )
            arcade.draw_circle_filled(
                i, SCREEN_HEIGHT - 50 - y_offset, 8, (*color_bot, 80)
            )

        # Panel central
        arcade.draw_rectangle_filled(
            self.panel_cx, self.panel_cy,
            self.panel_w, self.panel_h,
            (255, 255, 255, 230)
        )
        arcade.draw_rectangle_outline(
            self.panel_cx, self.panel_cy,
            self.panel_w, self.panel_h,
            COLOR_ACCENT, 3
        )

        # Número de nivel
        arcade.draw_text(
            f"Nivel {self.level} de {TOTAL_LEVELS}",
            self.panel_cx,
            self.level_number_y,
            COLOR_ACCENT,
            font_size=FONT_SIZE_BODY,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # Nombre del nivel (sin emojis)
        level_name = LEVEL_NAMES.get(self.level, f"Nivel {self.level}")
        arcade.draw_text(
            level_name,
            self.panel_cx,
            self.level_name_y,
            COLOR_PRIMARY,
            font_size=FONT_SIZE_SUBTITLE + 4,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # Instrucciones
        instructions = LEVEL_INSTRUCTIONS.get(self.level, ["¡Prepárate!"])
        for i, line in enumerate(instructions):
            arcade.draw_text(
                line,
                self.panel_cx,
                self.instructions_start_y - i * 32,
                COLOR_TEXT_DARK,
                font_size=FONT_SIZE_BODY,
                anchor_x="center",
                anchor_y="center",
            )

        # Botón de "Empezar"
        if self.ready:
            pulse = math.sin(self.animation_time * 4) * 0.05 + 1.0
            btn_width = int(200 * pulse)
            btn_height = int(50 * pulse)
            arcade.draw_rectangle_filled(
                self.panel_cx, self.button_y,
                btn_width, btn_height, COLOR_SECONDARY
            )
            arcade.draw_rectangle_outline(
                self.panel_cx, self.button_y,
                btn_width, btn_height, (255, 255, 255, 150), 2
            )
            arcade.draw_text(
                "Empezar",
                self.panel_cx,
                self.button_y,
                COLOR_TEXT_LIGHT,
                font_size=FONT_SIZE_BODY,
                anchor_x="center",
                anchor_y="center",
                bold=True,
            )
        else:
            arcade.draw_text(
                "Preparando...",
                self.panel_cx,
                self.button_y,
                (180, 180, 200),
                font_size=FONT_SIZE_BODY,
                anchor_x="center",
                anchor_y="center",
            )

    def on_update(self, delta_time):
        self.animation_time += delta_time
        if not self.ready:
            self.ready_timer += delta_time
            if self.ready_timer >= 1.5:
                self.ready = True

    def on_mouse_press(self, x, y, button, modifiers):
        if self.ready:
            self.start_level()

    def start_level(self):
        """Inicia el nivel correspondiente."""
        if self.level == 1:
            from views.level1_subitizing import Level1View
            self.window.show_view(Level1View())
        elif self.level == 2:
            from views.level2_counting import Level2View
            self.window.show_view(Level2View())
        elif self.level == 3:
            from views.level3_comparison import Level3View
            self.window.show_view(Level3View())
        elif self.level == 4:
            from views.level4_estimation import Level4View
            self.window.show_view(Level4View())
        elif self.level == 5:
            from views.level5_sequencing import Level5View
            self.window.show_view(Level5View())