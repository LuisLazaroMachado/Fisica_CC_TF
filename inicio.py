import streamlit as st

def mostrar():
    st.title("🔬 Física para Ciencias de la Computación")
    st.markdown("#### Simulaciones interactivas — Actividades de Desempeño")
    st.markdown("---")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown("### 📐 DDA")
            st.markdown("**Fuerza hidráulica sobre un dique**")
            st.markdown("Método del trapecio. Slider de altura H con trapecios en tiempo real.")
            if st.button("Ir a DDA →", key="btn_dda", use_container_width=True):
                st.session_state["ir_a"] = "📐 DDA — Fuerza hidráulica"
                st.rerun()

        st.markdown("")

        with st.container(border=True):
            st.markdown("### 〰️ DDC")
            st.markdown("**Ondas estacionarias en una cuerda**")
            st.markdown("Diferencias finitas 2do orden. Slider de tiempo que anima la onda.")
            if st.button("Ir a DDC →", key="btn_ddc", use_container_width=True):
                st.session_state["ir_a"] = "〰️ DDC — Ondas estacionarias"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### ⚡ DDB")
            st.markdown("**Campo eléctrico de una barra cargada**")
            st.markdown("Regla del trapecio. Slider de distancia x, numérico vs teórico.")
            if st.button("Ir a DDB →", key="btn_ddb", use_container_width=True):
                st.session_state["ir_a"] = "⚡ DDB — Campo eléctrico"
                st.rerun()

        st.markdown("")

        with st.container(border=True):
            st.markdown("### 🌅 DDD")
            st.markdown("**Espejismo óptico**")
            st.markdown("Runge-Kutta 4to orden. Trayectoria con fondo térmico y ángulo local.")
            if st.button("Ir a DDD →", key="btn_ddd", use_container_width=True):
                st.session_state["ir_a"] = "🌅 DDD — Espejismo óptico"
                st.rerun()

    st.markdown("---")
    st.markdown("👈 También podés usar el **menú lateral** para navegar.")