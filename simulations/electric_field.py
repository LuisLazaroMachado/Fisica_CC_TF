import numpy as np
import matplotlib.pyplot as plt
from math import pi
from matplotlib.ticker import FuncFormatter
import streamlit as st
import streamlit.components.v1 as components
# =========================================================
# FÍSICA PARA CIENCIAS DE LA COMPUTACIÓN
# DDB - Parte 1
# Campo eléctrico de una barra infinita cargada
# Método numérico: Regla del trapecio
# =========================================================
# =========================================================
# CONSTANTES FÍSICAS
# =========================================================
epsilon0 = 8.85e-12
k = 9.00e9
# =========================================================
# PARÁMETROS DEL PROBLEMA
# =========================================================
lam = 40.0e-9
# Límite superior de integración.
# Se aproxima la barra infinita como:
# integral de -∞ a +∞ ≈ 2 integral de 0 a L
L = 100.0 # m representa la longitud de la barra usada para aproximar la barra infinita
dy = 0.0100 # Paso de integración (intervalo entre puntos en y)
N = int(L / dy) # Número de intervalos para la integración
x_values = np.linspace(2.00, 80.0, 200) # Valores de x desde 2.00 m hasta 80.0 m, con 200 puntos
# =========================================================
# FORMATO CON TRES CIFRAS SIGNIFICATIVAS Y COMA DECIMAL
# =========================================================
def formato_3_cifras(valor, posicion=None):
    """
    Muestra los valores de los ejes con tres cifras significativas
    y coma decimal.
    """
    if valor < 10:
        texto = f"{valor:.2f}"
    elif valor < 100:
        texto = f"{valor:.1f}"
    else:
        texto = f"{valor:.0f}"
    return texto.replace(".", ",")
def formato_tabla(valor):
    """
    Formato para la tabla de resultados con tres cifras significativas
    y coma decimal.
    """
    if valor < 10:
        texto = f"{valor:.2f}"
    elif valor < 100:
        texto = f"{valor:.1f}"
    else:
        texto = f"{valor:.0f}"
    return texto.replace(".", ",")

