import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.signal import find_peaks
import math
import json
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# FÍSICA PARA CIENCIAS DE LA COMPUTACIÓN
# DDC - Parte 1
# Ondas estacionarias en una cuerda
# Método numérico: Diferencias finitas de 2do orden
# =========================================================

def tres_cifras_significativas(v, _=None, sig=3):
    if v == 0:
        return "0"
    decimales = sig - 1 - int(math.floor(math.log10(abs(v))))
    decimales = max(0, decimales)
    return f"{v:.{decimales}f}"

def mostrar():

    # =========================================================
    # SIDEBAR — CÓDIGO MATEMÁTICO PARA LA EXPOSICIÓN
    # =========================================================
    with st.sidebar:
        st.divider()
        st.subheader("1️⃣ Parámetros del sistema")
        st.code("""
L = 2.50        # longitud (m)
tension = 150   # tensión (N)
mu = 8.00e-3    # densidad lineal (kg/m)
A = 2.00e-2     # amplitud (m)
n_modo = 7      # modo
dx = 1.00e-2    # paso espacial (m)
        """, language="python")
        st.divider()
        st.subheader("2️⃣ Velocidad y frecuencia")
        st.code("""
v = np.sqrt(tension / densidad_lineal)
k_n = n_modo * np.pi / L
omega = k_n * v
f_osc = omega / (2 * np.pi)
T_per = 1.0 / f_osc
        """, language="python")
        st.divider()
        st.subheader("3️⃣ Condición de Courant")
        st.code("""
dt = 0.90 * dx / velocidad
a  = velocidad * dt / dx
# Se requiere a <= 1 para estabilidad
        """, language="python")
        st.divider()
        st.subheader("4️⃣ Condición inicial (onda exacta)")
        st.code("""
u_prev = 2*A*sin(k_n*x)*sin(omega*0)
u_curr = u_prev + dt*2*A*omega*sin(k_n*x)*cos(omega*0)
        """, language="python")
        st.divider()
        st.subheader("5️⃣ Diferencias finitas 2do orden")
        st.code("""
u_next[1:-1] = (
    2*u_curr[1:-1]
    - u_prev[1:-1]
    + a**2 * (
        u_curr[2:]
        - 2*u_curr[1:-1]
        + u_curr[:-2]
    )
)
u_next[0]  = 0.0  # extremo fijo
u_next[-1] = 0.0  # extremo fijo
        """, language="python")
        st.divider()

    # =========================================================
    # BLOQUE 1 — TÍTULO E INTRODUCCIÓN
    # =========================================================
    st.markdown("# 〰️ DDC — Ondas estacionarias en una cuerda tensa")
    st.markdown("---")
    st.markdown("""
### 🎻 ¿De qué trata?

Una **cuerda tensa fija en sus dos extremos** (como la cuerda de una guitarra)
puede vibrar de formas muy específicas llamadas **modos normales**.
Cuando la cuerda vibra en un modo, no se mueve como una ola que viaja
de un lado al otro — en cambio, ciertos puntos **nunca se mueven** (nodos)
y otros oscilan con la **máxima amplitud posible** (antinodos).

El objetivo es simular numéricamente cómo evoluciona esta vibración en el
tiempo usando **diferencias finitas de 2do orden**, y comparar el resultado
con la solución exacta analítica.
""")

    # =========================================================
    # BLOQUE 2 — VARIABLES DEL PROBLEMA
    # =========================================================
    st.markdown("---")
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
<th style="text-align:left; padding:8px; border-bottom:1px solid #555;">Variable</th>
<th style="text-align:left; padding:8px; border-bottom:1px solid #555;">Significado</th>
<th style="text-align:left; padding:8px; border-bottom:1px solid #555;">Valor</th>
</tr>
<tr><td style="padding:8px;">L</td><td style="padding:8px;">Longitud de la cuerda (m)</td><td style="padding:8px;">2,50 m</td></tr>
<tr><td style="padding:8px;">T</td><td style="padding:8px;">Tensión en la cuerda (N)</td><td style="padding:8px;">150 N</td></tr>
<tr><td style="padding:8px;">μ (mu)</td><td style="padding:8px;">Densidad lineal de masa (kg/m)</td><td style="padding:8px;">8,00×10⁻³ kg/m</td></tr>
<tr><td style="padding:8px;">A</td><td style="padding:8px;">Amplitud de la onda (m)</td><td style="padding:8px;">2,00×10⁻² m</td></tr>
<tr><td style="padding:8px;">n</td><td style="padding:8px;">Modo de vibración</td><td style="padding:8px;">7</td></tr>
<tr><td style="padding:8px;">v</td><td style="padding:8px;">Velocidad de propagación de la onda (m/s)</td><td style="padding:8px;">calculada</td></tr>
<tr><td style="padding:8px;">kₙ</td><td style="padding:8px;">Número de onda del modo n (rad/m)</td><td style="padding:8px;">calculado</td></tr>
<tr><td style="padding:8px;">ω</td><td style="padding:8px;">Frecuencia angular (rad/s)</td><td style="padding:8px;">calculada</td></tr>
<tr><td style="padding:8px;">f</td><td style="padding:8px;">Frecuencia de oscilación (Hz)</td><td style="padding:8px;">calculada</td></tr>
<tr><td style="padding:8px;">T_per</td><td style="padding:8px;">Período de la onda (s)</td><td style="padding:8px;">calculado</td></tr>
<tr><td style="padding:8px;">Δx</td><td style="padding:8px;">Paso espacial (m)</td><td style="padding:8px;">1,00×10⁻² m</td></tr>
<tr><td style="padding:8px;">Δt</td><td style="padding:8px;">Paso temporal (s)</td><td style="padding:8px;">calculado (Courant)</td></tr>
<tr><td style="padding:8px;">a</td><td style="padding:8px;">Número de Courant (adimensional)</td><td style="padding:8px;">debe ser ≤ 1 para NO divergir</td></tr>
</table>
</div>
""", unsafe_allow_html=True)

    # =========================================================
    # BLOQUE 3 — FUNDAMENTO FÍSICO Y MODELO MATEMÁTICO
    # =========================================================
    st.markdown("---")
    st.markdown("### 📐 ¿De dónde salen las fórmulas?")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("**Paso 1 — Ecuación de onda**")
        st.markdown("La dinámica de la cuerda está gobernada por la ecuación de onda:")
        st.latex(r"\frac{\partial^2 y}{\partial t^2} = v^2 \frac{\partial^2 y}{\partial x^2}")
        st.markdown("donde la velocidad de propagación depende de la tensión y la densidad:")
        st.latex(r"v = \sqrt{\frac{T}{\mu}}")

        st.markdown("**Paso 2 — Solución exacta (onda estacionaria)**")
        st.markdown("Sumando dos ondas viajeras en sentidos opuestos se obtiene:")
        st.latex(r"y(x,t) = 2A \cdot \sin(k_n x) \cdot \sin(\omega t)")
        st.caption("📌 Dos ondas que viajan en sentidos opuestos se suman y forman una onda estacionaria.")

    with col_f2:
        st.markdown("**Paso 3 — Modo n y condiciones de frontera**")
        st.markdown("Para que los extremos sean nodos (y=0), el número de onda debe ser:")
        st.latex(r"k_n = \frac{n \pi}{L} \quad \Rightarrow \quad \lambda_n = \frac{2L}{n}")
        st.markdown("La frecuencia angular y la frecuencia de oscilación:")
        st.latex(r"\omega = k_n \cdot v \qquad f_n = \frac{\omega}{2\pi} = \frac{n}{2L}\sqrt{\frac{T}{\mu}}")

        st.markdown("**Nodos y antinodos del modo n:**")
        st.latex(r"\text{Nodos: } x = \frac{j \cdot L}{n}, \quad j = 0, 1, \ldots, n")
        st.latex(r"\text{Antinodos: } x = \frac{(2j-1) \cdot L}{2n}, \quad j = 1, \ldots, n")

    st.info("""
