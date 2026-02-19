"""
Nivel 4: Estimación
El jugador debe estimar la cantidad aproximada de gemas que se mueven en pantalla.
"""

import arcade
import random
import math
from constants import *
from views.level_base import LevelBase, Gem, AnswerButton


class MovingGem(Gem):
    """Gema que se mueve por la pantalla para dificultar el conteo exacto."""

    def __init__(self, x, y, color, size, speed_x, speed_y, bounds):
        super().__init__(x, y, color, size)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.bounds = bounds  # (left, right, bottom, top)

    def update(self, delta_time):
        super().update(delta_time)
        # Movimiento
        self.x += self.speed_x * delta_time
        self.base_y += self.speed_y * delta_time
        self.y = self.base_y + math.sin(self.time * GEM_FLOAT_SPEED + self.phase) * 5

        # Rebotar en los bordes
        left, right, bottom, top = self.bounds
        if self.x < left or self.x > right:
            self.speed_x *= -1
            self.x = max(left, min(right, self.x))
        if self.base_y < bottom or self.base_y > top:
            self.speed_y *= -1
            self.base_y = max(bottom, min(top, self.base_y))


class Level4View(LevelBase):
    """Nivel de estimación: estimar cantidad de gemas en movimiento."""

    def __init__(self):
        super().__init__(level_number=4)
        self.correct_count = 0
        self.answered = False
        self.moving_gems = []
        self.trial_number = 0
        self.setup_trial()

    def setup_trial(self):
        """Configura un nuevo intento de estimación."""
        self.trial_number += 1
        self.answered = False
        self.state = "playing"

        # Cantidades grandes (10-25) para que sea difícil contar exactamente
        self.correct_count = random.randint(10, 25)

        # Crear gemas en movimiento
        self.moving_gems = []
        margin = 80
        bounds = (margin, SCREEN_WIDTH - margin, 160, SCREEN_HEIGHT - 120)

        for _ in range(self.correct_count):
            x = random.randint(bounds[0], bounds[1])
            y = random.randint(bounds[2], bounds[3])
            color = random.choice(GEM_COLORS)
            speed_x = random.uniform(-80, 80)
            speed_y = random.uniform(-60, 60)
            gem = MovingGem(x, y, color, GEM_SIZE_SMALL, speed_x, speed_y, bounds)
            gem.start_sparkle()
            self.moving_gems.append(gem)

        # Crear opciones de respuesta (estimaciones)
        self.answer_buttons = []
        options = self.generate_estimation_options(self.correct_count)
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

    def generate_estimation_options(self, correct):
        """Genera opciones de estimación con rangos variados."""
        options = [correct]
        # Agregar opciones a diferentes distancias
        deviations = [-8, -4, 4, 8]
        random.shuffle(deviations)
        for dev in deviations[:3]:
            val = max(3, correct + dev)
            if val not in options:
                options.append(val)

        # Si no tenemos suficientes opciones, agregar más
        while len(options) < 4:
            val = random.randint(max(3, correct - 10), correct + 10)
            if val not in options:
                options.append(val)

        options = options[:4]
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
            "¿Aproximadamente cuántas gemas hay? ¡No necesitas ser exacto!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 80,
            COLOR_PRIMARY,
            font_size=FONT_SIZE_BODY,
            anchor_x="center",
            bold=True,
        )

        # Área de gemas
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
            SCREEN_WIDTH - 100, SCREEN_HEIGHT - 280,
            (200, 200, 220, 100), 2,
        )

        # Dibujar gemas en movimiento
        for gem in self.moving_gems:
            gem.draw()

        # Botones de respuesta
        if not self.answered:
            for btn in self.answer_buttons:
                btn.draw()

        # Feedback
        self.draw_feedback()

    def on_update(self, delta_time):
        for gem in self.moving_gems:
            gem.update(delta_time)
        self.update_feedback(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.answered:
            for btn in self.answer_buttons:
                btn.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.state == "feedback" or self.answered:
            return

        for btn in self.answer_buttons:
            if btn.is_clicked(x, y):
                self.answered = True
                answer = btn.value

                # Para estimación, aceptar si está cerca (±2)
                is_close = abs(answer - self.correct_count) <= 2
                is_exact = answer == self.correct_count

                tracker = getattr(self.window, 'tracker', None)
                if tracker:
                    # Registramos como correcto si está dentro del rango
                    tracker.current_trial.is_correct = is_close
                    tracker.current_trial.player_answer = answer
                    tracker.current_trial.end_time = __import__('time').time()
                    tracker.current_trial.response_time = (
                        tracker.current_trial.end_time - tracker.current_trial.start_time
                    )
                    tracker.current_trial.attempts = 1
                    tracker.level_data[self.level_number].append(tracker.current_trial)

                if is_exact:
                    btn.state = "correct"
                    self.feedback_text = "¡Exacto! ⭐⭐"
                    self.feedback_color = COLOR_SUCCESS
                elif is_close:
                    btn.state = "correct"
                    self.feedback_text = f"¡Muy cerca! Eran {self.correct_count} ⭐"
                    self.feedback_color = COLOR_SUCCESS
                else:
                    btn.state = "incorrect"
                    self.feedback_text = f"Eran {self.correct_count}."
                    self.feedback_color = COLOR_SECONDARY
                    for b in self.answer_buttons:
                        if b.value == self.correct_count:
                            b.state = "correct"

                self.state = "feedback"
                self.feedback_timer = 0
                break