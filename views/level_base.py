"""
Clase base para todos los niveles del juego.
Proporciona funcionalidad común como dibujo de HUD, transiciones, feedback y sonido.
"""

import arcade
import math
import os
from constants import *


# --- Cargar sonidos una sola vez a nivel de módulo ---
SOUND_CORRECT = None
SOUND_TRY_AGAIN = None

def load_game_sounds():
    """Carga los archivos de sonido del juego.
    
    Se ejecuta una sola vez. Si los archivos no existen,
    el juego funciona sin sonido.
    """
    global SOUND_CORRECT, SOUND_TRY_AGAIN

    correct_path = os.path.join("assets", "sounds", "correct.wav")
    try_again_path = os.path.join("assets", "sounds", "try_again.wav")

    try:
        if os.path.exists(correct_path):
            SOUND_CORRECT = arcade.load_sound(correct_path)
        else:
            print(f"Aviso: No se encontró {correct_path}")
    except Exception as e:
        print(f"Aviso: No se pudo cargar sonido correcto: {e}")

    try:
        if os.path.exists(try_again_path):
            SOUND_TRY_AGAIN = arcade.load_sound(try_again_path)
        else:
            print(f"Aviso: No se encontró {try_again_path}")
    except Exception as e:
        print(f"Aviso: No se pudo cargar sonido incorrecto: {e}")

# Cargar sonidos al importar el módulo
load_game_sounds()


class Gem:
    """Representa una gema visual en el juego."""

    def __init__(self, x, y, color, size=GEM_SIZE):
        """Inicializa una gema con posición, color y tamaño.
        
        Args:
            x, y: Posición inicial de la gema.
            color: Tupla RGB del color de la gema.
            size: Tamaño base de la gema.
        """
        self.x = x
        self.y = y
        self.base_y = y
        self.color = color
        self.size = size
        self.time = 0
        self.phase = x * 0.1
        self.visible = True
        self.scale = 1.0
        self.alpha = 255
        self.sparkle_time = 0
        self.is_sparkling = False

    def update(self, delta_time):
        """Actualiza la animación de flotación de la gema.
        
        Args:
            delta_time: Tiempo transcurrido desde el último frame.
        """
        self.time += delta_time
        self.y = self.base_y + math.sin(self.time * GEM_FLOAT_SPEED + self.phase) * 5

    def draw(self):
        """Dibuja la gema como un polígono en forma de diamante con efectos."""
        if not self.visible:
            return

        actual_size = self.size * self.scale

        # Sombra debajo de la gema
        arcade.draw_ellipse_filled(
            self.x + 2, self.y - actual_size * 0.5,
            actual_size * 0.8, actual_size * 0.2,
            (0, 0, 0, 30)
        )

        # Cuerpo de la gema (forma de diamante)
        points = [
            (self.x, self.y + actual_size),
            (self.x + actual_size * 0.6, self.y),
            (self.x, self.y - actual_size * 0.4),
            (self.x - actual_size * 0.6, self.y),
        ]
        arcade.draw_polygon_filled(points, (*self.color, self.alpha))

        # Brillo superior para dar profundidad
        highlight = (
            min(255, self.color[0] + 100),
            min(255, self.color[1] + 100),
            min(255, self.color[2] + 100),
        )
        small_points = [
            (self.x, self.y + actual_size * 0.7),
            (self.x + actual_size * 0.25, self.y + actual_size * 0.15),
            (self.x, self.y + actual_size * 0.05),
            (self.x - actual_size * 0.25, self.y + actual_size * 0.15),
        ]
        arcade.draw_polygon_filled(small_points, (*highlight, min(255, self.alpha)))

        # Destellos animados
        if self.is_sparkling:
            self.sparkle_time += 0.05
            sparkle_alpha = int(abs(math.sin(self.sparkle_time * 5)) * 200)
            arcade.draw_circle_filled(
                self.x + actual_size * 0.3, self.y + actual_size * 0.5,
                3, (255, 255, 255, sparkle_alpha)
            )
            arcade.draw_circle_filled(
                self.x - actual_size * 0.2, self.y + actual_size * 0.3,
                2, (255, 255, 255, sparkle_alpha)
            )

    def start_sparkle(self):
        """Activa el efecto de destello en la gema."""
        self.is_sparkling = True
        self.sparkle_time = 0

    def contains_point(self, px, py):
        """Verifica si un punto está dentro del área de la gema.
        
        Args:
            px, py: Coordenadas del punto a verificar.
        
        Returns:
            True si el punto está dentro del área de la gema.
        """
        return (abs(px - self.x) < self.size * 0.7 and
                abs(py - self.y) < self.size * 1.1)


