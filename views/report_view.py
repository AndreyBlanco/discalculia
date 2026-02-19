"""
Pantalla de reporte observacional final.
Muestra un resumen del rendimiento del jugador en todos los niveles.
"""

import arcade
import math
from constants import *


class LevelCard:
    """Tarjeta visual para mostrar resultados de un nivel."""

    def __init__(self, x, y, width, height, level_num, level_data):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level_num = level_num
        self.data = level_data
        self.is_hovered = False

        # Extraer datos
        if self.data:
            self.accuracy = self.data.get("accuracy", 0)
            self.avg_time = self.data.get("avg_response_time", 0)
            self.errors = self.data.get("errors", 0)
            self.level_name = self.data.get("level_name", f"Nivel {level_num}")
        else:
            self.accuracy = 0
            self.avg_time = 0
            self.errors = 0
            self.level_name = LEVEL_NAMES.get(level_num, f"Nivel {level_num}")

        # Color según rendimiento
        if self.accuracy >= 70:
            self.accent_color = COLOR_SUCCESS
        elif self.accuracy >= 40:
            self.accent_color = COLOR_SECONDARY
        else:
            self.accent_color = COLOR_ERROR

    def draw(self):
        # Sombra
        arcade.draw_rectangle_filled(
            self.x + 2, self.y - 2,
            self.width, self.height,
            (0, 0, 0, 30)
        )

        # Fondo de la card
        bg = (240, 248, 255) if not self.is_hovered else (230, 240, 250)
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height, bg
        )

        # Borde superior con color de rendimiento
        arcade.draw_rectangle_filled(
            self.x, self.y + self.height // 2 - 3,
            self.width, 6, self.accent_color
        )

        # Borde general
        arcade.draw_rectangle_outline(
            self.x, self.y, self.width, self.height,
            (200, 210, 220), 2
        )

        # Nombre del nivel (abreviado)
        short_names = {
            1: "Subitizacion",
            2: "Conteo",
            3: "Comparacion",
            4: "Estimacion",
            5: "Secuenciacion",
        }
        name = short_names.get(self.level_num, f"Nivel {self.level_num}")

        arcade.draw_text(
            name,
            self.x, self.y + self.height // 2 - 25,
            COLOR_TEXT_DARK,
            font_size=11,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # Porcentaje grande
        arcade.draw_text(
            f"{self.accuracy}%",
            self.x, self.y + 10,
            self.accent_color,
            font_size=26,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        # Mini barra de progreso
        bar_w = self.width - 30
        bar_h = 8
        bar_y = self.y - 20
        arcade.draw_rectangle_filled(
            self.x, bar_y, bar_w, bar_h, (220, 220, 230)
        )
        filled = bar_w * (self.accuracy / 100)
        if filled > 0:
            arcade.draw_rectangle_filled(
                self.x - bar_w / 2 + filled / 2, bar_y,
                filled, bar_h, self.accent_color
            )

        # Tiempo promedio
        arcade.draw_text(
            f"{self.avg_time}s prom.",
            self.x, self.y - 42,
            (120, 120, 140),
            font_size=10,
            anchor_x="center",
            anchor_y="center",
        )

        # Errores
        error_color = COLOR_ERROR if self.errors > 0 else (120, 120, 140)
        arcade.draw_text(
            f"{self.errors} error{'es' if self.errors != 1 else ''}",
            self.x, self.y - 58,
            error_color,
            font_size=10,
            anchor_x="center",
            anchor_y="center",
        )

    def check_hover(self, mx, my):
        self.is_hovered = (
            abs(mx - self.x) <= self.width / 2
            and abs(my - self.y) <= self.height / 2
        )
        return self.is_hovered


class ObservationTab:
    """Pestaña clickeable para una observación."""

    def __init__(self, x, y, width, height, index, title, content, tab_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = index
        self.title = title
        self.content = content
        self.tab_color = tab_color
        self.is_selected = False
        self.is_hovered = False

    def draw(self):
        if self.is_selected:
            bg = self.tab_color
            text_color = COLOR_TEXT_LIGHT
            border_w = 2
        elif self.is_hovered:
            bg = (*self.tab_color, 180)
            text_color = COLOR_TEXT_LIGHT
            border_w = 1
        else:
            bg = (230, 235, 240)
            text_color = COLOR_TEXT_DARK
            border_w = 1

        # Pestaña
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, bg)
        arcade.draw_rectangle_outline(
            self.x, self.y, self.width, self.height, (180, 190, 200), border_w
        )

        # Texto de la pestaña
        arcade.draw_text(
            self.title,
            self.x, self.y,
            text_color,
            font_size=10,
            anchor_x="center",
            anchor_y="center",
            bold=self.is_selected,
        )

    def contains_point(self, px, py):
        return (
            abs(px - self.x) <= self.width / 2
            and abs(py - self.y) <= self.height / 2
        )

    def check_hover(self, mx, my):
        self.is_hovered = self.contains_point(mx, my)
        return self.is_hovered


class ReportView(arcade.View):
    """Vista del reporte observacional final."""

    def __init__(self):
        super().__init__()
        self.report = None
        self.saved_file = None
        self.animation_time = 0
        self.cards = []
        self.tabs = []
        self.selected_tab = 0

    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND)
        tracker = getattr(self.window, 'tracker', None)
        if tracker:
            self.report = tracker.get_full_report()
            self.saved_file = tracker.save_report_to_file(self.report)
        self.build_cards()
        self.build_tabs()

    def build_cards(self):
        """Construye las 5 tarjetas de nivel."""
        self.cards = []
        if not self.report:
            return

        levels_data = self.report.get("levels", {})
        card_w = 170
        card_h = 145
        total_w = 5 * card_w + 4 * 12  # 12px gap
        start_x = SCREEN_WIDTH // 2 - total_w // 2 + card_w // 2
        card_y = SCREEN_HEIGHT - 290

        for i in range(1, 6):
            level_data = levels_data.get(i, None)
            x = start_x + (i - 1) * (card_w + 12)
            card = LevelCard(x, card_y, card_w, card_h, i, level_data)
            self.cards.append(card)

    def build_tabs(self):
        """Construye las pestañas de observaciones."""
        self.tabs = []
        if not self.report:
            return

        observations = self.report.get("observations", [])
        if not observations:
            return

        # Nombres cortos para las pestañas
        tab_names = []
        tab_colors = []
        for obs in observations:
            if "Subitizacion" in obs or "Subitización" in obs:
                tab_names.append("Subit.")
            elif "Conteo" in obs:
                tab_names.append("Conteo")
            elif "Comparacion" in obs or "Comparación" in obs:
                tab_names.append("Compar.")
            elif "Estimacion" in obs or "Estimación" in obs:
                tab_names.append("Estim.")
            elif "Secuenciacion" in obs or "Secuenciación" in obs:
                tab_names.append("Secuen.")
            else:
                tab_names.append(f"Obs {len(tab_names) + 1}")

            # Color según tipo
            if "Buen" in obs:
                tab_colors.append(COLOR_SUCCESS)
            elif "moderada" in obs or "Tiempo" in obs:
                tab_colors.append(COLOR_SECONDARY)
            elif "baja" in obs:
                tab_colors.append(COLOR_ERROR)
            else:
                tab_colors.append(COLOR_PRIMARY)

        num_tabs = len(observations)
        tab_w = min(120, (SCREEN_WIDTH - 120) // max(num_tabs, 1))
        total_tabs_w = num_tabs * tab_w + (num_tabs - 1) * 6
        start_x = SCREEN_WIDTH // 2 - total_tabs_w // 2 + tab_w // 2
        tab_y = 268

        for i, obs in enumerate(observations):
            # Limpiar emojis del contenido
            clean_obs = obs
            for emoji in ["✅", "🔍", "⚠️", "⏱️"]:
                clean_obs = clean_obs.replace(emoji, "")
            clean_obs = clean_obs.strip()

            tab = ObservationTab(
                x=start_x + i * (tab_w + 6),
                y=tab_y,
                width=tab_w,
                height=28,
                index=i,
                title=tab_names[i] if i < len(tab_names) else f"Obs {i+1}",
                content=clean_obs,
                tab_color=tab_colors[i] if i < len(tab_colors) else COLOR_PRIMARY,
            )
            self.tabs.append(tab)

        if self.tabs:
            self.tabs[0].is_selected = True

    def on_draw(self):
        self.clear()

        if not self.report:
            arcade.draw_text(
                "No hay datos disponibles",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                COLOR_TEXT_DARK, font_size=FONT_SIZE_SUBTITLE,
                anchor_x="center", anchor_y="center",
            )
            return

        # --- Fondo del panel principal ---
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            SCREEN_WIDTH - 40, SCREEN_HEIGHT - 30,
            (255, 255, 255, 230),
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            SCREEN_WIDTH - 40, SCREEN_HEIGHT - 30,
            COLOR_PRIMARY, 3,
        )

        # --- Título ---
        arcade.draw_text(
            "Resumen Observacional",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 45,
            COLOR_PRIMARY,
            font_size=FONT_SIZE_SUBTITLE + 2,
            anchor_x="center", anchor_y="center",
            bold=True,
        )

        # --- Info del jugador ---
        arcade.draw_text(
            f"Jugador: {self.report.get('player_name', 'N/A')}  |  "
            f"Edad: {self.report.get('player_age', 'N/A')}  |  "
            f"Duracion: {self.report.get('total_session_time', 0)}s",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80,
            COLOR_TEXT_DARK, font_size=FONT_SIZE_SMALL,
            anchor_x="center", anchor_y="center",
        )

        # --- Precisión general ---
        overall = self.report.get("overall_accuracy", 0)
        if overall >= 70:
            ov_color = COLOR_SUCCESS
        elif overall >= 40:
            ov_color = COLOR_SECONDARY
        else:
            ov_color = COLOR_ERROR

        arcade.draw_text(
            f"Precision General: {overall}%  "
            f"({self.report.get('overall_correct', 0)}/{self.report.get('overall_total', 0)} correctas)",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 115,
            ov_color, font_size=FONT_SIZE_BODY,
            anchor_x="center", anchor_y="center",
            bold=True,
        )

        # Barra general
        bar_w = 500
        bar_y = SCREEN_HEIGHT - 140
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, bar_y, bar_w, 10, (220, 220, 230)
        )
        filled = bar_w * (overall / 100)
        if filled > 0:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2 - bar_w / 2 + filled / 2, bar_y,
                filled, 10, ov_color,
            )

        # --- Cards de niveles ---
        # Etiqueta
        arcade.draw_text(
            "Resultados por nivel:",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 170,
            COLOR_PRIMARY, font_size=FONT_SIZE_SMALL,
            anchor_x="center", anchor_y="center",
            bold=True,
        )

        for card in self.cards:
            card.draw()

        # --- Sección de observaciones ---
        obs_section_y = 290
        arcade.draw_line(
            50, obs_section_y, SCREEN_WIDTH - 50, obs_section_y,
            (200, 210, 220), 2
        )

        arcade.draw_text(
            "Observaciones:",
            SCREEN_WIDTH // 2, obs_section_y + 18,
            COLOR_PRIMARY, font_size=FONT_SIZE_SMALL,
            anchor_x="center", anchor_y="center",
            bold=True,
        )

        # Pestañas
        for tab in self.tabs:
            tab.draw()

        # Contenido de la pestaña seleccionada
        if self.tabs and self.selected_tab < len(self.tabs):
            selected = self.tabs[self.selected_tab]
            content = selected.content

            # Panel de contenido
            content_y = 220
            content_h = 60
            content_w = SCREEN_WIDTH - 120

            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, content_y,
                content_w, content_h,
                (245, 248, 252),
            )
            arcade.draw_rectangle_outline(
                SCREEN_WIDTH // 2, content_y,
                content_w, content_h,
                selected.tab_color, 2,
            )

            # Indicador de color a la izquierda
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2 - content_w // 2 + 4, content_y,
                8, content_h, selected.tab_color,
            )

            # Texto del contenido (dividir si es largo)
            max_chars = 75
            if len(content) > max_chars:
                # Dividir en dos líneas
                mid = content.rfind(" ", 0, max_chars)
                if mid == -1:
                    mid = max_chars
                line1 = content[:mid]
                line2 = content[mid:].strip()
                arcade.draw_text(
                    line1,
                    SCREEN_WIDTH // 2 - content_w // 2 + 20, content_y + 12,
                    COLOR_TEXT_DARK, font_size=12,
                    anchor_y="center",
                )
                arcade.draw_text(
                    line2,
                    SCREEN_WIDTH // 2 - content_w // 2 + 20, content_y - 12,
                    COLOR_TEXT_DARK, font_size=12,
                    anchor_y="center",
                )
            else:
                arcade.draw_text(
                    content,
                    SCREEN_WIDTH // 2 - content_w // 2 + 20, content_y,
                    COLOR_TEXT_DARK, font_size=12,
                    anchor_y="center",
                )

        # --- Disclaimer ---
        disclaimer_y = 155
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, disclaimer_y,
            SCREEN_WIDTH - 120, 44,
            (*COLOR_ERROR, 25),
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH // 2, disclaimer_y,
            SCREEN_WIDTH - 120, 44,
            COLOR_ERROR, 2,
        )
        arcade.draw_text(
            "HERRAMIENTA DE OBSERVACION -- NO ES UN INSTRUMENTO DE DIAGNOSTICO",
            SCREEN_WIDTH // 2, disclaimer_y + 8,
            COLOR_ERROR, font_size=11,
            anchor_x="center", anchor_y="center",
            bold=True,
        )
        arcade.draw_text(
            "Los resultados deben ser interpretados por un profesional calificado.",
            SCREEN_WIDTH // 2, disclaimer_y - 10,
            COLOR_TEXT_DARK, font_size=10,
            anchor_x="center", anchor_y="center",
        )

        # --- Archivo guardado ---
        if self.saved_file:
            arcade.draw_text(
                f"Reporte guardado en: {self.saved_file}",
                SCREEN_WIDTH // 2, 115,
                COLOR_SUCCESS, font_size=11,
                anchor_x="center", anchor_y="center",
            )

        # --- Botón volver ---
        btn_y = 55
        btn_w = 200
        btn_h = 40
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, btn_y, btn_w, btn_h, COLOR_PRIMARY
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH // 2, btn_y, btn_w, btn_h, (255, 255, 255, 100), 2
        )
        arcade.draw_text(
            "Volver al Menu",
            SCREEN_WIDTH // 2, btn_y,
            COLOR_TEXT_LIGHT, font_size=FONT_SIZE_SMALL,
            anchor_x="center", anchor_y="center",
            bold=True,
        )

    def on_update(self, delta_time):
        self.animation_time += delta_time

    def on_mouse_motion(self, x, y, dx, dy):
        for card in self.cards:
            card.check_hover(x, y)
        for tab in self.tabs:
            tab.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        # Click en pestañas
        for tab in self.tabs:
            if tab.contains_point(x, y):
                self.selected_tab = tab.index
                for t in self.tabs:
                    t.is_selected = (t.index == self.selected_tab)
                return

        # Botón volver al menú
        if abs(x - SCREEN_WIDTH // 2) <= 100 and abs(y - 55) <= 20:
            from views.menu_view import MenuView
            self.window.show_view(MenuView())