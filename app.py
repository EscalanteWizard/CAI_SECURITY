import random
from datetime import datetime

import streamlit as st

# ---------------------------------------------------------
# Configuración general de la aplicación
# ---------------------------------------------------------
st.set_page_config(
    page_title="CAI Security",
    page_icon="🛡️",
    layout="wide"
)

CAMARAS = ["Entrada principal", "Garaje", "Patio trasero"]
SENSORES_LASER = ["Pasillo interior", "Ventana trasera", "Cerca perimetral"]
MENU_OPCIONES = [
    "Panel principal",
    "Cámaras",
    "Sensores láser",
    "Contramedidas",
    "Reconocimiento facial",
    "Alertas",
    "Historial",
    "Acerca del prototipo",
]
ICONOS = {"movimiento": "🏃", "laser": "📡", "rostro": "🧑‍💻"}

BASE_ROSTROS = [
    {"nombre": "Juan Pérez", "estado": "Autorizado", "rol": "Residente",
     "confianza": 97, "camara": "Entrada principal", "riesgo": "Bajo"},
    {"nombre": "María Gómez", "estado": "Autorizado", "rol": "Residente",
     "confianza": 95, "camara": "Garaje", "riesgo": "Bajo"},
    {"nombre": "Carlos Ruiz", "estado": "Autorizado", "rol": "Personal de mantenimiento",
     "confianza": 91, "camara": "Patio trasero", "riesgo": "Bajo"},
    {"nombre": "Rostro no identificado", "estado": "Desconocido", "rol": "Sin registro",
     "confianza": 58, "camara": "Entrada principal", "riesgo": "Alto"},
    {"nombre": "Rostro no identificado", "estado": "Desconocido", "rol": "Sin registro",
     "confianza": 47, "camara": "Patio trasero", "riesgo": "Alto"},
]

# ---------------------------------------------------------
# Paleta de marca (tomada de cai_security.png) y temas
# ---------------------------------------------------------
COLORS = {
    "Claro": {
        "bg": "#f3f4f6", "bg_alt": "#e9eaed", "card_bg": "#ffffff", "card_border": "#e2e4e9",
        "sidebar_bg": "#ffffff", "text": "#111827", "subtext": "#6b7280",
        "accent": "#0bc5d9", "ok": "#15803d", "ok_soft": "#dcfce7",
        "alert": "#b91c1c", "alert_soft": "#fee2e2", "warn": "#b45309", "warn_soft": "#fef3c7",
        "shadow": "0 1px 3px rgba(0,0,0,0.07)",
    },
    "Oscuro": {
        "bg": "#1f2023", "bg_alt": "#2a2b2e", "card_bg": "#2a2b2e", "card_border": "#434343",
        "sidebar_bg": "#191a1c", "text": "#f4f4f5", "subtext": "#a1a1aa",
        "accent": "#0bc5d9", "ok": "#4ade80", "ok_soft": "#14532d",
        "alert": "#f87171", "alert_soft": "#450a0a", "warn": "#fbbf24", "warn_soft": "#451a03",
        "shadow": "0 1px 3px rgba(0,0,0,0.5)",
    },
}


def build_css(tema):
    c = COLORS[tema]
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

[data-testid="stAppViewContainer"] {{ background-color: {c['bg']}; }}
[data-testid="stHeader"] {{ background-color: transparent; }}

[data-testid="stSidebar"] {{
    background-color: {c['sidebar_bg']};
    border-right: 1px solid {c['card_border']};
}}
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] span, [data-testid="stSidebar"] div {{ color: {c['text']}; }}

[data-testid="stSidebar"] [data-testid="stImage"] {{
    display: flex; justify-content: center; margin: 6px 0 14px 0;
}}
[data-testid="stSidebar"] [data-testid="stImage"] img {{
    border-radius: 10px;
}}

h1, h2, h3, h4, p, span, li, label {{ color: {c['text']}; }}

.main-title {{ font-size: 42px; font-weight: 800; margin-bottom: 0px; color: {c['text']}; }}
.subtitle {{ font-size: 17px; color: {c['subtext']}; margin-top: 0px; }}

.card {{
    padding: 18px 20px; border-radius: 16px; border: 1px solid {c['card_border']};
    background-color: {c['card_bg']}; box-shadow: {c['shadow']}; margin-bottom: 14px; color: {c['text']};
}}
.camera-box {{
    padding: 14px; border-radius: 12px; background-color: {c['bg_alt']};
    border: 1px solid {c['card_border']}; color: {c['text']};
}}

