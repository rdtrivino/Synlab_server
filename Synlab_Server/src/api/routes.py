from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json

from src.monitors.cpu_monitor import CPUMonitor
from src.monitors.memory_monitor import MemoryMonitor
from src.monitors.disk_monitor import DiskMonitor
from src.monitors.network_monitor import NetworkMonitor

app = FastAPI()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="src/templates")

# Inicializar monitores
cpu_monitor = CPUMonitor()
memory_monitor = MemoryMonitor()
disk_monitor = DiskMonitor()
network_monitor = NetworkMonitor()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/api/metrics")
async def get_metrics():
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu": cpu_monitor.get_metrics(),
        "memory": memory_monitor.get_metrics(),
        "disk": disk_monitor.get_metrics(),
        "network": network_monitor.get_metrics()
    }
