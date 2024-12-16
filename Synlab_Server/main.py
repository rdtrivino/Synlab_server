from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="src/templates")

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para la página de canales
@app.get("/channels", response_class=HTMLResponse)
async def read_channels(request: Request):
    return templates.TemplateResponse("channels.html", {"request": request})

# Ruta para la página de estadísticas
@app.get("/statistics", response_class=HTMLResponse)
async def read_statistics(request: Request):
    return templates.TemplateResponse("statistics.html", {"request": request})

# Ruta para la página de historial
@app.get("/history", response_class=HTMLResponse)
async def read_history(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

# Ruta para la página de configuración
@app.get("/settings", response_class=HTMLResponse)
async def read_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)