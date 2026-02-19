"""
Nivel 5: Secuenciación Numérica
El jugador debe ordenar números de menor a mayor haciendo clic en el orden correcto.
"""

import arcade
import random
import math
from constants import *
from views.level_base import LevelBase


class NumberCard:
    """Tarjeta con un número para secuenciación."""

    def __init__(self, x, y, number, width=90, height=90):
        self.x = x
        self.y = y
        self.base_y = y
        self.number = number
        self.width = width
        self.height = height
        self.state = "available"
        self.order_selected = 0
        self.is_hovered = False
        self.time = 0
        self.phase = random.uniform(0, math.pi * 2)
        self.color = random.choice(GEM_COLORS)

    def update(self, delta_time):
        self.time += delta_time
        if self.state == "available":
            self.y = self.base_y + math.sin(self.time * 1.5 + self.phase) * 3

    def draw(self):
        if self.state == "selected":
            bg_color = COLOR_SECONDARY
            border_color = (255, 200, 50)
        elif self.state == "correct":
            bg_color = COLOR_SUCCESS
            border_color = (50, 200, 80)
        elif self.state == "incorrect":
            bg_color = COLOR_ERROR
            border_color = (200, 50, 50)
        elif self.is_hovered:
            bg_color = (*self.color, 200)
            border_color = self.color
        else:
            bg_color = (255, 255, 255, 230)
            border_color = self.color

        scale = 1.08 if self.is_hovered and self.state == "available" else 1.0
        w = self.width * scale
        h = self.height * scale

        # Sombra
        arcade.draw_rectangle_filled(
            self.x + 3, self.y - 3, w, h, (0, 0, 0, 30)
        )
        # Tarjeta
        arcade.draw_rectangle_filled(self.x, self.y, w, h, bg_color)
        arcade.draw_rectangle_outline(self.x, self.y, w, h, border_color, 3)

        # Pequeña gema decorativa en la esquina superior
        gem_x = self.x - w * 0.3
        gem_y = self.y + h * 0.3
        gem_size = 8
        gem_points = [
            (gem_x, gem_y + gem_size),
            (gem_x + gem_size * 0.5, gem_y),
            (gem_x, gem_y - gem_size * 0.3),
            (gem_x - gem_size * 0.5, gem_y),
        ]
        arcade.draw_polygon_filled(gem_points, self.color)

        # Número
        text_color = COLOR_TEXT_LIGHT if self.state in ("selected", "correct", "incorrect") else COLOR_TEXT_DARK
        arcade.draw_text(
            str(self.number),
            self.x,
            self.y - 5,
            text_color,
            font_size=FONT_SIZE_SUBTITLE + 4,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # Orden de selección
        if self.state == "selected" and self.order_selected > 0:
            arcade.draw_circle_filled(
                self.x + w * 0.35, self.y + h * 0.35, 14, COLOR_PRIMARY
            )
            arcade.draw_text(
                str(self.order_selected),
                self.x + w * 0.35,
                self.y + h * 0.35,
                COLOR_TEXT_LIGHT,
                font_size=FONT_SIZE_SMALL,
                anchor_x="center",
                anchor_y="center",
                bold=True,
            )

    def contains_point(self, px, py):
        return (
            abs(px - self.x) <= self.width / 2
            and abs(py - self.y) <= self.height / 2
        )

    def check_hover(self, mx, my):
        self.is_hovered = self.contains_point(mx, my)
        return self.is_hovered


class Level5View(LevelBase):
    """Nivel de secuenciación numérica: ordenar números de menor a mayor."""

    def __init__(self):
        super().__init__(level_number=5)
        self.cards = []
        self.correct_sequence = []
        self.player_sequence = []
        self.selection_order = 0
        self.answered = False
        self.trial_number = 0

        # Botones
        self.confirm_btn_x = SCREEN_WIDTH // 2
        self.confirm_btn_y = 70
        self.confirm_btn_w = 200
        self.confirm_btn_h = 50

        self.reset_btn_x = SCREEN_WIDTH - 120
        self.reset_btn_y = 70
        self.reset_btn_w = 160
        self.reset_btn_h = 40

        self.setup_trial()

    def setup_trial(self):
        """Configura un nuevo intento de secuenciación."""
        self.trial_number += 1
        self.answered = False
        self.player_sequence = []
        self.selection_order = 0
        self.state = "playing"

        # Generar números aleatorios (4-6 números)
        num_cards = random.randint(4, 6)
        numbers = random.sample(range(1, 20), num_cards)
        self.correct_sequence = sorted(numbers)

        # Crear tarjetas desordenadas
        shuffled = numbers[:]
        random.shuffle(shuffled)

        self.cards = []
        cols = min(num_cards, 4)
        rows = math.ceil(num_cards / cols)
        card_spacing_x = 130
        card_spacing_y = 130
        start_x = SCREEN_WIDTH // 2 - (cols - 1) * card_spacing_x // 2
        start_y = SCREEN_HEIGHT // 2 + (rows - 1) * card_spacing_y // 2 - 20

        for i, num in enumerate(shuffled):
            col = i % cols
            row = i // cols
            x = start_x + col * card_spacing_x
            y = start_y - row * card_spacing_y
            card = NumberCard(x, y, num)
            self.cards.append(card)

        # Registro de datos
        tracker = getattr(self.window, 'tracker', None)
        if tracker:
            tracker.start_trial(
                self.level_number,
                self.trial_number,
                self.correct_sequence,
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
            "Haz clic en los números en orden: del MENOR al MAYOR",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 80,
            COLOR_PRIMARY,
            font_size=FONT_SIZE_BODY,
            anchor_x="center",
            bold=True,
        )

        # Mostrar secuencia seleccionada
        if self.player_sequence:
            seq_text = " -> ".join(str(n) for n in self.player_sequence)
            arcade.draw_text(
                f"Tu orden: {seq_text}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 115,
                COLOR_ACCENT,
                font_size=FONT_SIZE_BODY,
                anchor_x="center",
                bold=True,
            )

        # Dibujar tarjetas
        for card in self.cards:
            card.draw()

        # Botón de confirmar
        if len(self.player_sequence) == len(self.cards) and not self.answered:
            pulse = math.sin(self.transition_timer * 4) * 0.05 + 1.0
            btn_w = int(self.confirm_btn_w * pulse)
            btn_h = int(self.confirm_btn_h * pulse)
            arcade.draw_rectangle_filled(
                self.confirm_btn_x, self.confirm_btn_y,
                btn_w, btn_h, COLOR_SUCCESS
            )
            arcade.draw_rectangle_outline(
                self.confirm_btn_x, self.confirm_btn_y,
                btn_w, btn_h, (255, 255, 255, 150), 2
            )
            arcade.draw_text(
                "Confirmar",
                self.confirm_btn_x,
                self.confirm_btn_y,
                COLOR_TEXT_LIGHT,
                font_size=FONT_SIZE_BODY,
                anchor_x="center",
                anchor_y="center",
                bold=True,
            )

        # Botón de reiniciar
        if self.player_sequence and not self.answered:
            arcade.draw_rectangle_filled(
                self.reset_btn_x, self.reset_btn_y,
                self.reset_btn_w, self.reset_btn_h, COLOR_ERROR
            )
            arcade.draw_text(
                "Reiniciar",
                self.reset_btn_x,
                self.reset_btn_y,
                COLOR_TEXT_LIGHT,
                font_size=FONT_SIZE_SMALL,
                anchor_x="center",
                anchor_y="center",
                bold=True,
            )

        # Feedback
        self.draw_feedback()

    def on_update(self, delta_time):
        self.transition_timer += delta_time
        for card in self.cards:
            card.update(delta_time)
        self.update_feedback(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.answered:
            for card in self.cards:
                if card.state == "available":
                    card.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.state == "feedback" or self.answered:
            return

        # Botón reiniciar
        if (self.player_sequence and not self.answered
                and abs(x - self.reset_btn_x) <= self.reset_btn_w // 2
                and abs(y - self.reset_btn_y) <= self.reset_btn_h // 2):
            self.reset_selection()
            return

        # Botón confirmar
        if (len(self.player_sequence) == len(self.cards) and not self.answered
                and abs(x - self.confirm_btn_x) <= self.confirm_btn_w // 2
                and abs(y - self.confirm_btn_y) <= self.confirm_btn_h // 2):
            self.confirm_answer()
            return

        # Seleccionar tarjeta
        if not self.answered:
            for card in self.cards:
                if card.state == "available" and card.contains_point(x, y):
                    self.selection_order += 1
                    card.state = "selected"
                    card.order_selected = self.selection_order
                    self.player_sequence.append(card.number)
                    break

    def reset_selection(self):
        """Reinicia la selección actual."""
        self.player_sequence = []
        self.selection_order = 0
        for card in self.cards:
            card.state = "available"
            card.order_selected = 0

    def confirm_answer(self):
        """Confirma la respuesta del jugador."""
        self.answered = True
        is_correct = self.player_sequence == self.correct_sequence

        # Registrar respuesta
        tracker = getattr(self.window, 'tracker', None)
        if tracker:
            tracker.current_trial.player_answer = self.player_sequence
            tracker.current_trial.is_correct = is_correct
            tracker.current_trial.end_time = __import__('time').time()
            tracker.current_trial.response_time = (
                tracker.current_trial.end_time - tracker.current_trial.start_time
            )
            tracker.current_trial.attempts = 1
            tracker.level_data[self.level_number].append(tracker.current_trial)

        # Feedback visual en tarjetas
        for card in self.cards:
            expected_pos = self.correct_sequence.index(card.number) + 1
            if card.order_selected == expected_pos:
                card.state = "correct"
            else:
                card.state = "incorrect"

        self.show_feedback(is_correct)
        if not is_correct:
            seq_text = " -> ".join(str(n) for n in self.correct_sequence)
            self.feedback_text = f"El orden era: {seq_text}"