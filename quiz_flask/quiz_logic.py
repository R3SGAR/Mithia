import random

# Banco de 20 preguntas simples de álgebra
# Cada pregunta es una tupla: (pregunta, respuesta correcta como string)
banco_preguntas = [
    ("¿Cuál es el valor de x en: 2x + 3 = 7?", "2"),
    ("¿Cuál es el valor de x en: 3x - 5 = 4?", "3"),
    ("¿Cuál es el valor de x en: x/2 = 4?", "8"),
    ("¿Cuál es el valor de x en: 5x = 25?", "5"),
    ("¿Cuál es el valor de x en: x + 7 = 12?", "5"),
    ("¿Cuál es el valor de x en: 4x + 2 = 18?", "4"),
    ("¿Cuál es el valor de x en: x - 3 = 6?", "9"),
    ("¿Cuál es el valor de x en: 2x - 4 = 0?", "2"),
    ("¿Cuál es el valor de x en: 3x + 1 = 10?", "3"),
    ("¿Cuál es el valor de x en: x/3 = 5?", "15"),
    ("¿Cuál es el valor de x en: 7x = 49?", "7"),
    ("¿Cuál es el valor de x en: x + 4 = 9?", "5"),
    ("¿Cuál es el valor de x en: 5x - 10 = 0?", "2"),
    ("¿Cuál es el valor de x en: x - 2 = 3?", "5"),
    ("¿Cuál es el valor de x en: 4x + 8 = 24?", "4"),
    ("¿Cuál es el valor de x en: 2x = 10?", "5"),
    ("¿Cuál es el valor de x en: x/4 = 3?", "12"),
    ("¿Cuál es el valor de x en: 6x - 3 = 15?", "3"),
    ("¿Cuál es el valor de x en: x + 5 = 11?", "6"),
    ("¿Cuál es el valor de x en: 3x = 18?", "6")
]

def obtener_preguntas_aleatorias(num=5):
    """Selecciona num preguntas aleatorias sin repetición."""
    return random.sample(banco_preguntas, num)

def verificar_respuesta(pregunta, respuesta_usuario, preguntas):
    """Verifica si la respuesta es correcta y devuelve el resultado."""
    for p, correcta in preguntas:
        if p == pregunta:
            return respuesta_usuario.strip() == correcta, correcta
    return False, None