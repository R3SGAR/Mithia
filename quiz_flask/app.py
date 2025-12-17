from flask import Flask, render_template, request, session, redirect, url_for
import quiz_logic
import db  # Importa el nuevo módulo
from flask import flash  # Para mensajes de error (opcional, pero útil)


app = Flask(__name__)
app.secret_key = '1'  # Necesario para sesiones, cámbiala a algo único

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        topico = request.form.get('topico')
        
        # Manejo de errores: si falta nombre o tópico
        if not nombre or not nombre.strip():
            flash('Por favor, ingresa un nombre de usuario válido.')
            return render_template('index.html')
        
        if not topico or topico.strip().lower() != 'algebra':
            flash('Tópico no disponible. Solo "algebra" está permitido.')
            return render_template('index.html')
        
        # Limpiar los valores (ahora es seguro porque ya validamos que no son None/vacíos)
        nombre = nombre.strip()
        topico = topico.strip().lower()
        
        # Obtener o crear usuario
        user_id = db.get_or_create_user(nombre)
        session['user_id'] = user_id
        
        # Iniciar el quiz
        session['preguntas'] = quiz_logic.obtener_preguntas_aleatorias()
        session['respuestas'] = []
        session['indice'] = 0
        session['correctas'] = 0
        return redirect(url_for('pregunta'))
    
    # Si es GET: solo mostrar la página inicial
    return render_template('index.html')

@app.route('/pregunta', methods=['GET', 'POST']) # Ruta pregunta
def pregunta():
    if 'preguntas' not in session:
        return redirect(url_for('index'))
    
    indice = session['indice']
    if indice >= 5:
        return redirect(url_for('resumen'))
    
    pregunta_actual = session['preguntas'][indice][0]
    
    if request.method == 'POST':
        resp_usuario = request.form.get('respuesta').strip()
        es_correcta, resp_correcta = quiz_logic.verificar_respuesta(pregunta_actual, resp_usuario, session['preguntas'])
        
        # Guardar en respuestas
        status = 'Correcta' if es_correcta else 'Incorrecta'
        session['respuestas'].append((pregunta_actual, resp_usuario, resp_correcta, status))
        
        if es_correcta:
            session['correctas'] += 1
        
        # Preparar feedback como diccionario
        feedback = {
            'pregunta': pregunta_actual,
            'resp_usuario': resp_usuario,
            'es_correcta': es_correcta,
            'correcta': resp_correcta
        }
        
        # Incrementar índice después de procesar
        session['indice'] += 1
        
        # Verificar si es la última
        last = session['indice'] >= 5
        
        # Renderizar la página de feedback en lugar de redirigir
        return render_template('feedback.html', feedback=feedback, last=last)
    
    # Para GET: mostrar la pregunta normal
    return render_template('pregunta.html', pregunta=pregunta_actual, num=indice+1)

@app.route('/resumen')
def resumen():
    if 'respuestas' not in session:
        return redirect(url_for('index'))
    
    respuestas = session['respuestas']
    correctas = session['correctas']
    porcentaje = (correctas / 5) * 100
    
    # Guardar sesión en DB
    user_id = session.get('user_id')
    if user_id:
        db.save_sesion(user_id, porcentaje)
    
    # Obtener progreso histórico
    progreso = db.get_progreso_usuario(user_id) if user_id else []
    
    session.clear()  # Limpia la sesión
    
    return render_template('resumen.html', respuestas=respuestas, porcentaje=porcentaje, progreso=progreso)
# Inicializar DB al empezar la app
db.init_db()

if __name__ == '__main__':
    app.run(debug=True)