.status-ok {{ color: {c['ok']}; font-weight: 700; }}
.status-alert {{ color: {c['alert']}; font-weight: 700; }}
.status-warn {{ color: {c['warn']}; font-weight: 700; }}
.small-text {{ color: {c['subtext']}; font-size: 13px; }}

.badge {{
    display: inline-block; padding: 3px 12px; border-radius: 999px;
    font-size: 12px; font-weight: 700; letter-spacing: 0.02em;
}}
.badge-alto {{ background-color: {c['alert_soft']}; color: {c['alert']}; }}
.badge-medio {{ background-color: {c['warn_soft']}; color: {c['warn']}; }}
.badge-bajo {{ background-color: {c['ok_soft']}; color: {c['ok']}; }}
.badge-autorizado {{ background-color: {c['ok_soft']}; color: {c['ok']}; }}
.badge-desconocido {{ background-color: {c['alert_soft']}; color: {c['alert']}; }}

[data-testid="stMetric"] {{
    background-color: {c['card_bg']}; border: 1px solid {c['card_border']};
    border-radius: 14px; padding: 14px 16px; box-shadow: {c['shadow']};
}}
[data-testid="stMetricLabel"] {{ color: {c['subtext']}; }}
[data-testid="stMetricValue"] {{ color: {c['text']}; }}

.stButton > button {{
    background-color: {c['accent']}; color: #062226; border: none; border-radius: 10px;
    padding: 0.5rem 1rem; font-weight: 700; transition: filter 0.15s ease, transform 0.1s ease;
}}
.stButton > button:hover {{ filter: brightness(1.08); transform: translateY(-1px); }}
.stButton > button:active {{ transform: translateY(0px); }}
.stButton > button:disabled {{ background-color: {c['card_border']}; color: {c['subtext']}; }}

hr {{ border-color: {c['card_border']}; }}
::-webkit-scrollbar {{ width: 10px; }}
::-webkit-scrollbar-thumb {{ background-color: {c['card_border']}; border-radius: 10px; }}
</style>
"""


# ---------------------------------------------------------
# Variables de sesión
# ---------------------------------------------------------
DEFAULTS = {
    "tema": "Claro",
    "evento_activo": None,
    "vigilancia_contactada": False,
    "alerta_descartada": False,
    "historial": [],
    "camara_seleccionada": "Entrada principal",
    "gas_activo": False,
    "gas_zona": None,
    "gas_nivel": 100,
}
for key, valor in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = valor


# ---------------------------------------------------------
# Funciones
# ---------------------------------------------------------
def hora_actual():
    return datetime.now().strftime("%H:%M:%S")


def agregar_historial(texto):
    st.session_state.historial.insert(0, f"{hora_actual()} - {texto}")


def badge(texto, tipo):
    return f'<span class="badge badge-{tipo}">{texto}</span>'


def badge_riesgo(riesgo):
    tipo = {"Alto": "alto", "Medio": "medio", "Bajo": "bajo"}.get(riesgo, "medio")
    return badge(riesgo, tipo)


def badge_estado_rostro(estado):
    tipo = "autorizado" if estado == "Autorizado" else "desconocido"
    return badge(estado, tipo)


def circular_gauge(percent, size=120, tema="Claro", label=""):
    c = COLORS[tema]
    percent = max(0, min(100, percent))
    stroke = max(8, int(size * 0.11))
    radius = (size - stroke) / 2
    center = size / 2
    circumference = 2 * 3.14159265358979 * radius
    offset = circumference * (1 - percent / 100)
    color = c["accent"] if percent > 20 else c["alert"]
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
            <circle cx="{center}" cy="{center}" r="{radius}" fill="none"
                stroke="{c['card_border']}" stroke-width="{stroke}" />
            <circle cx="{center}" cy="{center}" r="{radius}" fill="none"
                stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"
                stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}"
                transform="rotate(-90 {center} {center})" />
            <text x="50%" y="50%" dominant-baseline="central" text-anchor="middle"
                font-size="{size * 0.2:.0f}" font-weight="800" fill="{c['text']}">{percent}%</text>
        </svg>
        <span class="small-text">{label}</span>
    </div>
    """


def crear_evento(tipo, titulo, detalle, riesgo, **kwargs):
    st.session_state.evento_activo = {
        "tipo": tipo, "titulo": titulo, "detalle": detalle, "riesgo": riesgo, **kwargs,
    }
    st.session_state.vigilancia_contactada = False
    st.session_state.alerta_descartada = False
    agregar_historial(f"{titulo}: {detalle}")


