import streamlit as st
import inicio
from simulations import (
    hydraulic_force,
    electric_field,
    standing_waves,
    optical_mirage,
)


st.set_page_config(
    page_title="Física para Ciencias de la Computación",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


SECCIONES = [
    "🏠 Inicio",
    "📐 DDA — Fuerza hidráulica",
    "⚡ DDB — Campo eléctrico",
    "〰️ DDC — Ondas estacionarias",
    "🌅 DDD — Espejismo óptico",
]


PAGINAS = {
    "🏠 Inicio": inicio,
    "📐 DDA — Fuerza hidráulica": hydraulic_force,
    "⚡ DDB — Campo eléctrico": electric_field,
    "〰️ DDC — Ondas estacionarias": standing_waves,
    "🌅 DDD — Espejismo óptico": optical_mirage,
}


# ── Menú lateral ──────────────────────────────────────────────────────────────
st.sidebar.title("🔬 Física — Simulaciones")
st.sidebar.markdown("---")


if "ir_a" in st.session_state:
    st.session_state["seccion"] = st.session_state.pop("ir_a")


if "seccion" not in st.session_state:
    st.session_state["seccion"] = "🏠 Inicio"


seccion = st.sidebar.radio(
    "Selecciona la entrega:",
    SECCIONES,
    index=SECCIONES.index(st.session_state["seccion"]),
    key="seccion",
)


st.sidebar.markdown("---")
st.sidebar.caption("Física para Ciencias de la Computación")


# ── Enrutamiento ──────────────────────────────────────────────────────────────
PAGINAS[seccion].mostrar()