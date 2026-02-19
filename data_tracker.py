"""
Módulo de registro de datos de rendimiento.
Registra discretamente la precisión, tiempo de respuesta y patrones de error
para generar un resumen observacional.

NOTA IMPORTANTE: Esta es una herramienta de OBSERVACIÓN, NO de diagnóstico.
"""

import time
import json
import os
from constants import LEVEL_NAMES


class TrialData:
    """Datos de un solo intento/ronda dentro de un nivel."""

    def __init__(self, level, trial_number, correct_answer):
        self.level = level
        self.trial_number = trial_number
        self.correct_answer = correct_answer
        self.player_answer = None
        self.is_correct = False
        self.start_time = time.time()
        self.end_time = None
        self.response_time = None
        self.attempts = 0  # Número de intentos antes de acertar o pasar

    def record_answer(self, answer):
        """Registra la respuesta del jugador."""
        self.attempts += 1
        self.player_answer = answer
        self.end_time = time.time()
        self.response_time = self.end_time - self.start_time

        if isinstance(self.correct_answer, list):
            self.is_correct = answer == self.correct_answer
        else:
            self.is_correct = answer == self.correct_answer

        return self.is_correct

    def to_dict(self):
        """Convierte los datos a diccionario."""
        return {
            "level": self.level,
            "trial_number": self.trial_number,
            "correct_answer": self.correct_answer,
            "player_answer": self.player_answer,
            "is_correct": self.is_correct,
            "response_time": round(self.response_time, 2) if self.response_time else None,
            "attempts": self.attempts,
        }


class DataTracker:
    """
    Gestor principal de datos del juego.
    Registra todos los datos de rendimiento para generar el resumen observacional.
    """

    def __init__(self):
        self.player_name = ""
        self.player_age = ""
        self.session_start = time.time()
        self.session_end = None
        self.level_data = {1: [], 2: [], 3: [], 4: [], 5: []}
        self.current_trial = None

    def set_player_info(self, name, age):
        """Establece la información del jugador."""
        self.player_name = name
        self.player_age = age

    def start_trial(self, level, trial_number, correct_answer):
        """Inicia un nuevo intento/ronda."""
        self.current_trial = TrialData(level, trial_number, correct_answer)
        return self.current_trial

    def record_answer(self, answer):
        """Registra la respuesta del intento actual."""
        if self.current_trial:
            result = self.current_trial.record_answer(answer)
            self.level_data[self.current_trial.level].append(self.current_trial)
            return result
        return False

    def get_level_summary(self, level):
        """Obtiene un resumen del rendimiento en un nivel específico."""
        trials = self.level_data.get(level, [])
        if not trials:
            return None

        total = len(trials)
        correct = sum(1 for t in trials if t.is_correct)
        times = [t.response_time for t in trials if t.response_time is not None]
        avg_time = sum(times) / len(times) if times else 0
        total_attempts = sum(t.attempts for t in trials)

        return {
            "level": level,
            "level_name": LEVEL_NAMES.get(level, f"Nivel {level}"),
            "total_trials": total,
            "correct": correct,
            "accuracy": round((correct / total) * 100, 1) if total > 0 else 0,
            "avg_response_time": round(avg_time, 2),
            "total_attempts": total_attempts,
            "errors": total - correct,
        }

    def get_full_report(self):
        """Genera el reporte observacional completo."""
        self.session_end = time.time()
        total_time = self.session_end - self.session_start

        report = {
            "player_name": self.player_name,
            "player_age": self.player_age,
            "total_session_time": round(total_time, 1),
            "levels": {},
            "observations": [],
            "disclaimer": (
                "IMPORTANTE: Este reporte es una herramienta de OBSERVACIÓN, "
                "NO de diagnóstico. Los resultados deben ser interpretados por "
                "un profesional calificado en el contexto de una evaluación completa."
            ),
        }

        all_correct = 0
        all_total = 0

        for level in range(1, 6):
            summary = self.get_level_summary(level)
            if summary:
                report["levels"][level] = summary
                all_correct += summary["correct"]
                all_total += summary["total_trials"]

                                # Generar observaciones automáticas
                if summary["accuracy"] < 40:
                    report["observations"].append(
                        f"{summary['level_name']}: Precision baja ({summary['accuracy']}%). "
                        f"Podria indicar dificultad en esta area. "
                        f"Se recomienda observacion adicional."
                    )
                elif summary["accuracy"] < 70:
                    report["observations"].append(
                        f"{summary['level_name']}: Precision moderada ({summary['accuracy']}%). "
                        f"Podria beneficiarse de practica adicional."
                    )
                else:
                    report["observations"].append(
                        f"{summary['level_name']}: Buen desempeno ({summary['accuracy']}%)."
                    )

                if summary["avg_response_time"] > 15:
                    report["observations"].append(
                        f"{summary['level_name']}: Tiempo de respuesta elevado "
                        f"({summary['avg_response_time']}s promedio). "
                        f"Podria indicar inseguridad o dificultad con el concepto."
                    )

        report["overall_accuracy"] = (
            round((all_correct / all_total) * 100, 1) if all_total > 0 else 0
        )
        report["overall_correct"] = all_correct
        report["overall_total"] = all_total

        return report

    def save_report_to_file(self, report):
        """Guarda el reporte en un archivo JSON."""
        filename = f"reporte_{self.player_name}_{int(time.time())}.json"
        # Convertir datos de trials a diccionarios serializables
        serializable_report = report.copy()
        for level_key, level_val in serializable_report.get("levels", {}).items():
            if isinstance(level_val, dict):
                serializable_report["levels"][level_key] = level_val

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(serializable_report, f, ensure_ascii=False, indent=2)
            return filename
        except Exception as e:
            print(f"Error al guardar reporte: {e}")
            return None