def activar_alerta_movimiento():
    crear_evento(
        "movimiento", "Movimiento sospechoso",
        "La IA simulada detectó movimiento inusual en una zona donde normalmente no hay actividad.",
        "Alto", camara="Entrada principal",
    )


def activar_alerta_laser():
    sensor = random.choice(SENSORES_LASER)
    crear_evento(
        "laser", "Corte de sensor láser",
        f"Se interrumpió el haz láser correspondiente a '{sensor}', posible intento de acceso.",
        "Alto", sensor=sensor,
    )


def simular_reconocimiento_facial():
    persona = random.choice(BASE_ROSTROS)
    if persona["estado"] == "Autorizado":
        detalle = f"Rostro identificado como {persona['nombre']} ({persona['rol']}) con {persona['confianza']}% de confianza."
    else:
        detalle = f"Se detectó un rostro que no coincide con la base de datos registrada ({persona['confianza']}% de confianza)."
    crear_evento(
        "rostro", "Reconocimiento facial", detalle, persona["riesgo"],
        camara=persona["camara"], rostro_info=persona,
    )


def contactar_vigilancia():
    st.session_state.vigilancia_contactada = True
    agregar_historial("Se notificó al servicio de vigilancia de CAI Security.")


def descartar_alerta():
    st.session_state.evento_activo = None
    st.session_state.alerta_descartada = True
    st.session_state.vigilancia_contactada = False
    agregar_historial("El usuario marcó el evento como falsa alarma.")


def activar_gas(zona=None):
    zona = zona if zona in CAMARAS else "Entrada principal"
    st.session_state.gas_activo = True
    st.session_state.gas_zona = zona
    st.session_state.gas_nivel = max(0, st.session_state.gas_nivel - 15)
    agregar_historial(f"Contramedida simulada activada: niebla somnífera liberada en '{zona}'.")


def desactivar_gas():
    st.session_state.gas_activo = False
    st.session_state.gas_zona = None
    agregar_historial("Sistema de contramedidas restablecido (simulado).")


def reiniciar_demo():
    st.session_state.evento_activo = None
    st.session_state.vigilancia_contactada = False
    st.session_state.alerta_descartada = False
    st.session_state.gas_activo = False
    st.session_state.gas_zona = None
    agregar_historial("Se reinició la demostración.")


def mostrar_evento_activo(evento, key_prefix):
    icono = ICONOS.get(evento["tipo"], "⚠️")
    ubicacion = evento.get("camara") or evento.get("sensor") or "—"

    st.error(f"{icono} {evento['titulo'].upper()}")

    detalle_extra = ""
    if evento["tipo"] == "rostro":
        info = evento["rostro_info"]
        detalle_extra = (
            f"<b>Persona:</b> {info['nombre']}<br>"
            f"<b>Estado:</b> {badge_estado_rostro(info['estado'])}<br>"
            f"<b>Confianza IA:</b> {info['confianza']}%<br>"
        )

    st.markdown(f"""
    <div class="card">
        <b>Ubicación:</b> {ubicacion}<br>
        <b>Tipo de evento:</b> {evento['titulo']}<br>
        <b>Nivel de riesgo:</b> {badge_riesgo(evento['riesgo'])}<br>
        {detalle_extra}
        <b>Análisis:</b> {evento['detalle']}
    </div>
    """, unsafe_allow_html=True)

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("👁 Ver cámara", use_container_width=True, key=f"{key_prefix}_ver"):
            camara = evento.get("camara")
            if camara in CAMARAS:
                st.session_state.camara_seleccionada = camara
                st.info("Abra la sección 'Cámaras' para ver la simulación.")
            else:
                st.info("Este evento no proviene de una cámara de video.")
    with b2:
        if st.button("🚨 Contactar vigilancia", use_container_width=True, key=f"{key_prefix}_vig"):
            contactar_vigilancia()
            st.rerun()
    with b3:
        if st.button("✅ Marcar falsa alarma", use_container_width=True, key=f"{key_prefix}_desc"):
            descartar_alerta()
            st.rerun()
    with b4:
        if st.button("💨 Activar contramedida", use_container_width=True, key=f"{key_prefix}_gas",
                      disabled=(evento["riesgo"] != "Alto")):
            activar_gas(ubicacion if ubicacion in CAMARAS else "Entrada principal")
            st.rerun()

    if st.session_state.vigilancia_contactada:
        st.success("✅ El servicio de vigilancia fue notificado. Un agente revisará el incidente.")

    if st.session_state.gas_activo:
        st.warning(
            f"🌫️ Contramedida simulada activa en '{st.session_state.gas_zona}'. "
            "(Efecto ficticio, solo demostrativo)"
        )