def mostrar():

    # =========================================================
    # DRAWER LATERAL — GUÍA PARA LA EXPOSICIÓN
    # =========================================================
    with st.sidebar:

        st.divider()

        st.subheader("1️⃣ Parámetros físicos")

        st.code("""
epsilon0 = 8.85e-12
k = 9.00e9
lam = 40.0e-9
L = 100.0
dy = 0.0100
        """, language="python")

        st.caption("""
        Definen las constantes físicas y la aproximación de la barra infinita.
        """)

        st.divider()

        st.subheader("2️⃣ Integrando del campo eléctrico")

        st.code("""
f = (2 * k * lam * x) / ((y**2 + x**2)**(3/2))
        """, language="python")

        st.caption("""
        Representa el aporte diferencial del campo producido por cada elemento
        de carga dq = λdy.
        """)

        st.divider()

        st.subheader("3️⃣ Regla del trapecio")

        st.code("""
area_trapecio = ((f[i] + f[i+1]) / 2) * dy

integral += area_trapecio
        """, language="python")

        st.caption("""
        Suma numéricamente las áreas de los trapecios para aproximar la integral.
        """)

        st.divider()

        st.subheader("4️⃣ Modelo teórico")

        st.code("""
E_teo = lam / (2 * pi * epsilon0 * x)
        """, language="python")

        st.caption("""
        Valor exacto esperado para una barra infinita.
        """)

        st.divider()

        st.subheader("5️⃣ Comparación y error")

        st.code("""
error = np.abs(
    (E_teorico - E_numerico)
    / E_teorico
) * 100
        """, language="python")

        st.caption("""
        Permite evaluar qué tan cerca está la aproximación numérica del modelo.
        """)

        st.divider()

    st.markdown("# ⚡ DDB — Campo eléctrico de una barra infinita cargada")
    st.markdown("---")
    st.markdown("""
### 🔌 ¿De qué trata ?
Una **barra infinita cargada** genera un campo eléctrico a su alrededor.
Quiero saber **con qué intensidad** ese campo empuja una carga de prueba
ubicada a una distancia `x` de la barra.

El problema es que la barra es infinita — no puedo sumar el aporte de
cada pedacito con álgebra simple. Necesito **integrar** el aporte de cada
elemento de carga `dq = λ·dy` a lo largo de toda la barra.
""")
    
    st.markdown("---")
    st.markdown("### 📐 ¿De dónde salen las fórmulas?")
    st.markdown("### 📌 Variables del problema")

    st.markdown("""
    <div style="
        background-color:#111827;
        padding:20px;
        border-radius:12px;
        border:1px solid #374151;
        color:white;
        font-size:16px;
    ">

    <table style="width:100%; border-collapse:collapse;">

    <tr>
    <th style="text-align:left; padding:8px; border-bottom:1px solid #555;">
    Variable
    </th>
    <th style="text-align:left; padding:8px; border-bottom:1px solid #555;">
    Significado
    </th>
    </tr>

    <tr>
    <td style="padding:8px;">λ (lambda)</td>
    <td style="padding:8px;">Densidad lineal de carga = 40,0 × 10⁻⁹ C/m</td>
    </tr>

    <tr>
    <td style="padding:8px;">x</td>
    <td style="padding:8px;">Distancia perpendicular desde la barra hasta el punto de medición (m)</td>
    </tr>

    <tr>
    <td style="padding:8px;">y</td>
    <td style="padding:8px;">Posición a lo largo de la barra — variable de integración (m)</td>
    </tr>

    <tr>
    <td style="padding:8px;">k</td>
    <td style="padding:8px;">Constante de Coulomb = 9,00 × 10⁹ N·m²/C²</td>
    </tr>

    <tr>
    <td style="padding:8px;">ε₀</td>
    <td style="padding:8px;">Permitividad del vacío = 8,85 × 10⁻¹² C²/(N·m²)</td>
    </tr>

    <tr>
    <td style="padding:8px;">dE</td>
    <td style="padding:8px;">Campo eléctrico diferencial producido por un elemento de carga (N/C)</td>
    </tr>

    <tr>
    <td style="padding:8px;">E</td>
    <td style="padding:8px;">Campo eléctrico total generado por la barra (N/C)</td>
    </tr>

    </table>

    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("**Paso 1 — Campo de un elemento de carga `dq`**")
        st.latex(r"dq = \lambda \, dy")
        st.latex(r"dE = \frac{k \cdot dq}{r^2} = \frac{k \cdot \lambda \, dy}{y^2 + x^2}")
        st.markdown("**Paso 2 — Solo la componente horizontal sobrevive** (por simetría, las verticales se cancelan):")
        st.latex(r"dE_x = dE \cdot \cos\theta = \frac{k \cdot \lambda \cdot x \, dy}{(y^2 + x^2)^{3/2}}")

    with col_f2:
        st.markdown("**Paso 3 — Integrar de 0 a L y multiplicar por 2** (simetría de la barra):")
        st.latex(r"E(x) = 2\int_0^L \frac{k \cdot \lambda \cdot x}{(y^2 + x^2)^{3/2}} \, dy")
        st.markdown("**Solución teórica exacta** (barra infinita, L → ∞):")
        st.latex(r"E(x) = \frac{\lambda}{2\pi\varepsilon_0 \cdot x}")
        st.caption("📌 Nota: k = 1/(4πε₀), por eso ambas expresiones son equivalentes.")

    st.markdown("**Integrando numérico** — lo que el código evalúa en cada punto `y`:")
    st.latex(r"f(y) = \frac{2 \cdot k \cdot \lambda \cdot x}{(y^2 + x^2)^{3/2}}")
    st.info("""
💡 El factor 2 aparece porque integro solo de 0 a L (mitad de la barra)
y la barra es simétrica. La otra mitad aporta exactamente lo mismo.
""")
    # =========================================================
    # MÉTODO NUMÉRICO DEL TRAPECIO
    # =========================================================
    E_numerico = []
    E_teorico = []
    for x in x_values:
        y = np.linspace(0, L, N + 1) # Valores de y desde 0 hasta L, con N+1 puntos (incluyendo el límite superior)
        f = (2 * k * lam * x) / ((y**2 + x**2)**(3/2)) # Función a integrar para el campo eléctrico, considerando la simetría de la barra
        integral = 0
        for i in range(N):
            area_trapecio = ((f[i] + f[i + 1]) / 2) * dy # Área del trapecio para el intervalo [y[i], y[i+1]]
            integral += area_trapecio
        E_numerico.append(integral)
        E_teo = lam / (2 * pi * epsilon0 * x) # Campo eléctrico teórico para una barra infinita cargada a distancia x
        E_teorico.append(E_teo)
    E_numerico = np.array(E_numerico)
    E_teorico = np.array(E_teorico)
    # =========================================================
    # ERROR PORCENTUAL
    # =========================================================
    error = np.abs((E_teorico - E_numerico) / E_teorico) * 100 # Error porcentual entre el método numérico y el modelo teórico
    # =========================================================
    # TABLA DE RESULTADOS PARA CONSOLA
    # =========================================================
    print("\n======================================================")
    print("                TABLA DE RESULTADOS")
    print("======================================================")
    print(f"{'x (m)':<12}{'E Numérico (N/C)':<22}{'E Teórico (N/C)':<22}{'Error %':<12}")
    for i in range(0, len(x_values), 20):
        print(
            f"{formato_tabla(x_values[i]):<12}"
            f"{formato_tabla(E_numerico[i]):<22}"
            f"{formato_tabla(E_teorico[i]):<22}"
            f"{formato_tabla(error[i]):<12}"
        )
    
    st.markdown("---")
    st.markdown("### 💻 ¿Cómo se conecta el código con la física?")
    st.markdown("""
| Concepto físico | Línea en el código |
|---|---|
| Integrando `f(y) = 2kλx/(y²+x²)^(3/2)` | `f = (2 * k * lam * x) / ((y**2 + x**2)**(3/2))` |
| Área de cada trapecio `(f(yᵢ)+f(yᵢ₊₁))/2 · Δy` | `area_trapecio = ((f[i] + f[i+1]) / 2) * dy` |
| Suma de todos los trapecios | `integral += area_trapecio` — bucle `for i in range(N)` |
| Solución teórica `E = λ/(2πε₀x)` | `E_teo = lam / (2 * pi * epsilon0 * x)` |
| Error porcentual | `error = abs((E_teorico - E_numerico) / E_teorico) * 100` |
""")
    st.caption("📌 Abrir el drawer lateral para señalar esas líneas exactas.")

    # =========================================================
    # SLIDER INTERACTIVO DE POSICIÓN x
    # =========================================================
    x_sel = st.slider(
        "Distancia a la barra x (m)",
        min_value=float(x_values.min()),
        max_value=float(x_values.max()),
        value=float(x_values.min()),
        step=0.5
    )
    idx_sel = int(np.argmin(np.abs(x_values - x_sel)))
    col1, col2, col3 = st.columns(3)
    col1.metric("E numérico (N/C)", formato_tabla(E_numerico[idx_sel]))
    col2.metric("E teórico (N/C)",  formato_tabla(E_teorico[idx_sel]))
    col3.metric("Error (%)",        f"{error[idx_sel]:.4f}")
    # =========================================================
    # GRÁFICAS MATPLOTLIB — una debajo de la otra
    # =========================================================
    # ---------------------------------------------------------
    # Gráfica 1: Método numérico
    # ---------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(13, 5))
    ax1.plot(
        x_values,
        E_numerico,
        linewidth=2.5,
        label="Método numérico: regla del trapecio"
    )
    ax1.axvline(x_sel, color="orange", linestyle="--", linewidth=2,
                label=f"x = {formato_tabla(x_sel)} m")
    ax1.set_title("Gráfico campo eléctrico vs posición (Método numérico)",
                  fontsize=13, fontweight="bold", pad=8)
    ax1.set_xlabel("Posición x (m)", fontsize=11, labelpad=8)
    ax1.set_ylabel("Campo eléctrico E (N/C)", fontsize=11)
    ax1.grid(True)
    ax1.legend(loc="best", fontsize=9)
    ax1.xaxis.set_major_formatter(FuncFormatter(formato_3_cifras))
    ax1.yaxis.set_major_formatter(FuncFormatter(formato_3_cifras))
    st.pyplot(fig1)
    plt.close(fig1)
    # ---------------------------------------------------------
    # Gráfica 2: Modelo teórico
    # ---------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(13, 5))
    ax2.plot(
        x_values,
        E_teorico,
        linewidth=2.5,
        label="Modelo teórico: barra infinita"
    )
    ax2.axvline(x_sel, color="orange", linestyle="--", linewidth=2,
                label=f"x = {formato_tabla(x_sel)} m")
    ax2.set_title("Gráfico campo eléctrico vs posición (Modelo teórico)",
                  fontsize=13, fontweight="bold", pad=8)
    ax2.set_xlabel("Posición x (m)", fontsize=11, labelpad=8)
    ax2.set_ylabel("Campo eléctrico E (N/C)", fontsize=11)
    ax2.grid(True)
    ax2.legend(loc="best", fontsize=9)
    ax2.xaxis.set_major_formatter(FuncFormatter(formato_3_cifras))
    ax2.yaxis.set_major_formatter(FuncFormatter(formato_3_cifras))
    st.pyplot(fig2)
    plt.close(fig2)
    # ---------------------------------------------------------
    # Gráfica 3: Comparación numérico vs teórico
    # ---------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(13, 5))
    ax3.plot(x_values, E_numerico, linewidth=2.5,
             label="Método numérico: regla del trapecio")
    ax3.plot(x_values, E_teorico, linestyle="--", linewidth=2.5,
             label="Modelo teórico: barra infinita")
    ax3.axvline(x_sel, color="orange", linestyle="--", linewidth=2,
                label=f"x = {formato_tabla(x_sel)} m")
    ax3.set_title("Gráfico campo eléctrico vs posición (Método numérico y modelo teórico)",
                  fontsize=13, fontweight="bold", pad=8)
    ax3.set_xlabel("Posición x (m)", fontsize=11, labelpad=8)
    ax3.set_ylabel("Campo eléctrico E (N/C)", fontsize=11)
    ax3.grid(True)
    ax3.legend(loc="best", fontsize=9)
    ax3.xaxis.set_major_formatter(FuncFormatter(formato_3_cifras))
    ax3.yaxis.set_major_formatter(FuncFormatter(formato_3_cifras))
    st.pyplot(fig3)
    plt.close(fig3)
    # ---------------------------------------------------------
    # Gráfica 4: Trapecios
    # ---------------------------------------------------------
    fig4, ax4 = plt.subplots(figsize=(13, 5))
    # Valor fijo de x para mostrar cómo se aplica la regla del trapecio
    x_muestra = 2.00
    # Intervalo mostrado para la variable de integración y
    L_muestra = 20.0
    # Paso visual para los trapecios.
    # Se usa un paso grande solo para que los trapecios se distingan.
    dy_trapecio = 0.1
    # Puntos finos para dibujar la función suavemente
    y_suave = np.linspace(0, L_muestra, 1000)
    f_suave = (
        2 * k * lam * x_muestra
    ) / ((y_suave**2 + x_muestra**2)**(3/2))
    # Puntos gruesos para construir los trapecios
    y_trap = np.arange(0, L_muestra + dy_trapecio, dy_trapecio)
    f_trap = (
        2 * k * lam * x_muestra
    ) / ((y_trap**2 + x_muestra**2)**(3/2))
    # Dibujar trapecios sin alterar la curva real
    for i in range(len(y_trap) - 1):
        # Vértices del trapecio:
        # (y_i, 0), (y_i, f_i), (y_{i+1}, f_{i+1}), (y_{i+1}, 0)
        xs = [y_trap[i], y_trap[i], y_trap[i + 1], y_trap[i + 1]]
        ys = [0, f_trap[i], f_trap[i + 1], 0]
        ax4.fill(xs, ys, alpha=0.22, edgecolor="red", linewidth=1.2,
                 label="Trapecios de integración" if i == 0 else None)
        # Líneas verticales rojas, como en el esquema del enunciado
        ax4.plot([y_trap[i], y_trap[i]], [0, f_trap[i]],
                 color="red", linewidth=1)
    # Última línea vertical
    ax4.plot([y_trap[-1], y_trap[-1]], [0, f_trap[-1]],
             color="red", linewidth=1)
    # Dibujar la función real encima de los trapecios
    ax4.plot(y_suave, f_suave, linewidth=3,
             label="Integrando del campo eléctrico")
    ax4.set_title(
        "Representación de la regla del trapecio aplicada al integrando del campo eléctrico",
        fontsize=13, fontweight="bold", pad=8)
    ax4.set_xlabel("Posición sobre la barra, y (m)", fontsize=11, labelpad=8)
    ax4.set_ylabel("Integrando f(y) (N/C·m)", fontsize=11)
    ax4.grid(True)
    ax4.legend(loc="best", fontsize=9)
    ax4.xaxis.set_major_formatter(FuncFormatter(formato_3_cifras))
    ax4.yaxis.set_major_formatter(FuncFormatter(formato_3_cifras))
    st.pyplot(fig4)
    plt.close(fig4)
    # =========================================================
    # TABLA EN STREAMLIT
    # =========================================================
    st.markdown("### Tabla de resultados")
    indices_tabla = np.linspace(0, len(x_values) - 1, 6, dtype=int)
    datos = {
        "x (m)":            [formato_tabla(x_values[i]) for i in indices_tabla],
        "E numérico (N/C)": [formato_tabla(E_numerico[i]) for i in indices_tabla],
        "E teórico (N/C)":  [formato_tabla(E_teorico[i]) for i in indices_tabla],
        "Error (%)":        [formato_tabla(error[i]) for i in indices_tabla],
    }
    import pandas as pd
    st.dataframe(pd.DataFrame(datos), use_container_width=True)

    # =========================================================
    # ANIMACIÓN: barra cargada con partículas que salen radialmente
    # Las partículas salen más rápido y más juntas cerca de la barra
    # (campo fuerte) y más lento y espaciadas lejos (campo débil).
    # El slider de x mueve la línea de medición en tiempo real.
    # =========================================================
    E_en_x = float(lam / (2 * pi * epsilon0 * x_sel))
    E_max   = float(lam / (2 * pi * epsilon0 * x_values.min()))
    html_barra = f"""
<canvas id="cv" width="700" height="420"
        style="background:#0a0a1a;border-radius:10px;display:block;margin:auto;">
</canvas>
<script>
const canvas = document.getElementById("cv");
const ctx    = canvas.getContext("2d");
const W = canvas.width, H = canvas.height;
const CX = W * 0.18;          // centro x de la barra
const CY = H / 2;             // centro y
const x_sel  = {x_sel};       // distancia seleccionada (m)
const E_val  = {E_en_x};      // E en ese punto (N/C)
const E_max  = {E_max};       // E máximo (para normalizar)
const lam_js = {lam};
const k_js   = {k};
const eps0   = {epsilon0};
const pi     = Math.PI;
// Escala: cuántos píxeles por metro
const PX_POR_M = (W - CX - 30) / {float(x_values.max())};
// ── Partículas ──────────────────────────────────────────
const N_PART = 130;
let particulas = [];

function crearParticula(){{

    // Nace en cualquier punto de la barra
    const y0 = 35 + Math.random()*(H-70);

    // Sale únicamente hacia la derecha
    const ang = (Math.random()-0.5)*0.45;

    return{{
        x:CX,
        y:y0,
        ang:ang,
        dist:0,
        vida:0,
        vida_max:140+Math.random()*80
    }};
}}

for(let i=0;i<N_PART;i++){{
    const p=crearParticula();
    p.vida=Math.random()*p.vida_max;
    particulas.push(p);
}}

// ── Función para dibujar una flecha (línea + punta) ──────
function dibujarFlecha(x1, y1, x2, y2, color, grosor) {{
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = grosor;

    // Línea principal
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    // Punta de flecha (triángulo)
    const angulo = Math.atan2(y2 - y1, x2 - x1);
    const tamPunta = 5 + grosor; // tamaño proporcional al grosor
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(
        x2 - tamPunta * Math.cos(angulo - Math.PI / 6),
        y2 - tamPunta * Math.sin(angulo - Math.PI / 6)
    );
    ctx.lineTo(
        x2 - tamPunta * Math.cos(angulo + Math.PI / 6),
        y2 - tamPunta * Math.sin(angulo + Math.PI / 6)
    );
    ctx.closePath();
    ctx.fill();
}}

// ── Tiempo global para animar las flechas ────────────────
let tiempoFlechas = 0;

// ── Dibuja las flechas de campo eléctrico radiando de la barra ──
function dibujarFlechasCampo() {{
    const N_FILAS = 7;
    const N_COLUMNAS = 4;
    const x_max_flechas = {float(x_values.max())};
    const espacio_ciclo = x_max_flechas - 0.5; // recorrido total de cada flecha

    for (let fila = 0; fila < N_FILAS; fila++) {{
        const yy = 45 + fila * (H - 90) / (N_FILAS - 1);

        for (let col = 0; col < N_COLUMNAS; col++) {{
            // posición base de cada flecha en su "carril" (columna)
            const base = (col / N_COLUMNAS) * espacio_ciclo;

            // desplazamiento animado: avanza con el tiempo y vuelve a 0.5 al llegar al final
            const x_real = 0.5 + (base + tiempoFlechas) % espacio_ciclo;

            const campo = lam_js / (2 * pi * eps0 * x_real);
            const intensidad = Math.min(campo / E_max, 1);

            const px = CX + x_real * PX_POR_M;
            if (px > W - 20) continue;

            const largo = 14 + 26 * intensidad;
            const grosor = 1 + 2.5 * intensidad;
            const alpha = 0.35 + 0.65 * intensidad;

            dibujarFlecha(
                px, yy,
                px + largo, yy,
                `rgba(255,140,40,${{alpha}})`,
                grosor
            );
        }}
    }}

    // incrementa el tiempo: más rápido cerca de la barra estaría mejor,
    // pero un avance constante ya da un buen efecto de "flujo"
    tiempoFlechas += 0.15;
}}

// ── Loop principal ───────────────────────────────────────
function dibujar() {{
    ctx.clearRect(0, 0, W, H);
    // Fondo con gradiente radial (campo más fuerte cerca de la barra)
    const grd = ctx.createRadialGradient(CX, CY, 5, CX, CY, W * 0.8);
    grd.addColorStop(0,   "rgba(255,200,50,0.18)");
    grd.addColorStop(0.3, "rgba(80,120,255,0.08)");
    grd.addColorStop(1,   "rgba(0,0,0,0)");
    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, W, H);
    // ── Barra cargada (vertical, lado izquierdo) ──────────
    const grad_barra = ctx.createLinearGradient(CX - 8, 0, CX + 8, 0);
    grad_barra.addColorStop(0, "#ff8800");
    grad_barra.addColorStop(0.5, "#ffee44");
    grad_barra.addColorStop(1, "#ff8800");
    ctx.fillStyle = grad_barra;
    ctx.fillRect(CX - 6, 30, 12, H - 60);
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 1;
    ctx.strokeRect(CX - 6, 30, 12, H - 60);
    // Etiqueta barra
    ctx.fillStyle = "#ffee44";
    ctx.font = "bold 13px Arial";
    ctx.fillText("Barra", CX - 22, 22);
    ctx.fillText("+λ", CX - 10, H - 10);
    // ── Línea de medición en x_sel ────────────────────────
    const px_x = CX + x_sel * PX_POR_M;
    ctx.strokeStyle = "rgba(100,220,255,0.85)";
    ctx.lineWidth   = 2;
    ctx.setLineDash([6, 4]);
    ctx.beginPath();
    ctx.moveTo(px_x, 20);
    ctx.lineTo(px_x, H - 20);
    ctx.stroke();
    ctx.setLineDash([]);
    // Etiqueta x_sel
    ctx.fillStyle = "#64dcff";
    ctx.font = "12px Arial";
    ctx.fillText("x = " + x_sel.toFixed(1) + " m", px_x + 4, 32);
    // Valor E en esa línea
    const E_str = E_val > 1000
        ? (E_val / 1000).toFixed(1) + " kN/C"
        : E_val.toFixed(1) + " N/C";
    ctx.fillStyle = "#ffdd55";
    ctx.font = "bold 12px Arial";
    ctx.fillText("E = " + E_str, px_x + 4, 50);
    // ── Partículas (cargas positivas que salen radialmente) ──
    // ── Partículas ───────────────────────────────────────────
    for(let p of particulas){{

    p.vida++;

    if(p.vida>p.vida_max){{
        Object.assign(p,crearParticula());
    }}

    // velocidad depende de la distancia REAL a la barra
    const x_real=Math.max(0.15,p.dist/PX_POR_M);

    const campo=lam_js/(2*pi*eps0*x_real);
    const intensidad=Math.min(campo/E_max,1);
    const vel=0.4+7.0*intensidad;
    p.dist+=vel;

    const px=CX+p.dist*Math.cos(p.ang);
    const py=p.y+p.dist*Math.sin(p.ang);

    if(px>W+30){{
        Object.assign(p,crearParticula());
    }}

    const alpha=0.25+0.75*intensidad;
    const radio=2+2.5*intensidad;

    ctx.beginPath();
    ctx.arc(px,py,radio,0,2*Math.PI);
    ctx.fillStyle=`rgba(255,220,80,${{alpha}})`;
    ctx.fill();

    ctx.fillStyle=`rgba(255,255,255,${{alpha}})`;
    ctx.font="bold 8px Arial";
    ctx.fillText("+",px-2,py+3);
}}
    // ── Líneas de campo ──────────────────────────────────────
const N_LINEAS=18;

for(let i=0;i<N_LINEAS;i++){{

    const yy=35+i*(H-70)/(N_LINEAS-1);

    ctx.beginPath();

    for(let xx=0;xx<520;xx+=10){{

        const xr=Math.max(0.3,xx/PX_POR_M);
        const campo=lam_js/(2*pi*eps0*xr);
        const intensidad=Math.min(campo/E_max,1);
        const amp=6*intensidad;
        const y=yy+Math.sin(xx*0.03+i)*amp;

        if(xx===0)
            ctx.moveTo(CX,y);
        else
            ctx.lineTo(CX+xx,y);
    }}

    ctx.strokeStyle="rgba(80,180,255,0.35)";
    ctx.lineWidth=1+2*(E_val/E_max);
    ctx.stroke();
}}
    dibujarFlechasCampo();

    // ── Panel de datos ────────────────────────────────────
    ctx.fillStyle   = "rgba(0,0,0,0.65)";
    const px_box = 550 ;
    const py_box = H/2 - 50;
    ctx.fillRect(px_box, py_box, 120, 95);
    ctx.strokeStyle = "rgba(255,255,255,0.25)";
    ctx.lineWidth   = 1;
    ctx.strokeRect(px_box, py_box, 120, 95);
    ctx.fillStyle = "white";
    ctx.font = "bold 12px Arial";
    ctx.fillText("📊 Parámetros", px_box + 10, py_box + 20);
    ctx.font = "12px Arial";
    ctx.fillStyle = "#aef";
    ctx.fillText("λ = 40,0 × 10⁻⁹ C/m", px_box + 10, py_box + 40);
    ctx.fillStyle = "#ffa";
    ctx.fillText("x = " + x_sel.toFixed(1) + " m", px_box + 10, py_box + 57);
    ctx.fillStyle = "#aff";
    ctx.fillText("E = " + E_str, px_box + 10, py_box + 74);
    requestAnimationFrame(dibujar);
}}
dibujar();
</script>
"""
    st.markdown("### 🌊 Visualización: campo eléctrico de la barra cargada")
    st.caption("Las partículas representan cargas positivas empujadas por el campo. "
               "Cerca de la barra salen más rápido (campo fuerte). "
               "Mové el slider para ver cómo cambia E con la distancia.")
    components.html(html_barra, height=440)
    # =========================================================
    # ANÁLISIS
    # =========================================================
    print("\n======================================================")
    print("                     ANÁLISIS")
    print("======================================================")
    print("""