💡 Con n = 7 se forman **7 antinodos** y **8 nodos** (incluyendo los dos extremos fijos).
El antinodo de referencia que seguimos en la simulación está en x = 2L·3/(n·4).
""")

    # =========================================================
    # BLOQUE 4 — MÉTODO NUMÉRICO
    # =========================================================
    st.markdown("---")
    st.markdown("### 🔢 Método numérico: Diferencias Finitas de 2do orden")

    st.markdown("""
En vez de usar la solución exacta para todo el tiempo, discretizo la cuerda
en **nx nodos espaciales** separados por Δx, y avanzo el tiempo en pasos Δt.

La ecuación de onda continua se reemplaza por la aproximación discreta:
""")
    st.latex(
        r"u_i^{n+1} = 2u_i^n - u_i^{n-1} + a^2 \left( u_{i+1}^n - 2u_i^n + u_{i-1}^n \right)"
    )
    st.markdown("""
donde **a = v·Δt/Δx** es el número de Courant. El esquema es **estable solo si a ≤ 1**.
Con Δx = 0,01 m y a = 0,90·Δx/v se garantiza estabilidad en todos los casos.

- **u_i^n** = desplazamiento en el nodo i en el instante n
- El superíndice indica el instante de tiempo, el subíndice la posición
- Los extremos siempre se mantienen en cero: u₀ = uₙₓ = 0 (nodos fijos)
""")

    # =========================================================
    # BLOQUE 5 — CONEXIÓN CÓDIGO-FÍSICA
    # =========================================================
    st.markdown("---")
    st.markdown("### 💻 ¿Cómo se conecta el código con la física?")
    st.markdown("""
