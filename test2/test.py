import random

# Banco de 20 preguntas simples de álgebra
# Cada pregunta es una tupla: (pregunta, respuesta correcta como string para comparación exacta)
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

def main():
    print("Bienvenido al programa de ejercicios de álgebra.")
    print("1. Elegir el tópico (por ahora solo álgebra disponible).")
    topico = input("Ingresa 'algebra' para continuar: ").strip().lower()
    
    if topico != "algebra":
        print("Tópico no disponible. Saliendo.")
        return
    
    # Seleccionar 5 preguntas aleatorias sin repetición
    preguntas_seleccionadas = random.sample(banco_preguntas, 5)
    
    respuestas_usuario = []
    correctas = 0
    
    for i, (pregunta, respuesta_correcta) in enumerate(preguntas_seleccionadas, 1):
        print(f"\nPregunta {i}: {pregunta}")
        respuesta = input("Tu respuesta: ").strip()
        
        respuestas_usuario.append((pregunta, respuesta, respuesta_correcta))
        
        if respuesta == respuesta_correcta:
            print("¡Correcto!")
            correctas += 1
        else:
            print(f"Incorrecto. La respuesta correcta es: {respuesta_correcta}")
    
    # Resumen
    print("\nResumen:")
    for pregunta, respuesta, correcta in respuestas_usuario:
        status = "Correcta" if respuesta == correcta else "Incorrecta"
        print(f"- {pregunta} | Tu respuesta: {respuesta} | Correcta: {correcta} | {status}")
    
    porcentaje = (correctas / 5) * 100
    print(f"\nPorcentaje de acierto: {porcentaje:.2f}%")

if __name__ == "__main__":
    main()