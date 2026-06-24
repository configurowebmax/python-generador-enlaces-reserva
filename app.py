"""
=====================================================================
 Generador de Enlaces de Reserva
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_generador_enlaces_reserva_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Generador de Enlaces de Reserva."""

    def __init__(self, telefono, nombre_negocio, servicio):
        self.telefono = float(telefono)
        self.nombre_negocio = float(nombre_negocio)
        self.servicio = float(servicio)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        tel = str(self.telefono).strip().replace(" ", "").replace("+", "")
        msg = (f"Hola {self.nombre_negocio}, quiero reservar una cita "
               f"para {self.servicio}. ¿Qué horarios tienen disponibles?")
        wa = f"https://wa.me/{tel}?text={window.encodeURIComponent(msg)}"
        mail = f"mailto:?subject=Reserva&body={window.encodeURIComponent(msg)}"
        return {"whatsapp": wa, "mailto": mail, "telefono": tel}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""
        return "✅ Enlaces generados. Compártelos en tus redes."


# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(
        document.querySelector("#telefono").value or "",
        document.querySelector("#nombre_negocio").value or "",
        document.querySelector("#servicio").value or "",
    )
    r = c.calcular()
    html = f"""
      <div class="result-value">🔗 Enlaces listos</div>
      <p><a href="{r["whatsapp"]}" target="_blank" class="btn btn-primary mt-1">💬 Abrir WhatsApp</a></p>
      <p><a href="{r["mailto"]}" class="btn btn-secondary mt-1">📧 Enviar correo</a></p>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "telefono": input_float("telefono"),
            "nombre_negocio": input_float("nombre_negocio"),
            "servicio": input_float("servicio"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "telefono" in datos:
            document.querySelector("#telefono").value = datos["telefono"]
        if "nombre_negocio" in datos:
            document.querySelector("#nombre_negocio").value = datos["nombre_negocio"]
        if "servicio" in datos:
            document.querySelector("#servicio").value = datos["servicio"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