| Concepto físico | Línea en el código |
|---|---|
| Velocidad de onda `v = √(T/μ)` | `velocidad = np.sqrt(tension / densidad_lineal)` |
| Número de onda `kₙ = nπ/L` | `k_n = n_modo * np.pi / L` |
| Frecuencia angular `ω = kₙ·v` | `omega = k_n * velocidad` |
| Número de Courant `a = v·Δt/Δx` | `a = velocidad * dt / dx` |
| Solución exacta como condición inicial | `u_prev = 2*A*sin(k_n*x)*sin(omega*0)` |
| Diferencias finitas 2do orden | `u_next[1:-1] = 2*u_curr[1:-1] - u_prev[1:-1] + a**2*(...)` |
| Nodos fijos en los extremos | `u_next[0] = 0.0` y `u_next[-1] = 0.0` |
""")
    st.caption("📌 Abrir el sidebar para señalar esas líneas exactas.")

    # =========================================================
    # PARÁMETROS DEL SISTEMA (fijos)
    # =========================================================
    L = 2.50
    tension = 150
    densidad_lineal = 8.00e-3
    amplitud = 2.00e-2
    n_modo = 7
    dx = 1.00e-2
    x_antinodo_ref = 2 * L * 3 / (n_modo * 4)
    velocidad = np.sqrt(tension / densidad_lineal)
    k_n = n_modo * np.pi / L
    omega = k_n * velocidad
    f_osc = omega / (2 * np.pi)
    T_per = 1.00 / f_osc
    dt = 0.90 * dx / velocidad
    a = velocidad * dt / dx
    t_estab = 100 * L / velocidad
    t_muestras = [t_estab + (k - 1) * T_per / 4 for k in range(1, 6)]
    T_sim = max(t_muestras[-1], t_estab + 3 * T_per)
    nx = round(L / dx) + 1
    x = np.linspace(0, L, nx)
    idx_antinodo = int(round(x_antinodo_ref / dx))
    x_antinodo_real = x[idx_antinodo]

    # =========================================================
    # BLOQUE 6 — RESULTADOS CALCULADOS
    # =========================================================
    st.markdown("---")
    st.markdown("### 📊 Magnitudes físicas calculadas")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocidad de onda v", f"{velocidad:.2f} m/s")
    col2.metric("Frecuencia f", f"{f_osc:.2f} Hz")
    col3.metric("Período T", f"{T_per:.6f} s")
    col4.metric("Número de Courant a", f"{a:.4f}",
                "✓ estable" if a <= 1 else "✗ inestable")

    st.markdown("""
