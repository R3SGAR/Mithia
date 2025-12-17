from flask import Flask, render_template, request, session, redirect, url_for
import quiz_logic

app = Flask(__name__)
app.secret_key = '1'  # Necesario para sesiones, cámbiala a algo único

@app.route('/', methods=['GET', 'POST']) # Ruta inicial
def index():
    if request.method == 'POST':
        topico = request.form.get('topico').strip().lower()
        if topico == 'algebra':
            session['preguntas'] = quiz_logic.obtener_preguntas_aleatorias()
            session['respuestas'] = []  # Lista para guardar (pregunta, resp_usuario, correcta, status)
            session['indice'] = 0
            session['correctas'] = 0
            return redirect(url_for('pregunta'))
        else:
            return render_template('index.html', error='Tópico no disponible. Solo "algebra".')
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

@app.route('/resumen') # Ruta resumen
def resumen():
    if 'respuestas' not in session:
        return redirect(url_for('index'))
    
    respuestas = session['respuestas']
    correctas = session['correctas']
    porcentaje = (correctas / 5) * 100
    session.clear()  # Limpia la sesión para reiniciar
    return render_template('resumen.html', respuestas=respuestas, porcentaje=porcentaje)

if __name__ == '__main__':
    app.run(debug=True)