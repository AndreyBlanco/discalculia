"""
Constantes globales para el juego educativo de detección de indicadores de discalculia.
"""

# --- Configuración de Ventana ---
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "NumWorld - Aventura Numérica"

# --- Colores Personalizados ---
COLOR_BACKGROUND = (230, 245, 255)        # Azul cielo muy claro
COLOR_BACKGROUND_DARK = (200, 225, 245)   # Azul cielo un poco más oscuro
COLOR_PRIMARY = (70, 130, 180)            # Azul acero
COLOR_SECONDARY = (255, 183, 77)          # Naranja cálido
COLOR_SUCCESS = (102, 187, 106)           # Verde suave
COLOR_ERROR = (239, 83, 80)              # Rojo suave
COLOR_TEXT_DARK = (50, 50, 70)            # Texto oscuro
COLOR_TEXT_LIGHT = (255, 255, 255)        # Texto claro
COLOR_ACCENT = (171, 71, 188)            # Púrpura
COLOR_GOLD = (255, 215, 0)               # Dorado
COLOR_PANEL = (255, 255, 255, 200)        # Blanco semi-transparente

# --- Colores para Gemas ---
GEM_COLORS = [
    (255, 82, 82),    # Rojo
    (69, 170, 242),   # Azul
    (76, 175, 80),    # Verde
    (255, 183, 77),   # Naranja
    (171, 71, 188),   # Púrpura
    (255, 215, 0),    # Dorado
    (0, 188, 212),    # Cian
    (255, 128, 171),  # Rosa
]

# --- Configuración de Animación ---
ANIMATION_SPEED = 2.0
GEM_FLOAT_SPEED = 0.5
GEM_FLOAT_RANGE = 10
SPARKLE_DURATION = 0.5

# --- Configuración de Juego ---
TOTAL_LEVELS = 5
TRIALS_PER_LEVEL = 5  # Número de intentos/rondas por nivel

# --- Configuración de Fuentes ---
FONT_SIZE_TITLE = 48
FONT_SIZE_SUBTITLE = 28
FONT_SIZE_BODY = 20
FONT_SIZE_SMALL = 16
FONT_SIZE_LARGE = 64

# --- Nombres de Niveles ---
LEVEL_NAMES = {
    1: "Subitización",
    2: "Conteo",
    3: "Comparación de Magnitudes",
    4: "Estimación",
    5: "Secuenciación Numérica",
}

LEVEL_DESCRIPTIONS = {
    1: "¿Cuántas gemas ves? ¡Responde rápido!",
    2: "Cuenta todas las gemas con cuidado",
    3: "¿Qué grupo tiene más gemas?",
    4: "¿Aproximadamente cuántas gemas hay?",
    5: "Ordena los números de menor a mayor",
}

LEVEL_INSTRUCTIONS = {
    1: [
        "Bienvenido al Bosque de las Gemas Mágicas!",
        "",
        "Verás algunas gemas brillantes en la pantalla.",
        "Aparecerán solo por un momento.",
        "",
        "Tu misión: Decir cuántas gemas viste!",
        "Haz clic en el número correcto.",
        "",
        "¿Estás listo? ¡Vamos!",
    ],
    2: [
        "Bienvenido al Jardín del Conteo!",
        "",
        "Verás varias gemas en la pantalla.",
        "Esta vez puedes tomarte tu tiempo.",
        "",
        "Tu misión: Cuenta todas las gemas",
        "y haz clic en el número correcto.",
        "",
        "¡Cuenta con cuidado!",
    ],
    3: [
        "Bienvenido a la Cueva de Comparación!",
        "",
        "Verás dos grupos de gemas.",
        "",
        "Tu misión: Haz clic en el grupo",
        "que tenga MÁS gemas.",
        "",
        "¡Confía en tus ojos!",
    ],
    4: [
        "Bienvenido al Lago de la Estimación!",
        "",
        "Verás muchas gemas moviéndose.",
        "Son demasiadas para contar una por una!",
        "",
        "Tu misión: ¿Aproximadamente cuántas hay?",
        "Elige la respuesta más cercana.",
        "",
        "¡No necesitas ser exacto!",
    ],
    5: [
        "Bienvenido a la Montaña de los Números!",
        "",
        "Verás varios números desordenados.",
        "",
        "Tu misión: Haz clic en los números",
        "en orden, del menor al mayor.",
        "",
        "¡Tú puedes hacerlo!",
    ],
}

# --- Formas de Gemas (para dibujar con primitivas) ---
# Usaremos formas geométricas simples para no depender de archivos de imagen
GEM_SIZE = 40
GEM_SIZE_SMALL = 30
GEM_SIZE_LARGE = 50