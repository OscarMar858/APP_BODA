import streamlit as st
import csv
import os
from datetime import datetime

# Importación diferida de Google Sheets para mejorar la velocidad de carga inicial

import time
import base64
import streamlit.components.v1 as components

# ─────────────────────────────────────────────
# Configuración de la página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Nuestra Boda 💍",
    page_icon="💒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Evitar que Google Chrome intente traducir la página (el pop-up molesto)
components.html(
    """
    <script>
        // Establecer el idioma del documento principal a español
        parent.document.documentElement.lang = 'es';
        // Añadir meta tag para evitar la traducción
        if (!parent.document.querySelector('meta[name="google"]')) {
            let meta = parent.document.createElement('meta');
            meta.name = 'google';
            meta.content = 'notranslate';
            parent.document.head.appendChild(meta);
        }
    </script>
    """,
    height=0,
    width=0
)

@st.cache_data
def get_image_base64(path):
    if os.path.isfile(path):
        with open(path, "rb") as img_file:
            import base64
            return base64.b64encode(img_file.read()).decode()
    return ""

# Ruta Acuarela
ACUARELA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "acuarela.jpg")
acuarela_b64 = get_image_base64(ACUARELA_PATH)
acuarela_bg = f"background-image: url('data:image/jpeg;base64,{acuarela_b64}');" if acuarela_b64 else ""

