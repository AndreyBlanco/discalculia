"""
Nivel 2: Conteo
El jugador debe contar las gemas visibles sin límite de tiempo.
"""

import arcade
import random
import math
from constants import *
from views.level_base import LevelBase, Gem, AnswerButton


class Level2View(LevelBase):
    """Nivel de conteo: contar gemas visibles con calma."""

    def __init__(self):
        super().__init__(level_number=2)
        self.correct_count = 0
        self.answered = False
        self.gems_clicked = []
        self.trial_number = 0
        self.setup_trial()

    def setup_trial(self):
        """Configura un nuevo intento de conteo."""
        self.trial_number += 1
        self.answered = False
        self.gems_clicked = []
        self.state = "playing"

        # Cantidades más variadas (5-12)
        self.correct_count = random.randint(5, 12)

        # Crear gemas distribuidas
        self.gems = []
        margin = 80
        area_left = margin
        area_right = SCREEN_WIDTH - margin
        area_bottom = 180
        area_top = SCREEN_HEIGHT - 120

        positions = []
        for _ in range(self.correct_count):
            attempts = 0
            while attempts < 100:
                x = random.randint(area_left, area_right)
                y = random.randint(area_bottom, area_top)
                too_close = False
                for px, py in positions:
                    if math.hypot(x - px, y - py) < GEM_SIZE * 2.2:
                        too_close = True
                        break
                if not too_close:
                    positions.append((x, y))
                    break
                attempts += 1
            else:
                positions.append((random.randint(area_left, area_right),
                                  random.randint(area_bottom, area_top)))

        for i, (x, y) in enumerate(positions):
            color = GEM_COLORS[i % len(GEM_COLORS)]
            gem = Gem(x, y, color, GEM_SIZE)
            gem.start_sparkle()
            self.gems.append(gem)

        # Crear botones de respuesta
        self.answer_buttons = []
        options = self.generate_options(
            self.correct_count,
            max(3, self.correct_count - 3),
            min(15, self.correct_count + 3),
            4,
        )
        btn_spacing = 120
        start_x = SCREEN_WIDTH // 2 - (len(options) - 1) * btn_spacing // 2
        for i, opt in enumerate(options):
            btn = AnswerButton(
                x=start_x + i * btn_spacing,
                y=80,
                width=80,
                height=60,
                text=str(opt),
                value=opt,
            )
            self.answer_buttons.append(btn)

        # Registro de datos
        tracker = getattr(self.window, 'tracker', None)
        if tracker:
            tracker.start_trial(self.level_number, self.trial_number, self.correct_count)

    def generate_options(self, correct, min_val, max_val, num_options):
        """Genera opciones de respuesta incluyendo la correcta."""
        options = {correct}
        while len(options) < num_options:
            opt = random.randint(min_val, max_val)
            options.add(opt)
        options = list(options)
        random.shuffle(options)
        return options

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
            "Cuenta todas las gemas y elige el número correcto",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 80,
            COLOR_PRIMARY,
            font_size=FONT_SIZE_BODY,
            anchor_x="center",
            bold=True,
        )

        # Tip: el jugador puede hacer clic en gemas para marcarlas
        arcade.draw_text(
            "Haz clic en cada gema para marcarla mientras cuentas",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 110,
            (150, 150, 170),
            font_size=FONT_SIZE_SMALL - 2,
            anchor_x="center",
        )

        # Contador de gemas marcadas
        if self.gems_clicked:
            arcade.draw_text(
                f"Marcadas: {len(self.gems_clicked)}",
                SCREEN_WIDTH // 2,
                145,
                COLOR_ACCENT,
                font_size=FONT_SIZE_BODY,
                anchor_x="center",
                bold=True,
            )

        # Dibujar gemas
        for i, gem in enumerate(self.gems):
            gem.draw()
            # Si está marcada, dibujar un check
            if i in self.gems_clicked:
                arcade.draw_circle_filled(
                    gem.x + gem.size * 0.4,
                    gem.y + gem.size * 0.6,
                    10,
                    COLOR_SUCCESS,
                )
                arcade.draw_text(
                    "✓",
                    gem.x + gem.size * 0.4,
                    gem.y + gem.size * 0.6,
                    COLOR_TEXT_LIGHT,
                    font_size=12,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True,
                )

        # Botones de respuesta
        if not self.answered:
            for btn in self.answer_buttons:
                btn.draw()

        # Feedback
        self.draw_feedback()

    def on_update(self, delta_time):
        for gem in self.gems:
            gem.update(delta_time)
        self.update_feedback(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.answered:
            for btn in self.answer_buttons:
                btn.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.state == "feedback":
            return

        if not self.answered:
            # Verificar clic en gemas (para marcar)
            for i, gem in enumerate(self.gems):
                if gem.contains_point(x, y):
                    if i in self.gems_clicked:
                        self.gems_clicked.remove(i)
                    else:
                        self.gems_clicked.append(i)
                    return

            # Verificar clic en botones de respuesta
            for btn in self.answer_buttons:
                if btn.is_clicked(x, y):
                    self.answered = True
                    answer = btn.value

                    tracker = getattr(self.window, 'tracker', None)
                    is_correct = False
                    if tracker:
                        is_correct = tracker.record_answer(answer)

                    if is_correct:
                        btn.state = "correct"
                    else:
                        btn.state = "incorrect"
                        for b in self.answer_buttons:
                            if b.value == self.correct_count:
                                b.state = "correct"

                    self.show_feedback(is_correct)
                    break