1. El campo eléctrico disminuye al aumentar la distancia x, 
   lo cual concuerda con el modelo teórico E = λ/(2πε0x).
2. El método numérico aproxima correctamente el comportamiento
   del modelo teórico, ya que ambas gráficas presentan una tendencia
   decreciente de tipo inversamente proporcional.
3. Las diferencias entre el método numérico y el modelo teórico se deben
   a la discretización de la integral mediante la regla del trapecio y a que
   la barra infinita se aproxima usando un límite finito L = 100,0 m.
4. Para valores pequeños de x, la aproximación numérica es más cercana
   al modelo teórico. Para valores grandes de x, el error puede aumentar
   porque la longitud finita usada en la integración representa peor
   a una barra infinita.
5. Si se disminuye Δy o se aumenta el valor de L, la aproximación numérica
   mejora, aunque también aumenta el costo computacional.
""")
    
    st.markdown("---")
    st.markdown("### ✅ Conclusiones")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.success(f"""
**¿Se cumplió el objetivo?**
Sí. En x = {x_sel:.1f} m se obtuvo E numérico = {formato_tabla(E_numerico[idx_sel])} N/C
frente al valor teórico de {formato_tabla(E_teorico[idx_sel])} N/C,
con un error de {error[idx_sel]:.4f}%.
""")
        st.info("""
**¿Por qué el error es bajo para x pequeño?**
Cerca de la barra (x pequeño), los extremos de la barra a ±100 m
contribuyen muy poco al campo — la integral converge rápido.
Con L = 100 m es suficiente para aproximar la barra infinita.
""")
    with col_c2:
        st.warning("""
**Limitación del método**
Para x grande (ej. 80 m), los extremos de la barra a ±100 m
todavía aportan campo no despreciable. Una barra verdaderamente
infinita aportaría más — por eso el error aumenta con x.
""")
        st.info("""
**Ventaja computacional**
Con Δy = 0,01 m y L = 100 m uso 10.000 intervalos por cada punto x.
Eso da una aproximación muy precisa de la integral en todo el rango.
""")