# ─────────────────────────────────────────────
# CSS global
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Fuentes ── */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=Montserrat:wght@300;400;500;600&family=Great+Vibes&display=swap');

    /* ── Fondo ── */
    .stApp {
        background: linear-gradient(160deg, #fdf6f0 0%, #f5ebe0 30%, #faf3ed 60%, #f0e6d8 100%);
    }

    /* ── Ocultar UI de Streamlit ── */
    #MainMenu, footer, header, .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    /* ═══════════════════════════════════════
       ANIMACIONES
       ═══════════════════════════════════════ */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%      { transform: translateY(-14px); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes pulse-soft {
        0%, 100% { opacity: 0.6; }
        50%      { opacity: 1; }
    }
    @keyframes hint-pulse {
        0%, 100% { opacity: 0.4; letter-spacing: 5px; }
        50%      { opacity: 1; letter-spacing: 7px; }
    }
    @keyframes revealContent {
        from { opacity: 0; transform: translateY(40px) scale(0.97); }
        to   { opacity: 1; transform: translateY(0) scale(1); }
    }


    /* Hint */
    .open-hint {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.6rem;
        font-weight: 400;
        letter-spacing: 5px;
        text-transform: uppercase;
        color: #a3b899;
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        animation: hint-pulse 3s ease-in-out infinite;
    }

    /* ═══════════════════════════════════════
       INVITACIÓN – CONTENIDO
       ═══════════════════════════════════════ */
    .invitation-reveal {
        position: relative;
        z-index: 1;
        animation: revealContent 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    }

    .watermark-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 75vh;
        background-size: cover;
        background-position: center bottom;
        opacity: 0.35;
        z-index: 0;
        pointer-events: none;
        mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 40%, rgba(0,0,0,0) 100%);
        -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 40%, rgba(0,0,0,0) 100%);
    }

    .floating-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4.2rem;
        font-weight: 300;
        text-align: center;
        color: #7a8c6e;
        animation: float 4s ease-in-out infinite;
        margin-top: 1rem;
        margin-bottom: 0;
        letter-spacing: 3px;
        line-height: 1.2;
        text-shadow: 0 2px 15px rgba(122, 140, 110, 0.15);
    }

    .shimmer-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 1rem;
        font-weight: 300;
        text-align: center;
        letter-spacing: 8px;
        text-transform: uppercase;
        background: linear-gradient(90deg, #a3b899, #7a8c6e, #c2d4b5, #7a8c6e, #a3b899);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        margin-bottom: 2rem;
    }

    .ornament {
        text-align: center;
        font-size: 1.6rem;
        color: #a3b899;
        margin: 0.5rem 0 1.5rem 0;
        letter-spacing: 12px;
        animation: pulse-soft 3s ease-in-out infinite;
    }

    .info-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(163, 184, 153, 0.25);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(122, 140, 110, 0.08);
        animation: fadeInUp 1s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .info-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(122, 140, 110, 0.14);
    }

    .section-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 5px;
        text-transform: uppercase;
        color: #a3b899;
        margin-bottom: 0.5rem;
    }

    .date-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.2rem;
        font-weight: 300;
        color: #5a4a3a;
        margin: 0.3rem 0;
        letter-spacing: 6px;
    }

    .venue-name {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #5a4a3a;
        margin: 0.3rem 0;
    }
    .venue-address {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85rem;
        font-weight: 300;
        color: #8b7d6b;
        margin-bottom: 1.2rem;
    }

    .maps-btn {
        display: inline-block;
        padding: 0.7rem 2.2rem;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #fff;
        background: linear-gradient(135deg, #7a8c6e, #a3b899);
        border: none;
        border-radius: 50px;
        text-decoration: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(122, 140, 110, 0.25);
    }
    .maps-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(122, 140, 110, 0.35);
        color: #fff;
    }

    .poetic-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.15rem;
        font-style: italic;
        font-weight: 300;
        color: #8b7d6b;
        text-align: center;
        line-height: 1.8;
        margin: 1rem 0;
    }

    .rsvp-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.4rem;
        font-weight: 300;
        text-align: center;
        color: #7a8c6e;
        margin-bottom: 0.3rem;
    }
    .rsvp-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.7rem;
        font-weight: 400;
        letter-spacing: 4px;
        text-transform: uppercase;
        text-align: center;
        color: #a3b899;
        margin-bottom: 1.5rem;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(163, 184, 153, 0.3) !important;
        border-radius: 12px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important;
        color: #5a4a3a !important;
        padding: 0.8rem 1rem !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #a3b899 !important;
        box-shadow: 0 0 0 2px rgba(163, 184, 153, 0.15) !important;
    }
    .stTextInput label, .stTextArea label {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
        color: #7a8c6e !important;
    }

    /* ── Botones ── */
    .stButton > button {
        width: 100%;
        padding: 0.85rem 2rem !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        letter-spacing: 4px !important;
        text-transform: uppercase !important;
        color: #fff !important;
        background: linear-gradient(135deg, #7a8c6e, #a3b899) !important;
        border: none !important;
        border-radius: 50px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(122, 140, 110, 0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(122, 140, 110, 0.35) !important;
    }

    .stSuccess, .stAlert {
        border-radius: 12px !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    .countdown-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .countdown-item { text-align: center; }
    .countdown-number {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.6rem;
        font-weight: 300;
        color: #7a8c6e;
        line-height: 1;
    }
    .countdown-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.6rem;
        font-weight: 500;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #a3b899;
        margin-top: 0.3rem;
    }

    .wedding-footer {
        text-align: center;
        padding: 2rem 0;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        color: #a3b899;
        letter-spacing: 2px;
    }

    .elegant-sep {
        text-align: center;
        margin: 2rem 0;
        color: #a3b899;
        font-size: 1.2rem;
        letter-spacing: 8px;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="invitation-reveal">', unsafe_allow_html=True)
if acuarela_bg:
    st.markdown(f'<div class="watermark-bg" style="{acuarela_bg}"></div>', unsafe_allow_html=True)

# ── Título flotante ──
st.markdown('<div class="floating-title">Nos Casamos</div>', unsafe_allow_html=True)
st.markdown('<div class="ornament">✦ ✦ ✦</div>', unsafe_allow_html=True)
st.markdown('<div class="shimmer-subtitle">Estáis Invitados</div>', unsafe_allow_html=True)

# ── Iniciales ──
st.markdown("""
<div style="font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 6rem; color: #7a8c6e; text-align: center; margin: 1.5rem 0; line-height: 1; text-shadow: 0 2px 20px rgba(122, 140, 110, 0.15); letter-spacing: 5px;">
    A <span style="font-family: 'Great Vibes', cursive; font-size: 4rem; color: #a3b899; margin: 0 0.5rem; font-weight: 400;">&amp;</span> O
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="elegant-sep">─ ♡ ─</div>', unsafe_allow_html=True)

# ── Cuenta atrás ──
wedding_date = datetime(2026, 10, 17)
today = datetime.now()
delta = wedding_date - today

total_seconds = max(int(delta.total_seconds()), 0)
days_left = total_seconds // 86400
months_left = days_left // 30
remaining_days = days_left % 30
hours_left = (total_seconds % 86400) // 3600
minutes_left = (total_seconds % 3600) // 60
seconds_left = total_seconds % 60

st.markdown(f"""
<div class="info-card">
    <div class="section-label">Cuenta Atrás</div>
    <div class="countdown-container" style="gap: 1rem;">
        <div class="countdown-item">
            <div class="countdown-number" id="cd-months">{months_left}</div>
            <div class="countdown-label">Meses</div>
        </div>
        <div class="countdown-item">
            <div class="countdown-number" id="cd-days">{remaining_days}</div>
            <div class="countdown-label">Días</div>
        </div>
        <div class="countdown-item">
            <div class="countdown-number" id="cd-hours">{hours_left}</div>
            <div class="countdown-label">Horas</div>
        </div>
        <div class="countdown-item">
            <div class="countdown-number" id="cd-minutes">{minutes_left}</div>
            <div class="countdown-label">Min</div>
        </div>
        <div class="countdown-item">
            <div class="countdown-number" id="cd-seconds">{seconds_left}</div>
            <div class="countdown-label">Seg</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Fecha ──
st.markdown("""
<div class="info-card">
    <div class="section-label">Fecha</div>
    <div class="date-text">17 · 10 · 2026</div>
    <div style="font-family: 'Montserrat', sans-serif; font-size: 0.8rem; color: #a3b899;
                letter-spacing: 3px; text-transform: uppercase; margin-top: 0.3rem;">
        Sábado
    </div>
</div>
""", unsafe_allow_html=True)

# ── Lugar + Google Maps ──
GOOGLE_MAPS_URL = "https://www.google.com/maps/search/Cortijo+El+Gallinero+Collado+Villalba+Madrid"

st.markdown(f"""
<div class="info-card">
    <div class="section-label">Lugar de Celebración</div>
    <div class="venue-name">Cortijo El Gallinero</div>
    <div class="venue-address">Ctra. de Navacerrada, km 0,600 · Collado Villalba, Madrid</div>
    <a href="{GOOGLE_MAPS_URL}" target="_blank" class="maps-btn">
        📍&nbsp; Cómo Llegar
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="elegant-sep">─ ♡ ─</div>', unsafe_allow_html=True)

# ── RSVP ──
st.markdown('<div class="rsvp-title">Confirma tu Asistencia</div>', unsafe_allow_html=True)
st.markdown('<div class="rsvp-subtitle">Esperamos contar contigo</div>', unsafe_allow_html=True)

with st.form("rsvp_form", clear_on_submit=True):
    nombre = st.text_input("Nombre completo", placeholder="Escribe tu nombre aquí...")
    alergias = st.text_area(
        "Alergias o intolerancias alimentarias",
        placeholder="Indica si tienes alguna alergia o restricción alimentaria...",
        height=100,
    )
    enviado = st.form_submit_button("Confirmar Asistencia")

    if enviado:
        if not nombre.strip():
            st.error("⚠️ Por favor, escribe tu nombre para confirmar la asistencia.")
        else:
            fila = [
                nombre.strip(),
                alergias.strip() if alergias.strip() else "Ninguna",
                datetime.now().strftime("%d/%m/%Y %H:%M"),
            ]
            guardado = False

            # ── Intentar guardar en Google Sheets ──
            if "gcp_service_account" in st.secrets:
                try:
                    import gspread
                    from google.oauth2.service_account import Credentials
                    scope = [
                        "https://spreadsheets.google.com/feeds",
                        "https://www.googleapis.com/auth/drive",
                    ]
                    # Limpiar y reconstruir la clave privada para evitar cualquier error de formato o espaciado
                    gcp_info = dict(st.secrets["gcp_service_account"])
                    raw_key = gcp_info["private_key"]
                    
                    # Normalizar saltos de línea (reemplazar literal \n y \r por saltos de línea reales)
                    normalized_key = raw_key.replace("\\n", "\n").replace("\\r", "\n")
                    lines = normalized_key.split("\n")
                    
                    base64_lines = []
                    for line in lines:
                        line_stripped = line.strip()
                        if not line_stripped:
                            continue
                        # Ignorar líneas que contengan BEGIN o END
                        if "BEGIN" in line_stripped.upper() or "END" in line_stripped.upper():
                            continue
                        # Quitar espacios en blanco dentro de la línea de base64
                        cleaned_line = "".join(line_stripped.split())
                        base64_lines.append(cleaned_line)
                    
                    base64_content = "".join(base64_lines)
                    # Reconstruir el PEM en formato estándar (líneas de 64 caracteres)
                    wrapped_key = "\n".join([base64_content[i:i+64] for i in range(0, len(base64_content), 64)])
                    gcp_info["private_key"] = f"-----BEGIN PRIVATE KEY-----\n{wrapped_key}\n-----END PRIVATE KEY-----"

                    creds = Credentials.from_service_account_info(
                        gcp_info,
                        scopes=scope,
                    )
                    client = gspread.authorize(creds)
                    sheet = client.open(st.secrets["spreadsheet_name"]).sheet1
                    sheet.append_row(fila)
                    guardado = True
                except Exception as e:
                    err_msg = str(e)
                    try:
                        pk = st.secrets["gcp_service_account"]["private_key"]
                        # Encontrar índices de '=' en la clave procesada
                        processed_key = gcp_info.get("private_key", "")
                        eq_indices = [i for i, c in enumerate(processed_key) if c == "="]
                        diag = (
                            f"\n\n🔍 **Diagnóstico de Clave en Nube:**"
                            f"\n* Longitud leída por Streamlit: {len(pk)}"
                            f"\n* Inicio: `{repr(pk[:25])}`"
                            f"\n* Fin: `{repr(pk[-25:])}`"
                            f"\n* ¿Contiene 'ndVoTur'?: {'ndVoTur' in pk}"
                            f"\n* Índices de '=' en clave procesada: {eq_indices}"
                        )
                    except Exception as diag_err:
                        diag = f"\n\n❌ No se pudo generar el diagnóstico: {diag_err}"
                    st.warning(f"⚠️ No se pudo guardar en Google Sheets: {err_msg}{diag}")

            # ── Fallback: guardar en CSV local ──
            if not guardado:
                csv_file = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "lista_boda.csv"
                )
                file_exists = os.path.isfile(csv_file)
                with open(csv_file, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["Nombre", "Alergias", "Fecha de confirmación"])
                    writer.writerow(fila)

            st.success(f"🎉 ¡Gracias, **{nombre.strip()}**! Tu asistencia ha sido confirmada.")
            st.balloons()

# ── Footer ──
st.markdown('<div class="elegant-sep">─ ♡ ─</div>', unsafe_allow_html=True)
st.markdown("""
<div class="wedding-footer">
    Con todo nuestro amor 💛<br>
    <span style="font-size: 0.75rem; letter-spacing: 4px; font-family: 'Montserrat', sans-serif;">
        #NuestraBoda2026
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Inyección de JS para actualizar la cuenta atrás en tiempo real
components.html("""
<script>
    const targetDate = new Date("2026-10-17T00:00:00").getTime();
    
    function updateCountdown() {
        const now = new Date().getTime();
        const distance = targetDate - now;
        if (distance < 0) return;
        
        const totalSeconds = Math.floor(distance / 1000);
        const days = Math.floor(totalSeconds / 86400);
        const months = Math.floor(days / 30);
        const remDays = days % 30;
        const hours = Math.floor((totalSeconds % 86400) / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = Math.floor(totalSeconds % 60);
        
        const doc = window.parent.document;
        const elMonths = doc.getElementById("cd-months");
        const elDays = doc.getElementById("cd-days");
        const elHours = doc.getElementById("cd-hours");
        const elMinutes = doc.getElementById("cd-minutes");
        const elSeconds = doc.getElementById("cd-seconds");
        
        if (elMonths) elMonths.innerText = months;
        if (elDays) elDays.innerText = remDays;
        if (elHours) elHours.innerText = hours;
        if (elMinutes) elMinutes.innerText = minutes;
        if (elSeconds) elSeconds.innerText = seconds;
    }
    
    setInterval(updateCountdown, 1000);
    updateCountdown();
</script>
""", height=0, width=0)