# ---------------------------------------------------------
# Menú lateral
# ---------------------------------------------------------
st.sidebar.image("cai_security.png", width=140)

st.sidebar.caption("Apariencia")
modo_oscuro = st.sidebar.toggle("🌙 Modo oscuro", value=(st.session_state.tema == "Oscuro"))
st.session_state.tema = "Oscuro" if modo_oscuro else "Claro"

st.sidebar.divider()

seccion = st.sidebar.radio("Menú", MENU_OPCIONES)

st.sidebar.divider()

st.sidebar.caption("Simulaciones")
if st.sidebar.button("🏃 Simular movimiento sospechoso", use_container_width=True):
    activar_alerta_movimiento()
    st.rerun()

if st.sidebar.button("📡 Simular corte de sensor láser", use_container_width=True):
    activar_alerta_laser()
    st.rerun()

if st.sidebar.button("🧑‍💻 Simular reconocimiento facial", use_container_width=True):
    simular_reconocimiento_facial()
    st.rerun()

st.sidebar.divider()

if st.sidebar.button("🔄 Reiniciar demostración", use_container_width=True):
    reiniciar_demo()
    st.rerun()

st.sidebar.caption(
    "Este prototipo simula el funcionamiento del sistema. "
    "No utiliza cámaras, sensores ni sustancias reales."
)

st.markdown(build_css(st.session_state.tema), unsafe_allow_html=True)

# ---------------------------------------------------------
# Encabezado
# ---------------------------------------------------------
st.markdown('<div class="main-title">🛡️ CAI Security</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Prototipo de sistema inteligente de vigilancia para hogares y negocios</div>',
    unsafe_allow_html=True
)

st.divider()


