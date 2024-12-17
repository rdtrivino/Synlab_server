from fastapi import FastAPI, Request, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic
import secrets
import uvicorn

app = FastAPI()
security = HTTPBasic()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="src/templates")

# Usuarios de prueba
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "user": {
        "password": "user123",
        "role": "user"
    }
}

# Manejo de sesiones
sessions = {}

# Middleware para verificar sesión
async def get_current_user(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida"
        )
    return sessions[session_token]

# Ruta para el login
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Ruta para procesar el login
@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username in USERS and USERS[username]["password"] == password:
        session_token = secrets.token_urlsafe(32)
        sessions[session_token] = {
            "username": username,
            "role": USERS[username]["role"]
        }
        
        # Redirigir al index después del login exitoso
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="session_token", value=session_token)
        return response
    
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "message": "Usuario o contraseña incorrectos"
        }
    )

# Ruta para la página principal (index)
@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "username": current_user["username"],
            "role": current_user["role"]
        }
    )

# Ruta para la página de canales
@app.get("/channels", response_class=HTMLResponse)
async def read_channels(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "channels.html", 
        {
            "request": request,
            "username": current_user["username"],
            "role": current_user["role"]
        }
    )

# Ruta para la página de estadísticas
@app.get("/statistics", response_class=HTMLResponse)
async def read_statistics(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "statistics.html", 
        {
            "request": request,
            "username": current_user["username"],
            "role": current_user["role"]
        }
    )

# Ruta para la página de historial
@app.get("/history", response_class=HTMLResponse)
async def read_history(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "history.html", 
        {
            "request": request,
            "username": current_user["username"],
            "role": current_user["role"]
        }
    )

# Ruta para la página de configuración
@app.get("/settings", response_class=HTMLResponse)
async def read_settings(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso no autorizado"
        )
    return templates.TemplateResponse(
        "settings.html", 
        {
            "request": request,
            "username": current_user["username"],
            "role": current_user["role"]
        }
    )

# Ruta para cerrar sesión
@app.get("/logout")
async def logout(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token in sessions:
        del sessions[session_token]
    
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session_token")
    return response

# Manejador de errores
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_message": exc.detail
        },
        status_code=exc.status_code
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)