| Parámetro numérico | Valor |
|---|---|
| Paso temporal Δt | """ + f"{dt:.6f} s" + """ |
| Nodos espaciales nx | """ + f"{nx}" + """ |
| Tiempo de estabilización t_estab | """ + f"{t_estab:.4f} s" + """ |
| Antinodo de referencia | x = """ + f"{x_antinodo_real:.4f} m" + """ |
""")

    if a <= 1:
        st.success(f"✅ El esquema cumple la condición de Courant (a = {a:.4f} ≤ 1) — la simulación es estable.")
    else:
        st.error(f"❌ El esquema NO cumple la condición de Courant (a = {a:.4f} > 1) — la simulación es inestable.")

    # =========================================================
    # SIMULACIÓN POR DIFERENCIAS FINITAS
    # =========================================================
    def desplazamiento_exacto(x_arr, t_val):
        return 2 * amplitud * np.sin(k_n * x_arr) * np.sin(omega * t_val)

    def velocidad_exacta(x_arr, t_val):
        return 2 * amplitud * omega * np.sin(k_n * x_arr) * np.cos(omega * t_val)

    u_prev = desplazamiento_exacto(x, 0.0)
    u_curr = u_prev + dt * velocidad_exacta(x, 0.0)
    perfiles = {}
    t_actual = dt
    instantes_pendientes = sorted(t_muestras)
    idx_muestra = 0
    tiempo_antinodo = []
    amplitud_antinodo = []

    with st.spinner("Calculando la simulación por diferencias finitas..."):
        while t_actual <= T_sim + dt:
            if idx_muestra < len(instantes_pendientes):
                t_objetivo = instantes_pendientes[idx_muestra]
                if abs(t_actual - t_objetivo) < dt / 2:
                    perfiles[t_objetivo] = u_curr.copy()
                    idx_muestra += 1
            if t_actual >= t_estab and t_actual <= t_estab + 2 * T_per + 10 * dt:
                tiempo_antinodo.append(t_actual)
                amplitud_antinodo.append(u_curr[idx_antinodo])
            u_next = np.empty(nx)
            u_next[1:-1] = (
                2 * u_curr[1:-1] - u_prev[1:-1]
                + (a**2) * (u_curr[2:] - 2 * u_curr[1:-1] + u_curr[:-2])
            )
            u_next[0] = 0.0
            u_next[-1] = 0.0
            u_prev = u_curr
            u_curr = u_next
            t_actual += dt

    COLORES = ['#1a6faf', '#c94040', '#2a9d5c', '#e07b20', '#7b52ab']
    ESTILOS = ['-', '--', '-.', ':', (0, (3, 1, 1, 1))]
    t_arr = np.array(tiempo_antinodo)
    y_arr = np.array(amplitud_antinodo)
    t_rel = t_arr - t_estab

    # =========================================================
    # GRÁFICA 1 — Perfil de la cuerda
    # =========================================================
    st.markdown("---")
    st.markdown("### 📈 Gráfica 1 — Perfil de la cuerda en estado estacionario")
    st.caption(
        "Cada curva muestra la forma de la cuerda en uno de los 5 instantes "
        "capturados (t₁ a t₅), separados por T/4. Se observan claramente los "
        "nodos (puntos que no se mueven) y los antinodos (puntos de máxima amplitud)."
    )
    fig1, ax1 = plt.subplots(figsize=(12, 5.5))
    for idx, (t_cap, perfil) in enumerate(sorted(perfiles.items())):
        k = idx + 1
        label = f"$t_{k}$ = {t_cap:.5f} s  [+{(k-1)/4:.2f}T]"
        ax1.plot(x, perfil, color=COLORES[idx], linestyle=ESTILOS[idx],
                 linewidth=1.8, label=label)
    ax1.axhline(0, color='black', linewidth=0.7)
    ax1.set_xlim(0, L)
    ax1.set_ylim(-2 * amplitud * 1.25, 2 * amplitud * 1.25)
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(L / (2 * n_modo)))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(2 * amplitud * 0.50))
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
    ax1.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.6)
    ax1.set_title("Perfil de la cuerda en estado estacionario", fontsize=11, pad=10)
    ax1.set_xlabel("Posición a lo largo de la cuerda, x (m)", fontsize=10)
    ax1.set_ylabel("Desplazamiento transversal, y (m)", fontsize=10)
    ax1.legend(
        title=f"Instantes (t_estab = {t_estab:.5f} s)",
        title_fontsize=8, fontsize=8, loc='upper right'
    )
    st.pyplot(fig1)
    plt.close(fig1)

    # =========================================================
    # GRÁFICA 2 — Perfil + antinodo marcado
    # =========================================================
    st.markdown("### 📈 Gráfica 2 — Perfil de la cuerda con antinodo de referencia")
    st.caption(
        f"Misma gráfica que la anterior pero con el antinodo de referencia marcado "
        f"(línea punteada en x = {x_antinodo_real:.3f} m). "
        "En ese punto se mide la amplitud temporal en la siguiente gráfica."
    )
    fig2, ax2 = plt.subplots(figsize=(12, 5.5))
    for idx, (t_cap, perfil) in enumerate(sorted(perfiles.items())):
        k = idx + 1
        ax2.plot(x, perfil, color=COLORES[idx], linestyle=ESTILOS[idx],
                 linewidth=1.8, label=f"$t_{k}$ [+{(k-1)/4:.2f}T]")
    ax2.axvline(x_antinodo_real, color='black', linewidth=1.4,
                linestyle='--', alpha=0.7,
                label=f"Antinodo x = {x_antinodo_real:.3f} m")
    ax2.axhline(0, color='black', linewidth=0.7)
    ax2.set_xlim(0, L)
    ax2.set_ylim(-2 * amplitud * 1.25, 2 * amplitud * 1.25)
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(L / (2 * n_modo)))
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(2 * amplitud * 0.50))
    ax2.xaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
    ax2.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.6)
    ax2.set_title("Perfil de la cuerda + antinodo de referencia", fontsize=11, pad=10)
    ax2.set_xlabel("Posición a lo largo de la cuerda, x (m)", fontsize=10)
    ax2.set_ylabel("Desplazamiento transversal, y (m)", fontsize=10)
    ax2.legend(title_fontsize=8, fontsize=8, loc='upper right')
    st.pyplot(fig2)
    plt.close(fig2)

    # =========================================================
    # GRÁFICA 3 — Amplitud en el antinodo vs tiempo
    # =========================================================
    st.markdown("### 📈 Gráfica 3 — Amplitud en el antinodo vs tiempo")
    st.caption(
        f"Evolución temporal del desplazamiento en el antinodo (x = {x_antinodo_real:.3f} m). "
        "Los puntos rojos marcan los máximos — la distancia entre ellos es el período T. "
        "Se puede verificar que coincide con el valor teórico calculado."
    )
    fig3, ax3 = plt.subplots(figsize=(12, 5.5))
    ax3.plot(t_rel, y_arr, color='#1a6faf', linewidth=1.4,
             label=f"x = {x_antinodo_real:.3f} m")
    indices_crestas, _ = find_peaks(y_arr)
    num = 1
    for i in indices_crestas:
        ax3.scatter(t_rel[i], y_arr[i], color='red', zorder=6, s=60)
        ax3.annotate(
            f"t{num} = {t_rel[i]:.8f} s",
            xy=(t_rel[i], y_arr[i]),
            xytext=(-30, -15),
            textcoords='offset points',
            fontsize=8, color='red',
        )
        num += 1
    ax3.set_title(
        f"Evolución temporal de la amplitud en el antinodo x = {x_antinodo_real:.3f} m",
        fontsize=11, pad=10
    )
    ax3.set_xlabel("Tiempo desde el estado estacionario, t − t_estab (s)", fontsize=10)
    ax3.set_ylabel("Amplitud, A (m)", fontsize=10)
    ax3.set_ylim(-2 * amplitud * 1.25, 2 * amplitud * 1.25)
    ax3.set_xlim(0, 2 * T_per)
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(T_per / 4))
    ax3.xaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
    ax3.yaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
    ax3.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.6)
    ax3.legend(fontsize=8, loc='upper right')
    st.pyplot(fig3)
    plt.close(fig3)

    # =========================================================
    # ANIMACIÓN
    # =========================================================
    st.markdown("---")
    st.markdown("### 🎻 Animación — la cuerda en los 5 instantes capturados")
    st.caption(
        "Recorre los mismos 5 instantes t₁ a t₅ (separados por T/4). "
        "El punto rojo es el antinodo de referencia: observá cómo su altura "
        "cambia entre instantes — eso es lo que mide la Gráfica 3."
    )
    perfiles_ordenados = sorted(perfiles.items())
    n_perfiles = len(perfiles_ordenados)
    x_json = json.dumps([round(float(v), 6) for v in x.tolist()])
    perfiles_json = json.dumps(
        [[round(float(v), 8) for v in perfil.tolist()] for _, perfil in perfiles_ordenados]
    )
    t_caps_json = json.dumps([round(float(t_cap), 6) for t_cap, _ in perfiles_ordenados])
    fracciones_json = json.dumps([round(idx / 4.0, 2) for idx in range(n_perfiles)])
    amplitudes_antinodo_json = json.dumps(
        [round(float(perfil[idx_antinodo]), 8) for _, perfil in perfiles_ordenados]
    )
    html_cuerda = f"""