# ---------------------------------------------------------
# PANEL PRINCIPAL
# ---------------------------------------------------------
if seccion == "Panel principal":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Estado del sistema", "Activo", "Protección habilitada")

    with col2:
        st.metric("Cámaras conectadas", str(len(CAMARAS)), "Todas en línea")

    with col3:
        evento = st.session_state.evento_activo
        sensores_armados = len(SENSORES_LASER) - (1 if evento and evento["tipo"] == "laser" else 0)
        st.metric("Sensores láser", f"{sensores_armados}/{len(SENSORES_LASER)}", "Armados")

    with col4:
        if st.session_state.evento_activo:
            st.metric("Alertas activas", "1", "Requiere revisión")
        else:
            st.metric("Alertas activas", "0", "Sin incidentes")

    st.subheader("Estado general")

    st.markdown("""
    <div class="card">
        <span class="status-ok">● SISTEMA ACTIVO</span><br>
        Cámaras, sensores láser y reconocimiento facial están operando con normalidad.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Sistema de disuasión (simulado)")

    gcol1, gcol2 = st.columns([1, 2])
    with gcol1:
        st.markdown(
            circular_gauge(st.session_state.gas_nivel, size=104, tema=st.session_state.tema, label="Depósito"),
            unsafe_allow_html=True,
        )
    with gcol2:
        if st.session_state.gas_activo:
            st.markdown(f'<span class="status-alert">● Activo en {st.session_state.gas_zona}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-ok">● En espera</span>', unsafe_allow_html=True)
        st.caption("El nivel del depósito baja con cada activación simulada.")

    st.subheader("Cámaras")

    cols = st.columns(len(CAMARAS))
    for col, nombre in zip(cols, CAMARAS):
        with col:
            st.markdown(f"""
            <div class="camera-box">
                <b>📹 {nombre}</b><br>
                <span class="status-ok">En línea</span><br>
                <span class="small-text">Monitoreo activo</span>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("Evento más reciente")

    if st.session_state.evento_activo:
        mostrar_evento_activo(st.session_state.evento_activo, key_prefix="panel")
    else:
        st.success("No hay alertas activas en este momento.")

        if st.session_state.alerta_descartada:
            st.info(
                "La última alerta fue descartada por el usuario. "
                "En un sistema real, esta información podría utilizarse "
                "como retroalimentación para mejorar futuras detecciones."
            )


# ---------------------------------------------------------
# CÁMARAS
# ---------------------------------------------------------
elif seccion == "Cámaras":

    st.header("📹 Cámaras conectadas")

    camara = st.selectbox(
        "Seleccione una cámara",
        CAMARAS,
        index=CAMARAS.index(st.session_state.camara_seleccionada)
    )

    st.session_state.camara_seleccionada = camara

    st.markdown(f"""
    <div class="card">
        <b>{camara}</b><br>
        <span class="status-ok">● Cámara en línea</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="
            height: 340px;
            border-radius: 14px;
            background: linear-gradient(135deg, #111827, #374151);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            text-align: center;
            padding: 25px;
        ">
            📷<br><br>
            Vista simulada de la cámara<br>
            <span style="font-size:15px; color:#d1d5db;">
                En un producto real aquí aparecería el video en vivo.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    evento = st.session_state.evento_activo
    if evento and evento.get("camara") == camara:
        st.warning(f"La IA simulada detectó actividad relacionada con: {evento['titulo']}.")
    else:
        st.success("No se detecta actividad fuera de lo normal.")


# ---------------------------------------------------------
# SENSORES LÁSER
# ---------------------------------------------------------
elif seccion == "Sensores láser":

    st.header("📡 Sensores de barrera láser")

    st.write(
        "Los sensores láser detectan cortes en el haz de luz para reforzar el "
        "perímetro en zonas donde las cámaras no tienen línea de visión directa."
    )

    evento = st.session_state.evento_activo
    sensor_afectado = evento.get("sensor") if evento and evento["tipo"] == "laser" else None

    cols = st.columns(len(SENSORES_LASER))
    for col, sensor in zip(cols, SENSORES_LASER):
        with col:
            if sensor == sensor_afectado:
                st.markdown(f"""
                <div class="camera-box">
                    <b>📡 {sensor}</b><br>
                    <span class="status-alert">● Corte detectado</span><br>
                    <span class="small-text">Posible intrusión</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="camera-box">
                    <b>📡 {sensor}</b><br>
                    <span class="status-ok">● Armado</span><br>
                    <span class="small-text">Perímetro seguro</span>
                </div>
                """, unsafe_allow_html=True)

    st.write("")

    if st.button("🔺 Simular corte de haz láser"):
        activar_alerta_laser()
        st.rerun()


# ---------------------------------------------------------
# CONTRAMEDIDAS
# ---------------------------------------------------------
elif seccion == "Contramedidas":

    st.header("🌫️ Sistema de disuasión no letal (simulado)")

    st.warning(
        "⚠️ Módulo completamente ficticio, creado únicamente para esta actividad académica "
        "de Design Thinking. Representa de forma conceptual un disuasivo no letal (niebla de "
        "baja visibilidad) y **no** constituye instrucciones, diseño ni especificación de un "
        "dispositivo o sustancia real."
    )

    gcol, _ = st.columns([1, 3])
    with gcol:
        st.markdown(
            circular_gauge(st.session_state.gas_nivel, size=128, tema=st.session_state.tema, label="Nivel del depósito"),
            unsafe_allow_html=True,
        )

    st.subheader("Cobertura por zona")

    cols = st.columns(len(CAMARAS))
    for col, zona in zip(cols, CAMARAS):
        with col:
            activo_aqui = st.session_state.gas_activo and st.session_state.gas_zona == zona
            estado_html = (
                '<span class="status-alert">● Activado</span>' if activo_aqui
                else '<span class="status-ok">● Listo</span>'
            )
            st.markdown(f"""
            <div class="camera-box">
                <b>🌫️ {zona}</b><br>
                {estado_html}
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    zona_elegida = st.selectbox("Zona a cubrir", CAMARAS, key="zona_gas")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💨 Simular activación en la zona seleccionada", use_container_width=True):
            activar_gas(zona_elegida)
            st.rerun()
    with c2:
        if st.button("🔄 Restablecer sistema", use_container_width=True):
            desactivar_gas()
            st.rerun()

    if st.session_state.gas_activo:
        st.info(f"Contramedida simulada actualmente activa en **{st.session_state.gas_zona}**.")


# ---------------------------------------------------------
# RECONOCIMIENTO FACIAL
# ---------------------------------------------------------
elif seccion == "Reconocimiento facial":

    st.header("🧑‍💻 Reconocimiento facial (IA simulada)")

    st.write(
        "La IA simulada compara cada rostro detectado contra una base de datos "
        "ficticia de personas registradas."
    )

    st.subheader("Base de datos registrada (demo)")
    for persona in [p for p in BASE_ROSTROS if p["estado"] == "Autorizado"]:
        st.markdown(f"- **{persona['nombre']}** — {persona['rol']}")

    st.write("")

    if st.button("🔍 Simular detección de rostro"):
        simular_reconocimiento_facial()
        st.rerun()

    st.subheader("Última detección")

    evento = st.session_state.evento_activo
    if evento and evento["tipo"] == "rostro":
        info = evento["rostro_info"]
        st.markdown(f"""
        <div class="card">
            <b>Cámara:</b> {info['camara']}<br>
            <b>Persona:</b> {info['nombre']}<br>
            <b>Estado:</b> {badge_estado_rostro(info['estado'])}<br>
            <b>Rol:</b> {info['rol']}<br>
            <b>Confianza IA:</b> {info['confianza']}%
        </div>
        """, unsafe_allow_html=True)

        if info["estado"] != "Autorizado":
            st.error("⚠️ Este rostro no coincide con ningún registro autorizado.")
    else:
        st.info("Todavía no se ha simulado ninguna detección facial.")


# ---------------------------------------------------------
# ALERTAS
# ---------------------------------------------------------
elif seccion == "Alertas":

    st.header("🚨 Centro de alertas")

    if st.session_state.evento_activo:
        mostrar_evento_activo(st.session_state.evento_activo, key_prefix="alertas")
    else:
        st.success("Actualmente no hay alertas pendientes.")

    st.divider()

    st.subheader("¿Qué representa esta sección?")

    st.write(
        "En el producto real, las alertas serían generadas por el análisis automático de "
        "cámaras, sensores láser y reconocimiento facial. El objetivo es que el usuario pueda "
        "identificar rápidamente lo ocurrido y decidir qué acción tomar."
    )


# ---------------------------------------------------------
# HISTORIAL
# ---------------------------------------------------------
elif seccion == "Historial":

    st.header("🕒 Historial de eventos")

    if len(st.session_state.historial) == 0:
        st.info(
            "Todavía no hay eventos. Use los botones de simulación en el menú "
            "lateral para iniciar la demostración."
        )
    else:
        for evento in st.session_state.historial:
            st.write("•", evento)


# ---------------------------------------------------------
# ACERCA DEL PROTOTIPO
# ---------------------------------------------------------
elif seccion == "Acerca del prototipo":

    st.header("ℹ️ Acerca del prototipo")

    st.write(
        """
        Este prototipo representa la plataforma de **CAI Security**, una empresa de seguridad
        tecnológica. La propuesta consiste en utilizar cámaras, sensores láser de perímetro y
        reconocimiento facial por inteligencia artificial para detectar comportamientos fuera
        de lo normal, además de un módulo conceptual de disuasión no letal.
        """
    )

    st.write(
        """
        Cuando se detecta un posible incidente, el usuario recibe una alerta y puede revisar la
        cámara, descartar el evento si se trata de una falsa alarma, contactar al servicio de
        vigilancia o activar la contramedida simulada.
        """
    )

    st.subheader("Módulos del prototipo")

    st.markdown(
        """
        - 📹 **Cámaras** — vista simulada de las cámaras conectadas.
        - 📡 **Sensores láser** — detección simulada de cortes en el perímetro.
        - 🧑‍💻 **Reconocimiento facial** — comparación simulada contra una base de datos.
        - 🌫️ **Contramedidas** — disuasivo no letal conceptual, completamente ficticio.
        - 🌙 **Tema claro / oscuro** — interfaz adaptable a la preferencia del usuario.
        """
    )

    st.subheader("Flujo representado")

    st.markdown(
        """
        **1. Cámara, sensor láser o reconocimiento facial detectan un evento**
        ↓
        **2. La IA simulada analiza el evento y asigna un nivel de riesgo**
        ↓
        **3. El usuario recibe una alerta**
        ↓
        **4. El usuario revisa la cámara**
        ↓
        **5. Se descarta la alerta, se contacta a vigilancia o se activa la contramedida**
        """
    )

    st.info(
        "Importante: este es un prototipo académico de CAI Security. La detección con IA, las "
        "cámaras, los sensores láser, el reconocimiento facial y el sistema de contramedidas son "
        "simulaciones para mostrar cómo funcionaría la solución. Ningún módulo utiliza hardware, "
        "software de IA ni sustancias reales."
    )
