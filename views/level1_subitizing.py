"""
Nivel 1: Subitización
El jugador debe reconocer rápidamente la cantidad de gemas mostradas brevemente.
"""

import arcade
import random
import math
from constants import *
from views.level_base import LevelBase, Gem, AnswerButton


class Level1View(LevelBase):
    """Nivel de subitización: reconocer cantidades de un vistazo."""

    def __init__(self):
        super().__init__(level_number=1)
        self.display_time = 1.5  # Tiempo que las gemas son visibles (segundos)
        self.display_timer = 0
        self.showing_gems = True
        self.correct_count = 0
        self.answered = False
        self.trial_number = 0
        self.setup_trial()

    def setup_trial(self):
        """Configura un nuevo intento de subitización."""
        self.trial_number += 1
        self.showing_gems = True
        self.display_timer = 0
        self.answered = False
        self.state = "playing"

        # Generar cantidad aleatoria (1-6 para subitización)
        self.correct_count = random.randint(1, 6)

        # Crear gemas en posiciones aleatorias (área central)
        self.gems = []
        margin = 120
        area_left = margin + 100
        area_right = SCREEN_WIDTH - margin - 100
        area_bottom = 200
        area_top = SCREEN_HEIGHT - 150

        positions = []
        for _ in range(self.correct_count):
            attempts = 0
            while attempts < 50:
                x = random.randint(area_left, area_right)
                y = random.randint(area_bottom, area_top)
                # Asegurar que no se superpongan
                too_close = False
                for px, py in positions:
                    if math.hypot(x - px, y - py) < GEM_SIZE * 2.5:
                        too_close = True
                        break
                if not too_close:
                    positions.append((x, y))
                    break
                attempts += 1
            else:
                positions.append((random.randint(area_left, area_right),
                                  random.randint(area_bottom, area_top)))

        for x, y in positions:
            color = random.choice(GEM_COLORS)
            gem = Gem(x, y, color, GEM_SIZE_LARGE)
            gem.start_sparkle()
            self.gems.append(gem)

        # Crear botones de respuesta
        self.answer_buttons = []
        options = self.generate_options(self.correct_count, 1, 6, 4)
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

        # Iniciar registro de datos
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

        # Fondo
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND
        )

        # HUD
        self.draw_hud()

        # Instrucción
        if self.showing_gems:
            arcade.draw_text(
                "¡Observa las gemas!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 80,
                COLOR_ACCENT,
                font_size=FONT_SIZE_BODY,
                anchor_x="center",
                bold=True,
            )
            # Barra de tiempo restante
            time_ratio = max(0, 1 - self.display_timer / self.display_time)
            bar_width = 300 * time_ratio
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100,
                bar_width, 6, COLOR_SECONDARY
            )
        else:
            arcade.draw_text(
                "¿Cuántas gemas había?",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 80,
                COLOR_PRIMARY,
                font_size=FONT_SIZE_SUBTITLE,
                anchor_x="center",
                bold=True,
            )

        # Dibujar gemas (solo si están visibles)
        if self.showing_gems:
            for gem in self.gems:
                gem.draw()

        # Dibujar botones de respuesta (solo cuando las gemas desaparecen)
        if not self.showing_gems and not self.answered:
            for btn in self.answer_buttons:
                btn.draw()

        # Feedback
        self.draw_feedback()

    def on_update(self, delta_time):
        # Actualizar animación de gemas
        for gem in self.gems:
            gem.update(delta_time)

        # Temporizador de visualización
        if self.showing_gems:
            self.display_timer += delta_time
            if self.display_timer >= self.display_time:
                self.showing_gems = False

        # Actualizar feedback
        self.update_feedback(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.showing_gems and not self.answered:
            for btn in self.answer_buttons:
                btn.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.state == "feedback":
            return

        if not self.showing_gems and not self.answered:
            for btn in self.answer_buttons:
                if btn.is_clicked(x, y):
                    self.answered = True
                    answer = btn.value

                    # Registrar respuesta
                    tracker = getattr(self.window, 'tracker', None)
                    is_correct = False
                    if tracker:
                        is_correct = tracker.record_answer(answer)

                    # Feedback visual en botón
                    if is_correct:
                        btn.state = "correct"
                    else:
                        btn.state = "incorrect"
                        # Mostrar cuál era el correcto
                        for b in self.answer_buttons:
                            if b.value == self.correct_count:
                                b.state = "correct"

                    self.show_feedback(is_correct)
                    break