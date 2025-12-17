from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import quiz_logic
import db

app = FastAPI()

# Montar carpeta static si la creas más adelante (CSS, JS)
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Middleware para sesiones (necesario)
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="super_secreta_clave_cambia_esta")

# Inicializar DB al arrancar
db.init_db()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start")
async def start_quiz(request: Request, nombre: str = Form(...), topico: str = Form(...)):
    topico = topico.strip().lower()
    nombre = nombre.strip()
    
    error = None
    if topico != "algebra":
        error = "Tópico no disponible. Solo 'algebra' está permitido."
    elif not nombre:
        error = "Por favor, ingresa un nombre de usuario válido."
    
    if error:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": error
        })
    
    # Si todo está bien
    user_id = db.get_or_create_user(nombre)
    request.session["user_id"] = user_id
    request.session["preguntas"] = quiz_logic.obtener_preguntas_aleatorias()
    request.session["respuestas"] = []
    request.session["indice"] = 0
    request.session["correctas"] = 0
    
    return RedirectResponse(url="/pregunta", status_code=303)

@app.get("/pregunta", response_class=HTMLResponse)
async def get_pregunta(request: Request):
    if "preguntas" not in request.session:
        return RedirectResponse(url="/", status_code=303)
    
    indice = request.session["indice"]
    if indice >= 5:
        return RedirectResponse(url="/resumen", status_code=303)
    
    pregunta_actual = request.session["preguntas"][indice][0]
    return templates.TemplateResponse("pregunta.html", {
        "request": request,
        "pregunta": pregunta_actual,
        "num": indice + 1
    })

@app.post("/pregunta", response_class=HTMLResponse)
async def post_pregunta(request: Request, respuesta: str = Form(...)):
    if "preguntas" not in request.session:
        return RedirectResponse(url="/", status_code=303)
    
    indice = request.session["indice"]
    pregunta_actual = request.session["preguntas"][indice][0]
    
    es_correcta, resp_correcta = quiz_logic.verificar_respuesta(
        pregunta_actual, respuesta, request.session["preguntas"]
    )
    
    status = 'Correcta' if es_correcta else 'Incorrecta'
    request.session["respuestas"].append((pregunta_actual, respuesta.strip(), resp_correcta, status))
    
    if es_correcta:
        request.session["correctas"] += 1
    
    feedback = {
        "pregunta": pregunta_actual,
        "resp_usuario": respuesta.strip(),
        "es_correcta": es_correcta,
        "correcta": resp_correcta
    }
    
    request.session["indice"] += 1
    last = request.session["indice"] >= 5
    
    return templates.TemplateResponse("feedback.html", {
        "request": request,
        "feedback": feedback,
        "last": last
    })

@app.get("/resumen", response_class=HTMLResponse)
async def resumen(request: Request):
    if "respuestas" not in request.session:
        return RedirectResponse(url="/", status_code=303)
    
    respuestas = request.session["respuestas"]
    correctas = request.session["correctas"]
    porcentaje = (correctas / 5) * 100
    
    user_id = request.session.get("user_id")
    if user_id:
        db.save_sesion(user_id, porcentaje)
    
    progreso = db.get_progreso_usuario(user_id) if user_id else []
    
    request.session.clear()
    
    return templates.TemplateResponse("resumen.html", {
        "request": request,
        "respuestas": respuestas,
        "porcentaje": porcentaje,
        "progreso": progreso
    })