<div style="display:flex;justify-content:center;gap:10px;margin-bottom:8px;">
    <button id="btn_prev" style="padding:6px 14px;border-radius:6px;border:none;background:#333;color:white;cursor:pointer;">⏮ Anterior</button>
    <button id="btn_play" style="padding:6px 18px;border-radius:6px;border:none;background:#1a6faf;color:white;cursor:pointer;">▶ Reproducir</button>
    <button id="btn_next" style="padding:6px 14px;border-radius:6px;border:none;background:#333;color:white;cursor:pointer;">Siguiente ⏭</button>
</div>
<canvas id="cv_cuerda" width="700" height="300"
        style="background:#0a0a1a;border-radius:10px;display:block;margin:auto;">
</canvas>
<script>
const canvas = document.getElementById("cv_cuerda");
const ctx    = canvas.getContext("2d");
const W = canvas.width, H = canvas.height;
const L_js         = {L};
const A_js         = {amplitud};
const x_arr        = {x_json};
const perfiles_arr = {perfiles_json};
const t_caps       = {t_caps_json};
const fracciones_T = {fracciones_json};
const amp_antinodo = {amplitudes_antinodo_json};
const x_anti_js   = {x_antinodo_real};
const n_perfiles   = perfiles_arr.length;
const margen_x = 50, margen_y = 40, cy = H / 2;
const PX_POR_M = (W - 2*margen_x) / L_js;
const ESCALA_Y = (H/2 - margen_y) / (2*A_js);
function xPix(xm){{ return margen_x + xm*PX_POR_M; }}
function yPix(ym){{ return cy - ym*ESCALA_Y; }}
let idx_actual = 0, reproduciendo = false, ultimo_cambio = 0;
const INTERVALO_MS = 900;
function valorEnX(perfil, xm){{
    let i = Math.round((xm/L_js)*(perfil.length-1));
    i = Math.max(0, Math.min(perfil.length-1, i));
    return perfil[i];
}}
function dibujarFrame(){{
    ctx.clearRect(0,0,W,H);
    ctx.strokeStyle="rgba(255,255,255,0.15)"; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(xPix(0),cy); ctx.lineTo(xPix(L_js),cy); ctx.stroke();
    const idx_prev=(idx_actual-1+n_perfiles)%n_perfiles;
    const p_prev=perfiles_arr[idx_prev];
    ctx.strokeStyle="rgba(255,255,255,0.18)"; ctx.lineWidth=1.5;
    ctx.beginPath();
    for(let i=0;i<x_arr.length;i++){{
        const px=xPix(x_arr[i]),py=yPix(p_prev[i]);
        if(i===0)ctx.moveTo(px,py); else ctx.lineTo(px,py);
    }}
    ctx.stroke();
    const perfil=perfiles_arr[idx_actual];
    const grad=ctx.createLinearGradient(xPix(0),0,xPix(L_js),0);
    grad.addColorStop(0,"#64dcff"); grad.addColorStop(0.5,"#ffdd55"); grad.addColorStop(1,"#64dcff");
    ctx.strokeStyle=grad; ctx.lineWidth=3;
    ctx.beginPath();
    for(let i=0;i<x_arr.length;i++){{
        const px=xPix(x_arr[i]),py=yPix(perfil[i]);
        if(i===0)ctx.moveTo(px,py); else ctx.lineTo(px,py);
    }}
    ctx.stroke();
    ctx.fillStyle="#888";
    ctx.fillRect(xPix(0)-6,cy-14,12,28);
    ctx.fillRect(xPix(L_js)-6,cy-14,12,28);
    const y_anti=valorEnX(perfil,x_anti_js);
    ctx.beginPath(); ctx.arc(xPix(x_anti_js),yPix(y_anti),8,0,2*Math.PI);
    ctx.fillStyle="#ff5a36"; ctx.fill();
    ctx.strokeStyle="white"; ctx.lineWidth=1.5; ctx.stroke();
    ctx.fillStyle="#ff5a36"; ctx.font="bold 12px Arial";
    ctx.fillText("y = "+y_anti.toFixed(5)+" m",xPix(x_anti_js)+12,yPix(y_anti)-10);
    ctx.fillStyle="rgba(0,0,0,0.65)"; ctx.fillRect(10,10,230,70);
    ctx.strokeStyle="rgba(255,255,255,0.25)"; ctx.strokeRect(10,10,230,70);
    ctx.fillStyle="white"; ctx.font="bold 13px Arial";
    ctx.fillText("t"+(idx_actual+1)+"  =  "+t_caps[idx_actual].toFixed(5)+" s",20,30);
    ctx.fillStyle="#aef"; ctx.font="12px Arial";
    ctx.fillText("Desfase: +"+fracciones_T[idx_actual].toFixed(2)+" T",20,48);
    ctx.fillStyle="#ffa";
    ctx.fillText("Amplitud antinodo: "+amp_antinodo[idx_actual].toFixed(5)+" m",20,65);
    const cx0=W-140;
    for(let i=0;i<n_perfiles;i++){{
        const px=cx0+i*22;
        ctx.beginPath(); ctx.arc(px,25,6,0,2*Math.PI);
        ctx.fillStyle=(i===idx_actual)?"#ff5a36":"rgba(255,255,255,0.3)"; ctx.fill();
        ctx.fillStyle="white"; ctx.font="9px Arial";
        ctx.fillText("t"+(i+1),px-6,42);
    }}
}}
function avanzar(){{ idx_actual=(idx_actual+1)%n_perfiles; dibujarFrame(); }}
function retroceder(){{ idx_actual=(idx_actual-1+n_perfiles)%n_perfiles; dibujarFrame(); }}
document.getElementById("btn_next").addEventListener("click",()=>{{ reproduciendo=false; document.getElementById("btn_play").innerText="▶ Reproducir"; avanzar(); }});
document.getElementById("btn_prev").addEventListener("click",()=>{{ reproduciendo=false; document.getElementById("btn_play").innerText="▶ Reproducir"; retroceder(); }});
document.getElementById("btn_play").addEventListener("click",()=>{{ reproduciendo=!reproduciendo; document.getElementById("btn_play").innerText=reproduciendo?"⏸ Pausar":"▶ Reproducir"; }});
function loop(ts){{ if(reproduciendo&&ts-ultimo_cambio>INTERVALO_MS){{ avanzar(); ultimo_cambio=ts; }} requestAnimationFrame(loop); }}
dibujarFrame(); requestAnimationFrame(loop);
</script>
"""
    components.html(html_cuerda, height=370)

    # =========================================================
    # EXPLORADOR CONCEPTUAL DEL MODO n
    # =========================================================
    st.markdown("---")
    st.markdown("### 🧠 Explorador conceptual: ¿qué hace el modo n?")
    st.caption(
        f"Cambiá el modo n para ver cómo aparecen los nodos y antinodos. "
        f"Los resultados del informe siempre usan n = {n_modo}."
    )
    n_conceptual = st.slider("Modo n de prueba", min_value=1, max_value=10, value=n_modo)
    fig_c, ax_c = plt.subplots(figsize=(12, 3.2))
    x_fino = np.linspace(0, L, 400)
    y_fino = np.sin(n_conceptual * np.pi * x_fino / L)
    ax_c.plot(x_fino, y_fino, color="#1a6faf", linewidth=2.5)
    ax_c.axhline(0, color="black", linewidth=0.7)
    nodos_c = [j * L / n_conceptual for j in range(0, n_conceptual + 1)]
    antinodos_c = [(2*j - 1) * L / (2*n_conceptual) for j in range(1, n_conceptual + 1)]
    ax_c.scatter(nodos_c, [0]*len(nodos_c), color="#888", s=60, zorder=5, label="Nodos (fijos)")
    ax_c.scatter(antinodos_c,
                 [np.sin(n_conceptual * np.pi * xv / L) for xv in antinodos_c],
                 color="#ff5a36", s=60, zorder=5, label="Antinodos (máxima oscilación)")
    ax_c.set_xlim(0, L)
    ax_c.set_ylim(-1.3, 1.3)
    ax_c.set_xlabel("Posición x (m)")
    ax_c.set_title(
        f"Modo n = {n_conceptual}  →  {n_conceptual} antinodos, {n_conceptual + 1} nodos",
        fontsize=11
    )
    ax_c.legend(loc="upper right", fontsize=8)
    ax_c.grid(alpha=0.3)
    st.pyplot(fig_c)
    plt.close(fig_c)

    # =========================================================
    # BLOQUE 7 — CONCLUSIONES
    # =========================================================
    st.markdown("---")
    st.markdown("### ✅ Conclusiones")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.success(f"""