class AnswerButton:
    """Botón de respuesta clickeable con estados visuales."""

    def __init__(self, x, y, width, height, text, value):
        """Inicializa un botón de respuesta.
        
        Args:
            x, y: Posición central del botón.
            width, height: Dimensiones del botón.
            text: Texto a mostrar en el botón.
            value: Valor que representa la respuesta.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = str(text)
        self.value = value
        self.is_hovered = False
        self.state = "normal"
        self.animation_time = 0

    def draw(self):
        """Dibuja el botón con su estado visual actual."""
        if self.state == "correct":
            color = COLOR_SUCCESS
            self.animation_time += 0.05
            scale = 1 + math.sin(self.animation_time * 10) * 0.05
        elif self.state == "incorrect":
            color = COLOR_ERROR
            scale = 1
        elif self.is_hovered:
            color = COLOR_SECONDARY
            scale = 1.05
        else:
            color = COLOR_PRIMARY
            scale = 1

        w = self.width * scale
        h = self.height * scale

        # Sombra
        arcade.draw_rectangle_filled(self.x + 3, self.y - 3, w, h, (0, 0, 0, 40))
        # Botón
        arcade.draw_rectangle_filled(self.x, self.y, w, h, color)
        arcade.draw_rectangle_outline(self.x, self.y, w, h, (255, 255, 255, 120), 2)
        # Texto
        arcade.draw_text(
            self.text,
            self.x, self.y,
            COLOR_TEXT_LIGHT,
            font_size=FONT_SIZE_SUBTITLE,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

    def check_hover(self, mx, my):
        """Actualiza el estado de hover del botón.
        
        Args:
            mx, my: Posición del mouse.
        
        Returns:
            True si el mouse está sobre el botón.
        """
        self.is_hovered = (
            abs(mx - self.x) <= self.width / 2 and
            abs(my - self.y) <= self.height / 2
        )
        return self.is_hovered

    def is_clicked(self, mx, my):
        """Verifica si el botón fue clickeado.
        
        Args:
            mx, my: Posición del clic.
        
        Returns:
            True si el clic está dentro del área del botón.
        """
        return (
            abs(mx - self.x) <= self.width / 2 and
            abs(my - self.y) <= self.height / 2
        )


class LevelBase(arcade.View):
    """Clase base para todos los niveles del juego.
    
    Proporciona funcionalidad compartida: HUD, sistema de feedback
    con sonido, y lógica de transición entre niveles.
    """

    def __init__(self, level_number):
        """Inicializa la base del nivel.
        
        Args:
            level_number: Número del nivel (1-5).
        """
        super().__init__()
        self.level_number = level_number
        self.trial_number = 0
        self.total_trials = TRIALS_PER_LEVEL
        self.gems = []
        self.answer_buttons = []
        self.state = "playing"
        self.feedback_timer = 0
        self.feedback_text = ""
        self.feedback_text_line2 = ""
        self.feedback_color = COLOR_SUCCESS
        self.transition_timer = 0
        self.message = ""

    def play_feedback_sound(self, is_correct):
        """Reproduce el sonido de feedback según si la respuesta fue correcta.
        
        Args:
            is_correct: True para sonido de correcto, False para intentar de nuevo.
        """
        try:
            if is_correct and SOUND_CORRECT:
                arcade.play_sound(SOUND_CORRECT)
            elif not is_correct and SOUND_TRY_AGAIN:
                arcade.play_sound(SOUND_TRY_AGAIN)
        except Exception:
            # Si hay error de audio, el juego continúa sin sonido
            pass

    def draw_hud(self):
        """Dibuja la barra de información superior (HUD)."""
        # Barra superior
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25, SCREEN_WIDTH, 50, (*COLOR_PRIMARY, 220)
        )

        # Nombre del nivel
        level_name = LEVEL_NAMES.get(self.level_number, f"Nivel {self.level_number}")
        arcade.draw_text(
            f"Nivel {self.level_number}: {level_name}",
            15, SCREEN_HEIGHT - 35,
            COLOR_TEXT_LIGHT,
            font_size=FONT_SIZE_SMALL,
            bold=True,
        )

        # Progreso (ronda actual)
        arcade.draw_text(
            f"Ronda {self.trial_number}/{self.total_trials}",
            SCREEN_WIDTH - 15, SCREEN_HEIGHT - 35,
            COLOR_TEXT_LIGHT,
            font_size=FONT_SIZE_SMALL,
            anchor_x="right",
            bold=True,
        )

        # Barra de progreso visual
        bar_width = 200
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = SCREEN_HEIGHT - 45
        progress = self.trial_number / self.total_trials if self.total_trials > 0 else 0

        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, bar_y, bar_width, 8, (255, 255, 255, 80)
        )
        if progress > 0:
            filled_width = bar_width * progress
            arcade.draw_rectangle_filled(
                bar_x + filled_width / 2, bar_y, filled_width, 8, COLOR_GOLD
            )

    def draw_feedback(self):
        """Dibuja el panel de feedback visual después de una respuesta."""
        if self.state == "feedback":
            # Calcular tamaño del panel según si hay segunda línea
            has_line2 = len(self.feedback_text_line2) > 0
            panel_w = 700
            panel_h = 140 if has_line2 else 100

            # Panel semi-transparente
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                panel_w, panel_h, (*self.feedback_color, 230)
            )
            arcade.draw_rectangle_outline(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                panel_w, panel_h, (255, 255, 255, 180), 3
            )

            if has_line2:
                # Texto en dos líneas
                arcade.draw_text(
                    self.feedback_text,
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 22,
                    COLOR_TEXT_LIGHT,
                    font_size=FONT_SIZE_BODY + 2,
                    anchor_x="center", anchor_y="center",
                    bold=True,
                )
                arcade.draw_text(
                    self.feedback_text_line2,
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 22,
                    COLOR_TEXT_LIGHT,
                    font_size=FONT_SIZE_BODY + 2,
                    anchor_x="center", anchor_y="center",
                    bold=True,
                )
            else:
                # Texto en una línea
                arcade.draw_text(
                    self.feedback_text,
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    COLOR_TEXT_LIGHT,
                    font_size=FONT_SIZE_SUBTITLE,
                    anchor_x="center", anchor_y="center",
                    bold=True,
                )

    def show_feedback(self, is_correct):
        """Muestra feedback visual y reproduce sonido.
        
        Args:
            is_correct: True si la respuesta fue correcta.
        """
        self.state = "feedback"
        self.feedback_timer = 0
        self.feedback_text_line2 = ""
        if is_correct:
            self.feedback_text = "¡Correcto!"
            self.feedback_color = COLOR_SUCCESS
        else:
            self.feedback_text = "¡Inténtalo de nuevo!"
            self.feedback_color = COLOR_SECONDARY

        # Reproducir sonido de feedback
        self.play_feedback_sound(is_correct)

    def update_feedback(self, delta_time):
        """Actualiza el temporizador de feedback y avanza cuando termina.
        
        Args:
            delta_time: Tiempo transcurrido desde el último frame.
        """
        if self.state == "feedback":
            self.feedback_timer += delta_time
            if self.feedback_timer >= 1.5:
                self.state = "playing"
                self.next_trial()

    def next_trial(self):
        """Avanza al siguiente intento o al siguiente nivel."""
        if self.trial_number >= self.total_trials:
            self.go_to_next_level()
        else:
            self.setup_trial()

    def setup_trial(self):
        """Configura el siguiente intento. Debe ser implementado por subclases."""
        pass

    def go_to_next_level(self):
        """Avanza al siguiente nivel o muestra el reporte final."""
        next_level = self.level_number + 1
        if next_level <= TOTAL_LEVELS:
            from views.instruction_view import InstructionView
            self.window.show_view(InstructionView(level=next_level))
        else:
            from views.report_view import ReportView
            self.window.show_view(ReportView())