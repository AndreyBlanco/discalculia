"""
Nivel 3: Comparación de Magnitudes
El jugador debe identificar cuál de dos grupos tiene más gemas.
"""

import arcade
import random
import math
from constants import *
from views.level_base import LevelBase, Gem, AnswerButton


class GemGroup:
    """Representa un grupo de gemas para comparación."""

    def __init__(self, center_x, center_y, count, area_width, area_height, color):
        self.center_x = center_x
        self.center_y = center_y
        self.count = count
        self.gems = []
        self.is_hovered = False
        self.state = "normal"  # "normal", "correct", "incorrect"
        self.area_width = area_width
        self.area_height = area_height
        self.border_color = COLOR_PRIMARY

        # Generar posiciones de gemas dentro del área
        half_w = area_width // 2 - 40
        half_h = area_height // 2 - 60
        positions = []
        for _ in range(count):
            attempts = 0
            while attempts < 80:
                x = center_x + random.randint(-half_w, half_w)
                y = center_y + random.randint(-half_h, half_h)
                too_close = False
                for px, py in positions:
                    if math.hypot(x - px, y - py) < GEM_SIZE * 2:
                        too_close = True
                        break
                if not too_close:
                    positions.append((x, y))
                    break
                attempts += 1
            else:
                positions.append((
                    center_x + random.randint(-half_w, half_w),
                    center_y + random.randint(-half_h, half_h),
                ))

        for x, y in positions:
            gem = Gem(x, y, color, GEM_SIZE)
            gem.start_sparkle()
            self.gems.append(gem)

    def update(self, delta_time):
        for gem in self.gems:
            gem.update(delta_time)

    def draw(self):
        # Fondo del grupo
        if self.state == "correct":
            bg_color = (*COLOR_SUCCESS, 40)
            self.border_color = COLOR_SUCCESS
        elif self.state == "incorrect":
            bg_color = (*COLOR_ERROR, 40)
            self.border_color = COLOR_ERROR
        elif self.is_hovered:
            bg_color = (*COLOR_SECONDARY, 40)
            self.border_color = COLOR_SECONDARY
        else:
            bg_color = (255, 255, 255, 60)
            self.border_color = COLOR_PRIMARY

        arcade.draw_rectangle_filled(
            self.center_x, self.center_y,
            self.area_width, self.area_height,
            bg_color,
        )
        arcade.draw_rectangle_outline(
            self.center_x, self.center_y,
            self.area_width, self.area_height,
            self.border_color, 3,
        )

        # Dibujar gemas
        for gem in self.gems:
            gem.draw()

    def contains_point(self, px, py):
        return (
            abs(px - self.center_x) <= self.area_width / 2
            and abs(py - self.center_y) <= self.area_height / 2
        )

    def check_hover(self, mx, my):
        self.is_hovered = self.contains_point(mx, my)
        return self.is_hovered


class Level3View(LevelBase):
    """Nivel de comparación de magnitudes."""

    def __init__(self):
        super().__init__(level_number=3)
        self.group_left = None
        self.group_right = None
        self.correct_side = ""  # "left" o "right"
        self.answered = False
        self.trial_number = 0
        self.setup_trial()

    def setup_trial(self):
        """Configura un nuevo intento de comparación."""
        self.trial_number += 1
        self.answered = False
        self.state = "playing"

        # Generar dos cantidades diferentes
        count_a = random.randint(2, 9)
        count_b = random.randint(2, 9)
        while count_a == count_b:
            count_b = random.randint(2, 9)

        # Decidir posiciones
        group_width = SCREEN_WIDTH // 2 - 60
        group_height = SCREEN_HEIGHT - 220

        color_left = random.choice(GEM_COLORS)
        color_right = random.choice(GEM_COLORS)
        while color_right == color_left:
            color_right = random.choice(GEM_COLORS)

        self.group_left = GemGroup(
            center_x=SCREEN_WIDTH // 4,
            center_y=SCREEN_HEIGHT // 2 - 20,
            count=count_a,
            area_width=group_width,
            area_height=group_height,
            color=color_left,
        )

        self.group_right = GemGroup(
            center_x=3 * SCREEN_WIDTH // 4,
            center_y=SCREEN_HEIGHT // 2 - 20,
            count=count_b,
            area_width=group_width,
            area_height=group_height,
            color=color_right,
        )

        if count_a > count_b:
            self.correct_side = "left"
        else:
            self.correct_side = "right"

        # Registro de datos
        tracker = getattr(self.window, 'tracker', None)
        if tracker:
            tracker.start_trial(
                self.level_number,
                self.trial_number,
                self.correct_side,
            )

    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND)

    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND
        )

        self.draw_hud()

        # Instrucción
        arcade.draw_text(
            "¿Qué grupo tiene MÁS gemas? ¡Haz clic en él!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 80,
            COLOR_PRIMARY,
            font_size=FONT_SIZE_BODY,
            anchor_x="center",
            bold=True,
        )

        # Etiquetas
        arcade.draw_text(
            "Grupo A",
            SCREEN_WIDTH // 4,
            SCREEN_HEIGHT - 110,
            COLOR_ACCENT,
            font_size=FONT_SIZE_BODY,
            anchor_x="center",
            bold=True,
        )
        arcade.draw_text(
            "Grupo B",
            3 * SCREEN_WIDTH // 4,
            SCREEN_HEIGHT - 110,
            COLOR_ACCENT,
            font_size=FONT_SIZE_BODY,
            anchor_x="center",
            bold=True,
        )

        # Separador central
        arcade.draw_line(
            SCREEN_WIDTH // 2, 80,
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130,
            (200, 200, 220), 2,
        )
        arcade.draw_text(
            "VS",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            COLOR_SECONDARY,
            font_size=FONT_SIZE_SUBTITLE,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # Dibujar grupos
        if self.group_left:
            self.group_left.draw()
        if self.group_right:
            self.group_right.draw()

        # Feedback
        self.draw_feedback()

    def on_update(self, delta_time):
        if self.group_left:
            self.group_left.update(delta_time)
        if self.group_right:
            self.group_right.update(delta_time)
        self.update_feedback(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.answered:
            if self.group_left:
                self.group_left.check_hover(x, y)
            if self.group_right:
                self.group_right.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.state == "feedback" or self.answered:
            return

        clicked_side = None
        if self.group_left and self.group_left.contains_point(x, y):
            clicked_side = "left"
        elif self.group_right and self.group_right.contains_point(x, y):
            clicked_side = "right"

        if clicked_side:
            self.answered = True
            is_correct = clicked_side == self.correct_side

            # Registrar respuesta
            tracker = getattr(self.window, 'tracker', None)
            if tracker:
                tracker.record_answer(clicked_side)

            # Feedback visual
            if clicked_side == "left":
                self.group_left.state = "correct" if is_correct else "incorrect"
                if not is_correct:
                    self.group_right.state = "correct"
            else:
                self.group_right.state = "correct" if is_correct else "incorrect"
                if not is_correct:
                    self.group_left.state = "correct"

            self.show_feedback(is_correct)