**¿Se cumplió el objetivo?**
Sí. Se simuló correctamente la onda estacionaria de modo n = {n_modo}
usando diferencias finitas de 2do orden, con número de Courant
a = {a:.4f} (≤ 1 → estabilidad garantizada).
Los 5 perfiles capturados muestran la oscilación completa de la cuerda
en los instantes t₁ a t₅ separados por T/4.
""")
        st.info(f"""
**¿Por qué diferencias finitas y no la fórmula exacta?**
La solución analítica y = 2A·sin(kₙx)·sin(ωt) solo vale
para un modo puro y condiciones ideales. Las diferencias finitas
permiten simular casos más complejos (múltiples modos, condiciones
de frontera arbitrarias) que no tienen solución cerrada.
""")
    with col_c2:
        st.warning(f"""
**Limitación del método**
Si el número de Courant supera 1 (a > 1), el esquema se vuelve
inestable y los valores numéricos crecen sin control.
Por eso se elige Δt = 0,90·Δx/v (en vez de el límite exacto),
dejando un margen de seguridad del 10%.
""")
        st.info(f"""
**Ventaja computacional**
Con Δx = {dx} m se usan {nx} nodos espaciales.
El método avanza paso a paso en el tiempo y captura exactamente
los instantes de muestreo t_k = t_estab + (k-1)·T/4,
reproduciendo fielmente la física de la onda estacionaria.
""")
