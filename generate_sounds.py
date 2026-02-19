"""
Script para generar los archivos de sonido del juego.
Ejecutar una sola vez: python generate_sounds.py
Genera dos archivos WAV usando solo la biblioteca estándar de Python.
"""

import wave
import struct
import math
import os


def generate_correct_sound(filename):
    """Genera un sonido agradable ascendente de dos tonos para respuesta correcta.
    
    Args:
        filename: Ruta del archivo WAV a crear.
    """
    sample_rate = 44100
    duration = 0.45
    num_samples = int(sample_rate * duration)
    volume = 0.4

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)       # Mono
        wav_file.setsampwidth(2)       # 16 bits
        wav_file.setframerate(sample_rate)

        for i in range(num_samples):
            t = i / sample_rate

            # Dos tonos ascendentes: C5 luego E5
            if t < 0.2:
                freq = 523.25  # C5
            else:
                freq = 659.25  # E5

            # Fade out suave al final
            fade = 1.0
            if i > num_samples * 0.75:
                fade = (num_samples - i) / (num_samples * 0.25)

            # Fade in muy corto para evitar clic
            if i < 200:
                fade *= i / 200

            value = volume * fade * math.sin(2 * math.pi * freq * t)
            packed = struct.pack('h', int(value * 32767))
            wav_file.writeframes(packed)


def generate_try_again_sound(filename):
    """Genera un sonido suave y bajo para respuesta incorrecta.
    
    No es un sonido negativo/feo, sino un tono gentil que invita
    a intentar de nuevo, apropiado para niños.
    
    Args:
        filename: Ruta del archivo WAV a crear.
    """
    sample_rate = 44100
    duration = 0.35
    num_samples = int(sample_rate * duration)
    volume = 0.3

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for i in range(num_samples):
            t = i / sample_rate

            # Dos tonos descendentes suaves: A4 luego F4
            if t < 0.17:
                freq = 440.0   # A4
            else:
                freq = 349.23  # F4

            # Fade out
            fade = 1.0
            if i > num_samples * 0.7:
                fade = (num_samples - i) / (num_samples * 0.3)

            # Fade in
            if i < 200:
                fade *= i / 200

            value = volume * fade * math.sin(2 * math.pi * freq * t)
            packed = struct.pack('h', int(value * 32767))
            wav_file.writeframes(packed)


if __name__ == "__main__":
    # Crear carpeta de sonidos si no existe
    os.makedirs("assets/sounds", exist_ok=True)

    # Generar archivos
    generate_correct_sound("assets/sounds/correct.wav")
    print("Generado: assets/sounds/correct.wav")

    generate_try_again_sound("assets/sounds/try_again.wav")
    print("Generado: assets/sounds/try_again.wav")

    print("\nSonidos generados exitosamente!")
    print("Ya puedes ejecutar el juego con: python main.py")