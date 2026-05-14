import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(
    page_title="MindREM - Elige tu Enfoque",
    page_icon="🧠",
    layout="centered"
)

# REFUERZO DE LEGIBILIDAD: CSS para hacer las letras súper negras y visibles
st.markdown("""
    <style>
    /* Forzar que todos los textos principales, etiquetas y párrafos sean negros intensos y firmes */
    html, body, p, label, [data-testid="stWidgetLabel"] p, .stMarkdown p {
        color: #111111 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    /* Hacer los títulos principales aún más fuertes y destacados */
    h1, h2, h3, h4 {
        color: #004A90 !important; /* Azul oscuro corporativo, muy legible */
        font-weight: 800 !important;
    }
    /* Resaltar las aclaraciones/captions pequeños para que no se pierdan */
    .stCaption {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    /* Poner los textos de los botones en negrita */
    button p {
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 MindREM")
st.subheader("¿Qué mundo prefieres explorar hoy?")
st.write("Escribe tu sueño, personaliza las opciones de abajo y elige tu enfoque.")

# 2. MEMORIA DE LA SESIÓN (Evita que los datos se borren al descargar)
if "ver_reporte" not in st.session_state:
    st.session_state.ver_reporte = False
if "texto_pantalla" not in st.session_state:
    st.session_state.texto_pantalla = ""
if "texto_oculto" not in st.session_state:
    st.session_state.texto_oculto = ""
if "enfoque_activo" not in st.session_state:
    st.session_state.enfoque_activo = ""

# 3. PROMPTS CENTRALES
PROMPT_CIENTIFICO_UNIFICADO = """
Eres un experto que combina la Psicología Cognitiva amigable y la Neurobiología académica. Analiza el sueño de forma sintética.
DEBES SEPARAR TU RESPUESTA EN DOS PARTES USANDO EXACTAMENTE EL MARCADOR "===SEPARADOR===" en una línea sola.

PARTE 1:
### 🧠 Lo que tu mente procesó anoche
[Explica por qué el cerebro procesó esa emoción en base a su contexto]
### 🔮 Tu metáfora visual
[Explica el escenario como un reflejo simple de su vida despierto]
### ⚡ Hack de Bienestar para hoy
[Una acción física o mental de 1 minuto para equilibrar esa emoción hoy]

===SEPARADOR===

PARTE 2:
**Región Cerebral Activa:** [Menciona partes como Amígdala o Corteza Prefrontal y su acción]
**Química de la Fase REM:** [Menciona niveles de Acetilcolina o Dopamina en este sueño]
"""

PROMPT_HINDU = """
Eres un sabio experto en la filosofía del Hinduismo y el Svapna Shastra. Tu tono es espiritual y profundo.
ESTRUCTURA DE RESPUESTA:
### 🌌 Tu Impresión Kármica (Samskaras)
[Explica cómo este sueño es tu alma liberando miedos o deseos guardados (Samskaras) para limpiar tu Karma]
### 🔮 Simbología del Svapna Shastra
[Busca elementos del sueño y tradúcelos usando los presagios auténticos del tratado védico]
### 🧘 Consejo para el Alma (Dharma)
[Da un consejo espiritual enfocado en la paz interior o el desapego]
"""

# 4. CONFIGURACIÓN DE LA BARRA LATERAL
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Gemini API Key:", type="password")

# 5. FORMULARIO DE ENTRADA
relato = st.text_area("¿Qué soñaste?", placeholder="Narra aquí tu sueño...", height=150)

st.caption("👇 Personaliza estos datos para un análisis más exacto:")

col1, col2 = st.columns(2)
with col1:
    emocion = st.selectbox(
        "¿Qué emoción sentiste más fuerte?", 
        ["Haz clic para elegir... 🎭", "Ansiedad 😰", "Frustración 😡", "Alivio 😌", "Tristeza 😢", "Confusión 😮"]
    )
with col2:
    contexto = st.text_input(
        "Contexto reciente (Opcional)", 
        placeholder="Ej: Estrés, cambios en el trabajo..."
    )

st.divider()

# Ajuste interno de variables
emocion_final = "No especificada claramente" if "Haz clic" in emocion else emocion
input_data = f"Sueño: {relato}. Emoción: {emocion_final}. Contexto: {contexto}"

# 6. BOTONES DE ACCIÓN
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("Análisis Científico 🧠", use_container_width=True):
        if not api_key:
            st.warning("Introduce tu API Key en la barra lateral.")
        elif not relato:
            st.error("Escribe un sueño primero.")
        else:
            with st.spinner("Analizando redes neuronales..."):
                try:
                    genai.configure(api_key=api_key)
                    model_cientifico = genai.GenerativeModel("gemini-2.5-flash", system_instruction=PROMPT_CIENTIFICO_UNIFICADO)
                    respuesta = model_cientifico.generate_content(input_data)
                    
                    if "===SEPARADOR===" in respuesta.text:
                        p_cog, p_bio = respuesta.text.split("===SEPARADOR===")
                    else:
                        p_cog, p_bio = respuesta.text, ""
                    
                    st.session_state.texto_pantalla = p_cog
                    st.session_state.texto_oculto = p_bio
                    st.session_state.enfoque_activo = "Científico"
                    st.session_state.ver_reporte = True
                except Exception as e:
                    st.error(f"Error: {e}")

with col_btn2:
    if st.button("Análisis Védico 🕉️", use_container_width=True):
        if not api_key:
            st.warning("Introduce tu API Key en la barra lateral.")
        elif not relato:
            st.error("Escribe un sueño primero.")
        else:
            with st.spinner("Consultando los tratados antiguos..."):
                try:
                    genai.configure(api_key=api_key)
                    model_hin = genai.GenerativeModel("gemini-2.5-flash", system_instruction=PROMPT_HINDU)
                    respuesta = model_hin.generate_content(input_data)
                    
                    st.session_state.texto_pantalla = respuesta.text
                    st.session_state.texto_oculto = ""
                    st.session_state.enfoque_activo = "Védico"
                    st.session_state.ver_reporte = True
                except Exception as e:
                    st.error(f"Error: {e}")

# 7. RENDERIZADO DEL REPORTE Y BOTÓN DE DESCARGA
if st.session_state.ver_reporte:
    st.divider()
    if st.session_state.enfoque_activo == "Científico":
        st.success("🔬 Enfoque Neuro-Cognitivo Completado")
        st.markdown(st.session_state.texto_pantalla)
        if st.session_state.texto_oculto:
            st.divider()
            with st.expander("🔬 Ver análisis neurobiológico avanzado (Solo Académicos)"):
                st.markdown(st.session_state.texto_oculto)
    else:
        st.success("🕉️ Enfoque Espiritual Completado")
        st.markdown(st.session_state.texto_pantalla)
    
    # Preparación del documento para descargar
    texto_descarga = f"MINDREM - REPORTE DE SUEÑO\nEnfoque: {st.session_state.enfoque_activo}\n\n"
    texto_descarga += f"SUEÑO RELATADO:\n{relato}\n\n"
    texto_descarga += f"ANÁLISIS:\n{st.session_state.texto_pantalla}\n"
    if st.session_state.texto_oculto:
        texto_descarga += f"\nANÁLISIS AVANZADO:\n{st.session_state.texto_oculto}"
    
    st.divider()
    st.download_button(
        label="📥 Descargar Reporte Completo (Formato Documento)",
        data=texto_descarga,
        file_name=f"MindREM_Reporte_{st.session_state.enfoque_activo}.txt",
        mime="text/plain",
        use_container_width=True
    )