import streamlit as st
import csv
import os
from datetime import datetime

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

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

# ─────────────────────────────────────────────
# Estado de sesión: sobre abierto / cerrado
# ─────────────────────────────────────────────
if "envelope_state" not in st.session_state:
# Se ha eliminado la carga de la imagen del sello para usar un sello CSS puro y perfecto

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

    /* ═══════════════════════════════════════
       PANTALLA DEL SOBRE (NUEVO DISEÑO 3D)
       ═══════════════════════════════════════ */

    .envelope-container {
        width: 90vw;
        max-width: 400px;
        aspect-ratio: 1.428;
        position: relative;
        margin: 15vh auto 40px auto;
        perspective: 1000px;
    }
    .envelope-container.arrive {
        animation: envelopeArrive 1.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }
    @keyframes envelopeArrive {
        0% { transform: translateY(100vh) scale(0.7) rotate(-5deg); opacity: 0; }
        100% { transform: translateY(0) scale(1) rotate(0deg); opacity: 1; }
    }

    .envelope {
        position: relative;
        width: 100%;
        height: 100%;
        background: #4A5B46; 
        border-radius: 8px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    }

    .letter {
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        height: 90%;
        background: #fff;
        border-radius: 8px;
        z-index: 1;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
        text-align: center;
        background-image: linear-gradient(135deg, #fff 0%, #f9f5f0 100%);
    }

    .letter-content {
        font-family: 'Cormorant Garamond', serif;
        color: #7a8c6e;
    }
    .letter-title {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        font-size: 3rem;
        line-height: 1.2;
        margin-bottom: 0.2rem;
        color: #7a8c6e;
        white-space: nowrap;
    }
    .letter-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 3px;
        color: #a3b899;
        text-transform: uppercase;
    }

    .flap-left {
        position: absolute;
        top: 0; left: 0;
        width: 50%; height: 100%;
        background: #556B51;
        clip-path: polygon(0 0, 100% 50%, 0 100%);
        z-index: 2;
        border-radius: 8px 0 0 8px;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    }
    .flap-right {
        position: absolute;
        top: 0; right: 0;
        width: 50%; height: 100%;
        background: #556B51;
        clip-path: polygon(100% 0, 0 50%, 100% 100%);
        z-index: 2;
        border-radius: 0 8px 8px 0;
        box-shadow: -2px 0 5px rgba(0,0,0,0.05);
    }
    .flap-bottom {
        position: absolute;
        bottom: 0; left: 0;
        width: 100%; height: 60%;
        background: #5E755A;
        clip-path: polygon(0 100%, 50% 0, 100% 100%);
        z-index: 3;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
    }
    .flap-top-wrapper {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 65%;
        z-index: 4;
        transform-origin: top;
    }
    .flap-top-shape {
        width: 100%; height: 100%;
        background: #3E4D3B;
        clip-path: polygon(0 0, 50% 100%, 100% 0);
        border-radius: 8px 8px 0 0;
    }

    @keyframes pulse-vibrate {
        0% { transform: translate(-50%, -50%) scale(1); box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.7); }
        50% { transform: translate(-50%, -50%) scale(1.05); box-shadow: 0 0 20px 10px rgba(212, 175, 55, 0); }
        100% { transform: translate(-50%, -50%) scale(1); box-shadow: 0 0 0 0 rgba(212, 175, 55, 0); }
    }
    .wax-seal {
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 110px;
        height: 110px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10;
        animation: pulse-vibrate 2s infinite ease-in-out;
        
        /* Efecto 3D de cera dorada puro CSS */
        background: radial-gradient(ellipse at 30% 30%, #f9d976 0%, #d4af37 40%, #aa801b 80%, #684a04 100%);
        box-shadow: 
            inset 0 4px 6px rgba(255, 255, 255, 0.6), 
            inset 0 -4px 6px rgba(0, 0, 0, 0.5),      
            0 5px 15px rgba(0, 0, 0, 0.4);            
        border: 1px solid #b58d24; 
    }
    
    /* Anillo interior para dar realismo al sello */
    .wax-seal::before {
        content: '';
        position: absolute;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        border: 2px solid rgba(0,0,0,0.15);
        box-shadow: 
            inset 0 2px 4px rgba(0,0,0,0.3),
            0 2px 2px rgba(255,255,255,0.4);
        pointer-events: none;
    }

    .seal-text {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 700;
        color: #d4af37; 
        font-size: 2.2rem;
        line-height: 1;
        white-space: nowrap;
        text-shadow: -1px -1px 1px rgba(255, 255, 255, 0.7), 1px 1px 3px rgba(0, 0, 0, 0.8);
        margin-top: 3px;
        letter-spacing: 1px;
        z-index: 2; 
        position: relative;
    }
    .seal-text .ampersand-seal {
        font-family: 'Great Vibes', cursive;
        font-weight: 400;
        font-size: 1.8rem;
        margin: 0 2px;
    }

    /* Animaciones de apertura */
    @keyframes openFlap {
        0% { transform: rotateX(0deg); z-index: 4; }
        100% { transform: rotateX(180deg); z-index: 0; }
    }
    @keyframes slideLetter {
        0% { transform: translate(-50%, 0); z-index: 1; }
        100% { transform: translate(-50%, -120px); z-index: 1; }
    }

    .envelope-opening .flap-top-wrapper {
        animation: openFlap 1s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    .envelope-opening .letter {
        animation: slideLetter 1.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        animation-delay: 0.5s;
    }

    .envelope-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(160deg, #fdf6f0 0%, #f5ebe0 30%, #faf3ed 60%, #f0e6d8 100%);
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
        animation: hideOverlay 2.5s forwards;
    }
    @keyframes hideOverlay {
        0%, 80% { opacity: 1; visibility: visible; }
        100% { opacity: 0; visibility: hidden; pointer-events: none; }
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


# ═════════════════════════════════════════════
# PANTALLA 1: SOBRE ELEGANTE (INTERACTIVO)
# ═════════════════════════════════════════════
if st.session_state.envelope_state == "closed":

    # CSS para hacer el botón invisible a pantalla completa
    st.markdown("""
    <style>
        .stButton[data-testid="stButton"] {
            position: fixed !important;
            inset: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 9999 !important;
        }
        .stButton[data-testid="stButton"] button {
            width: 100% !important;
            height: 100% !important;
            background: transparent !important;
            border: none !important;
            color: transparent !important;
            box-shadow: none !important;
        }
        .stButton[data-testid="stButton"] button:hover {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    envelope_class = "envelope-container arrive envelope-closed"
    
    # Renderizamos el sobre HTML
    st.markdown(f"""
    <div class="{envelope_class}">
        <div class="envelope">
            <div class="letter">
                <div class="letter-content">
                    <div class="letter-title">A <span style="font-family: 'Great Vibes', cursive; font-size: 2.5rem;">&amp;</span> O</div>
                    <div class="letter-subtitle">Estáis Invitados</div>
                </div>
            </div>
            <div class="flap-left"></div>
            <div class="flap-right"></div>
            <div class="flap-bottom"></div>
            <div class="flap-top-wrapper">
                <div class="flap-top-shape"></div>
                <div class="wax-seal">
                    <div class="seal-text">A <span class="ampersand-seal">&amp;</span> O</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Botón invisible a pantalla completa
    if st.button(" ", key="open_envelope", use_container_width=True):
        st.session_state.envelope_state = "opened"
        st.rerun()

# ═════════════════════════════════════════════
# PANTALLA 2: INVITACIÓN COMPLETA
# ═════════════════════════════════════════════
elif st.session_state.envelope_state == "opened":

    # Overlay de animación fluida del sobre abriéndose
    st.markdown(f"""
    <div class="envelope-overlay">
        <div class="envelope-container envelope-opening">
            <div class="envelope">
                <div class="letter">
                    <div class="letter-content">
                    <div class="letter-title">A <span style="font-family: 'Great Vibes', cursive; font-size: 2.5rem;">&amp;</span> O</div>
                    <div class="letter-subtitle">Estáis Invitados</div>
                </div>
                </div>
                <div class="flap-left"></div>
                <div class="flap-right"></div>
                <div class="flap-bottom"></div>
                <div class="flap-top-wrapper">
                    <div class="flap-top-shape"></div>
                    <div class="wax-seal">
                        <div class="seal-text">A <span class="ampersand-seal">&amp;</span> O</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
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
                if GSPREAD_AVAILABLE and "gcp_service_account" in st.secrets:
                    try:
                        scope = [
                            "https://spreadsheets.google.com/feeds",
                            "https://www.googleapis.com/auth/drive",
                        ]
                        creds = Credentials.from_service_account_info(
                            dict(st.secrets["gcp_service_account"]),
                            scopes=scope,
                        )
                        client = gspread.authorize(creds)
                        sheet = client.open(st.secrets["spreadsheet_name"]).sheet1
                        sheet.append_row(fila)
                        guardado = True
                    except Exception as e:
                        st.warning(f"⚠️ No se pudo guardar en Google Sheets: {e}")

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
