"""
Pantalla para recopilar información básica del jugador.
"""

import arcade
from constants import *


class PlayerInfoView(arcade.View):
    """Vista para ingresar el nombre y edad del jugador."""

    def __init__(self):
        super().__init__()
        self.player_name = ""
        self.player_age = ""
        self.active_field = "name"
        self.error_message = ""
        self.cursor_visible = True
        self.cursor_timer = 0

        # --- Panel ---
        self.panel_cx = SCREEN_WIDTH // 2
        self.panel_cy = SCREEN_HEIGHT // 2
        self.panel_w = 500
        self.panel_h = 420
        self.panel_top = self.panel_cy + self.panel_h // 2
        self.panel_bottom = self.panel_cy - self.panel_h // 2

        # --- Posiciones centradas con márgenes iguales ---
        # Margen superior (panel_top - title) = Margen inferior (button - panel_bottom) = 70
        self.title_y = self.panel_cy + 140
        self.name_label_y = self.panel_cy + 72
        self.name_field_y = self.panel_cy + 42
        self.age_label_y = self.panel_cy - 22
        self.age_field_y = self.panel_cy - 52
        self.button_y = self.panel_cy - 140
        self.error_y = self.button_y - 35

        # --- Campos ---
        self.field_width = 380
        self.field_height = 40

        # --- Instrucción fuera del panel ---
        self.instruction_y = self.panel_bottom - 35

    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND)

    def on_draw(self):
        self.clear()

        # Panel central
        arcade.draw_rectangle_filled(
            self.panel_cx, self.panel_cy,
            self.panel_w, self.panel_h,
            (255, 255, 255, 230)
        )
        arcade.draw_rectangle_outline(
            self.panel_cx, self.panel_cy,
            self.panel_w, self.panel_h,
            COLOR_PRIMARY, 3
        )

        # Título
        arcade.draw_text(
            "¡Cuéntanos sobre ti!",
            self.panel_cx,
            self.title_y,
            COLOR_PRIMARY,
            font_size=FONT_SIZE_SUBTITLE,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # --- Campo de nombre ---
        name_color = COLOR_PRIMARY if self.active_field == "name" else (180, 180, 200)
        arcade.draw_text(
            "Tu nombre:",
            self.panel_cx - self.field_width // 2,
            self.name_label_y,
            COLOR_TEXT_DARK,
            font_size=FONT_SIZE_BODY,
        )
        arcade.draw_rectangle_outline(
            self.panel_cx, self.name_field_y,
            self.field_width, self.field_height,
            name_color, 2
        )
        arcade.draw_rectangle_filled(
            self.panel_cx, self.name_field_y,
            self.field_width - 4, self.field_height - 4,
            (245, 245, 255)
        )
        cursor_name = "|" if self.active_field == "name" and self.cursor_visible else ""
        arcade.draw_text(
            self.player_name + cursor_name,
            self.panel_cx - self.field_width // 2 + 10,
            self.name_field_y - 8,
            COLOR_TEXT_DARK,
            font_size=FONT_SIZE_BODY,
        )

        # --- Campo de edad ---
        age_color = COLOR_PRIMARY if self.active_field == "age" else (180, 180, 200)
        arcade.draw_text(
            "Tu edad:",
            self.panel_cx - self.field_width // 2,
            self.age_label_y,
            COLOR_TEXT_DARK,
            font_size=FONT_SIZE_BODY,
        )
        arcade.draw_rectangle_outline(
            self.panel_cx, self.age_field_y,
            self.field_width, self.field_height,
            age_color, 2
        )
        arcade.draw_rectangle_filled(
            self.panel_cx, self.age_field_y,
            self.field_width - 4, self.field_height - 4,
            (245, 245, 255)
        )
        cursor_age = "|" if self.active_field == "age" and self.cursor_visible else ""
        arcade.draw_text(
            self.player_age + cursor_age,
            self.panel_cx - self.field_width // 2 + 10,
            self.age_field_y - 8,
            COLOR_TEXT_DARK,
            font_size=FONT_SIZE_BODY,
        )

        # --- Botón comenzar ---
        btn_color = COLOR_SUCCESS if (self.player_name and self.player_age) else (180, 180, 180)
        arcade.draw_rectangle_filled(
            self.panel_cx, self.button_y, 200, 50, btn_color
        )
        arcade.draw_rectangle_outline(
            self.panel_cx, self.button_y, 200, 50, (255, 255, 255, 100), 2
        )
        arcade.draw_text(
            "¡Comenzar!",
            self.panel_cx,
            self.button_y,
            COLOR_TEXT_LIGHT,
            font_size=FONT_SIZE_BODY,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # --- Mensaje de error ---
        if self.error_message:
            arcade.draw_text(
                self.error_message,
                self.panel_cx,
                self.error_y,
                COLOR_ERROR,
                font_size=FONT_SIZE_SMALL,
                anchor_x="center",
                anchor_y="center",
            )

        # --- Instrucción (fuera del panel, abajo) ---
        arcade.draw_text(
            "Usa Tab para cambiar de campo - Enter para continuar",
            self.panel_cx,
            self.instruction_y,
            (150, 150, 170),
            font_size=FONT_SIZE_SMALL - 2,
            anchor_x="center",
            anchor_y="center",
        )

    def on_update(self, delta_time):
        self.cursor_timer += delta_time
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.TAB:
            self.active_field = "age" if self.active_field == "name" else "name"
            self.error_message = ""
        elif key == arcade.key.ENTER or key == arcade.key.RETURN:
            self.try_start_game()
        elif key == arcade.key.BACKSPACE:
            if self.active_field == "name" and self.player_name:
                self.player_name = self.player_name[:-1]
            elif self.active_field == "age" and self.player_age:
                self.player_age = self.player_age[:-1]

    def on_text(self, text):
        if text in ('\r', '\n', '\t'):
            return
        if self.active_field == "name" and len(self.player_name) < 20:
            if text.isalpha() or text == " ":
                self.player_name += text
        elif self.active_field == "age" and len(self.player_age) < 2:
            if text.isdigit():
                self.player_age += text

    def on_mouse_press(self, x, y, button, modifiers):
        half_w = self.field_width // 2
        half_h = self.field_height // 2

        # Click en campo de nombre
        if (self.panel_cx - half_w <= x <= self.panel_cx + half_w
                and self.name_field_y - half_h <= y <= self.name_field_y + half_h):
            self.active_field = "name"
        # Click en campo de edad
        elif (self.panel_cx - half_w <= x <= self.panel_cx + half_w
              and self.age_field_y - half_h <= y <= self.age_field_y + half_h):
            self.active_field = "age"
        # Click en botón comenzar
        elif (self.panel_cx - 100 <= x <= self.panel_cx + 100
              and self.button_y - 25 <= y <= self.button_y + 25):
            self.try_start_game()

    def try_start_game(self):
        if not self.player_name.strip():
            self.error_message = "Por favor, escribe tu nombre"
            self.active_field = "name"
        elif not self.player_age.strip():
            self.error_message = "Por favor, escribe tu edad"
            self.active_field = "age"
        else:
            from views.instruction_view import InstructionView
            from data_tracker import DataTracker

            tracker = DataTracker()
            tracker.set_player_info(self.player_name.strip(), self.player_age.strip())
            self.window.tracker = tracker
            self.window.show_view(InstructionView(level=1))