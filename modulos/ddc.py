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
    # PARÁMETROS DEL SISTEMA (sin cambios respecto al original)
    # =========================================================
    L = 2.50
    tension = 150
    densidad_lineal = 8.00e-3
    amplitud = 2.00e-2
    n_modo = 7
    dx = 1.00e-2

    # Antinodo de referencia
    x_antinodo_ref = 2 * L * 3 / (n_modo * 4)

    # MAGNITUDES DERIVADAS
    velocidad = np.sqrt(tension / densidad_lineal)
    k_n = n_modo * np.pi / L
    omega = k_n * velocidad
    f_osc = omega / (2 * np.pi)
    T_per = 1.00 / f_osc

    # MALLA ESPACIAL Y TEMPORAL
    dt = 0.90 * dx / velocidad
    # Número de Courant
    a = velocidad * dt / dx
    # Tiempo de estabilización: la onda recorre 100 veces la longitud de la cuerda
    t_estab = 100 * L / velocidad
    # Los 5 instantes de muestreo según la fórmula:
    # t_k = t_estab + (k-1) · T/4   para k = 1,2,3,4,5
    t_muestras = [t_estab + (k - 1) * T_per / 4 for k in range(1, 6)]
    # Tiempo total de simulación
    T_sim = max(t_muestras[-1], t_estab + 3 * T_per)

    nx = round(L / dx) + 1
    x = np.linspace(0, L, nx)
    idx_antinodo = int(round(x_antinodo_ref / dx))
    x_antinodo_real = x[idx_antinodo]

    def desplazamiento_exacto(x_arr, t_val):
        return 2 * amplitud * np.sin(k_n * x_arr) * np.sin(omega * t_val)

    def velocidad_exacta(x_arr, t_val):
        return 2 * amplitud * omega * np.sin(k_n * x_arr) * np.cos(omega * t_val)

    # Condiciones iniciales
    u_prev = desplazamiento_exacto(x, 0.0)               # nivel n = 0  (t = 0)
    u_curr = u_prev + dt * velocidad_exacta(x, 0.0)      # nivel n = 1  (t = Δt)

    perfiles = {}
    t_actual = dt
    instantes_pendientes = sorted(t_muestras)
    idx_muestra = 0
    tiempo_antinodo = []
    amplitud_antinodo = []

    # =========================================================
    # SIMULACIÓN POR DIFERENCIAS FINITAS (idéntica al original)
    # =========================================================
    with st.spinner("Calculando la simulación por diferencias finitas..."):
        while t_actual <= T_sim + dt:
            # Captura de perfiles en los instantes t_k
            if idx_muestra < len(instantes_pendientes):
                t_objetivo = instantes_pendientes[idx_muestra]
                if abs(t_actual - t_objetivo) < dt / 2:
                    perfiles[t_objetivo] = u_curr.copy()
                    idx_muestra += 1

            # Registro del antinodo
            if t_actual >= t_estab and t_actual <= t_estab + 2 * T_per + 10 * dt:
                tiempo_antinodo.append(t_actual)
                amplitud_antinodo.append(u_curr[idx_antinodo])

            # Diferencias finitas de 2do orden
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
    # CONDICIÓN DE ESTABILIDAD Y RESULTADOS GENERALES
    # =========================================================
    st.markdown("### Parámetros calculados")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocidad de onda v", f"{velocidad:.2f} m/s")
    col2.metric("Frecuencia f", f"{f_osc:.2f} Hz")
    col3.metric("Periodo T", f"{T_per:.6f} s")
    col4.metric(
        "Número de Courant (a)",
        f"{a:.4f}",
        "✓ estable" if a <= 1 else "✗ inestable"
    )

    with st.expander("📋 Ver detalles numéricos de la simulación"):
        st.write(f"**Paso de tiempo (Δt):** {dt:.6f} s")
        st.write(f"**Nodos espaciales (nx):** {nx}")
        st.write(f"**Tiempo de estabilización:** {t_estab:.4f} s")
        st.write(f"**Antinodo de referencia:** x = {x_antinodo_real:.4f} m")
        st.write(f"**Perfiles capturados:** {len(perfiles)}")
        if a <= 1:
            st.success("El esquema cumple la condición de estabilidad de Courant (a ≤ 1).")
        else:
            st.error("El esquema NO cumple la condición de estabilidad de Courant (a > 1).")

    # =========================================================
    # ¿QUÉ ES UN NODO Y UN ANTINODO? (explicación rápida)
    # =========================================================
    with st.expander("❓ ¿Qué es un nodo y un antinodo?"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                "**🔵 Nodo**\n\n"
                "Punto de la cuerda que **nunca se mueve**. "
                "Los extremos siempre son nodos porque la cuerda "
                "está fija ahí. Con el modo n se forman **n+1 nodos**."
            )
        with col_b:
            st.markdown(
                "**🔴 Antinodo**\n\n"
                "Punto que se mueve con la **máxima amplitud posible** "
                "(sube y baja entre $-2A$ y $+2A$). Con el modo n se "
                "forman **n antinodos**."
            )
        st.caption(
            f"En nuestro sistema, n = {n_modo} → {n_modo} antinodos y {n_modo + 1} nodos "
            f"(incluyendo los dos extremos fijos)."
        )

    # =========================================================
    # FUNCIONES DE DIBUJO (idénticas en lógica al original,
    # solo adaptadas para recibir el eje 'ax' como parámetro)
    # =========================================================
    def dibujar_perfil(ax, mostrar_antinodo=False):
        for idx, (t_cap, perfil) in enumerate(sorted(perfiles.items())):
            k = idx + 1
            label = f"$t_{k}$ = {t_cap:.5f} s  [+{(k-1)/4:.2f}T]"
            ax.plot(x, perfil,
                    color=COLORES[idx], linestyle=ESTILOS[idx],
                    linewidth=1.8, label=label)

        if mostrar_antinodo:
            ax.axvline(x_antinodo_real,
                       color='black', linewidth=1.4, linestyle='--', alpha=0.7,
                       label=f"Antinodo  $x$ = {x_antinodo_real:.3f} m")

        ax.set_title("Perfil de la cuerda en estado estacionario",
                     fontsize=11, pad=10)
        ax.set_xlabel("Posición a lo largo de la cuerda,  $x$  (m)", fontsize=10)
        ax.set_ylabel("Desplazamiento transversal,  $y$  (m)", fontsize=10)
        ax.axhline(0, color='black', linewidth=0.7)
        ax.set_xlim(0, L)
        ax.set_ylim(-2 * amplitud * 1.25, 2 * amplitud * 1.25)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(L / (2 * n_modo)))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2 * amplitud * 0.50))
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(4))
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(4))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
        ax.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.6)
        ax.grid(which='minor', linestyle=':', linewidth=0.3, alpha=0.4)
        ax.legend(
            title=f"Instantes de tiempo:\n$t_{{\\rm estab}}$ = {t_estab:.5f} s",
            title_fontsize=8, fontsize=8,
            loc='upper right', framealpha=0.92, edgecolor='#cccccc',
        )

    def dibujar_amplitud(ax):
        ax.plot(t_rel, y_arr, color='#1a6faf', linewidth=1.4,
                label=f"$x$ = {x_antinodo_real:.3f} m")

        indices_crestas, _ = find_peaks(y_arr)
        num = 1
        for i in indices_crestas:
            ax.scatter(t_rel[i], y_arr[i], color='red', zorder=6, s=60)
            ax.annotate(
                f"t{num} = {t_rel[i]:.8f} s",
                xy=(t_rel[i], y_arr[i]),
                xytext=(-30, -15),
                textcoords='offset points',
                fontsize=8,
                color='red',
            )
            num += 1

        ax.set_title(
            f"Evolución temporal de la amplitud en el antinodo $x$ = {x_antinodo_real:.3f} m",
            fontsize=11, pad=10
        )
        ax.set_xlabel(
            "Tiempo desde el estado estacionario,  $t - t_{\\rm estab}$  (s)",
            fontsize=10
        )
        ax.set_ylabel("Amplitud,  $A$  (m)", fontsize=10)
        ax.set_ylim(-2 * amplitud * 1.25, 2 * amplitud * 1.25)
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2 * amplitud * 0.50))
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(4))
        ax.set_xlim(0, 2 * T_per)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(T_per / 4))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(4))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(tres_cifras_significativas))
        ax.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.6)
        ax.grid(which='minor', linestyle=':', linewidth=0.3, alpha=0.4)
        ax.legend(
            title=f"x = {x_antinodo_real:.3f} m",
            title_fontsize=8, fontsize=8,
            loc='upper right', framealpha=0.92, edgecolor='#cccccc',
        )

    # =========================================================
    # SELECTOR DE VISTA (reemplaza los RadioButtons de matplotlib)
    # =========================================================
    st.markdown("### Visualización de resultados")
    vista = st.radio(
        "Selecciona la vista:",
        ["Perfil de onda", "Perfil + antinodo", "Amplitud vs tiempo"],
        horizontal=True
    )

    fig, ax = plt.subplots(figsize=(12, 5.5))
    if vista == "Perfil de onda":
        dibujar_perfil(ax, mostrar_antinodo=False)
    elif vista == "Perfil + antinodo":
        dibujar_perfil(ax, mostrar_antinodo=True)
    else:
        dibujar_amplitud(ax)
    st.pyplot(fig)
    plt.close(fig)

    # =========================================================
    # ANIMACIÓN: recorrido real por t1, t2, t3, t4, t5
    # Usa EXACTAMENTE los perfiles calculados por diferencias
    # finitas (los mismos que en la gráfica "Perfil de onda"),
    # no una fórmula aproximada. Solo se anima la transición.
    # =========================================================
    st.markdown("### 🎻 Animación: la cuerda en los 5 instantes capturados")
    st.caption(
        "Recorre los mismos 5 instantes $t_1$ a $t_5$ (separados por T/4) que "
        "ya hay en la gráfica de arriba, pero en secuencia animada. El punto "
        "rojo es el antinodo de referencia: nos fijamos cómo su altura cambia entre "
        "cada instante — eso es lo que se mide en la gráfica 'Amplitud vs tiempo'."
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

const L_js          = {L};
const A_js          = {amplitud};
const x_arr         = {x_json};
const perfiles_arr  = {perfiles_json};
const t_caps        = {t_caps_json};
const fracciones_T  = {fracciones_json};
const amp_antinodo  = {amplitudes_antinodo_json};
const x_antinodo_js = {x_antinodo_real};
const n_perfiles    = perfiles_arr.length;

const margen_x = 50;
const margen_y = 40;
const cy = H / 2;
const PX_POR_M = (W - 2 * margen_x) / L_js;
const ESCALA_Y = (H / 2 - margen_y) / (2 * A_js);

function xPix(xm) {{ return margen_x + xm * PX_POR_M; }}
function yPix(ym) {{ return cy - ym * ESCALA_Y; }}

let idx_actual = 0;
let reproduciendo = false;
let ultimo_cambio = 0;
const INTERVALO_MS = 900;

function valorEnX(perfil, xm) {{
    // Interpolación simple para hallar y en x = xm dentro del arreglo discreto
    let i = Math.round((xm / L_js) * (perfil.length - 1));
    i = Math.max(0, Math.min(perfil.length - 1, i));
    return perfil[i];
}}

function dibujarFrame() {{
    ctx.clearRect(0, 0, W, H);

    // Línea de referencia (cuerda en reposo)
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(xPix(0), cy);
    ctx.lineTo(xPix(L_js), cy);
    ctx.stroke();

    // Perfil anterior (fantasma, para notar el movimiento)
    const idx_prev = (idx_actual - 1 + n_perfiles) % n_perfiles;
    const perfil_prev = perfiles_arr[idx_prev];
    ctx.strokeStyle = "rgba(255,255,255,0.18)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let i = 0; i < x_arr.length; i++) {{
        const px = xPix(x_arr[i]), py = yPix(perfil_prev[i]);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }}
    ctx.stroke();

    // Perfil actual
    const perfil = perfiles_arr[idx_actual];
    const grad = ctx.createLinearGradient(xPix(0), 0, xPix(L_js), 0);
    grad.addColorStop(0, "#64dcff");
    grad.addColorStop(0.5, "#ffdd55");
    grad.addColorStop(1, "#64dcff");
    ctx.strokeStyle = grad;
    ctx.lineWidth = 3;
    ctx.beginPath();
    for (let i = 0; i < x_arr.length; i++) {{
        const px = xPix(x_arr[i]), py = yPix(perfil[i]);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }}
    ctx.stroke();

    // Soportes fijos
    ctx.fillStyle = "#888";
    ctx.fillRect(xPix(0) - 6, cy - 14, 12, 28);
    ctx.fillRect(xPix(L_js) - 6, cy - 14, 12, 28);

    // Antinodo de referencia resaltado
    const y_antinodo = valorEnX(perfil, x_antinodo_js);
    ctx.beginPath();
    ctx.arc(xPix(x_antinodo_js), yPix(y_antinodo), 8, 0, 2 * Math.PI);
    ctx.fillStyle = "#ff5a36";
    ctx.fill();
    ctx.strokeStyle = "white";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.fillStyle = "#ff5a36";
    ctx.font = "bold 12px Arial";
    ctx.fillText(
        "y = " + y_antinodo.toFixed(5) + " m",
        xPix(x_antinodo_js) + 12,
        yPix(y_antinodo) - 10
    );

    // Panel de información del instante actual
    ctx.fillStyle = "rgba(0,0,0,0.65)";
    ctx.fillRect(10, 10, 230, 70);
    ctx.strokeStyle = "rgba(255,255,255,0.25)";
    ctx.strokeRect(10, 10, 230, 70);
    ctx.fillStyle = "white";
    ctx.font = "bold 13px Arial";
    ctx.fillText("t" + (idx_actual + 1) + "  =  " + t_caps[idx_actual].toFixed(5) + " s", 20, 30);
    ctx.fillStyle = "#aef";
    ctx.font = "12px Arial";
    ctx.fillText("Desfase: +" + fracciones_T[idx_actual].toFixed(2) + " T", 20, 48);
    ctx.fillStyle = "#ffa";
    ctx.fillText("Amplitud antinodo: " + amp_antinodo[idx_actual].toFixed(5) + " m", 20, 65);

    // Indicador de progreso (puntos t1..t5)
    const cx0 = W - 140;
    for (let i = 0; i < n_perfiles; i++) {{
        const px = cx0 + i * 22;
        ctx.beginPath();
        ctx.arc(px, 25, 6, 0, 2 * Math.PI);
        ctx.fillStyle = (i === idx_actual) ? "#ff5a36" : "rgba(255,255,255,0.3)";
        ctx.fill();
        ctx.fillStyle = "white";
        ctx.font = "9px Arial";
        ctx.fillText("t" + (i + 1), px - 6, 42);
    }}
}}

function avanzar() {{
    idx_actual = (idx_actual + 1) % n_perfiles;
    dibujarFrame();
}}
function retroceder() {{
    idx_actual = (idx_actual - 1 + n_perfiles) % n_perfiles;
    dibujarFrame();
}}

document.getElementById("btn_next").addEventListener("click", () => {{
    reproduciendo = false;
    document.getElementById("btn_play").innerText = "▶ Reproducir";
    avanzar();
}});
document.getElementById("btn_prev").addEventListener("click", () => {{
    reproduciendo = false;
    document.getElementById("btn_play").innerText = "▶ Reproducir";
    retroceder();
}});
document.getElementById("btn_play").addEventListener("click", () => {{
    reproduciendo = !reproduciendo;
    document.getElementById("btn_play").innerText = reproduciendo ? "⏸ Pausar" : "▶ Reproducir";
}});

function loop(timestamp) {{
    if (reproduciendo && timestamp - ultimo_cambio > INTERVALO_MS) {{
        avanzar();
        ultimo_cambio = timestamp;
    }}
    requestAnimationFrame(loop);
}}

dibujarFrame();
requestAnimationFrame(loop);
</script>
"""
    components.html(html_cuerda, height=370)

    # =========================================================
    # SECCIÓN EDUCATIVA: explorador conceptual del modo n
    # (Puramente ilustrativo — NO forma parte de los resultados
    # numéricos del informe. Solo ayuda a entender qué hace "n".)
    # =========================================================
    st.markdown("---")
    st.markdown("### 🧠 Explorador conceptual: ¿qué hace el modo n?")
    st.caption(
        "Esta sección es solo educativa: cambia un número n de prueba y "
        "cómo cambian los nodos y antinodos. **No afecta los resultados del "
        f"informe**, que siempre usa n = {n_modo}."
    )

    n_conceptual = st.slider("Modo n de prueba", min_value=1, max_value=10, value=n_modo)

    fig_concepto, ax_c = plt.subplots(figsize=(12, 3.2))
    x_fino = np.linspace(0, L, 400)
    y_fino = np.sin(n_conceptual * np.pi * x_fino / L)
    ax_c.plot(x_fino, y_fino, color="#1a6faf", linewidth=2.5)
    ax_c.axhline(0, color="black", linewidth=0.7)

    nodos_c = [j * L / n_conceptual for j in range(0, n_conceptual + 1)]
    antinodos_c = [(2 * j - 1) * L / (2 * n_conceptual) for j in range(1, n_conceptual + 1)]
    ax_c.scatter(nodos_c, [0] * len(nodos_c), color="#888888", s=60, zorder=5, label="Nodos (fijos)")
    ax_c.scatter(
        antinodos_c,
        [np.sin(n_conceptual * np.pi * xv / L) for xv in antinodos_c],
        color="#ff5a36", s=60, zorder=5, label="Antinodos (máxima oscilación)"
    )
    ax_c.set_xlim(0, L)
    ax_c.set_ylim(-1.3, 1.3)
    ax_c.set_xlabel("Posición x (m)")
    ax_c.set_title(f"Modo n = {n_conceptual}  →  {n_conceptual} antinodos, {n_conceptual + 1} nodos", fontsize=11)
    ax_c.legend(loc="upper right", fontsize=8)
    ax_c.grid(alpha=0.3)
    st.pyplot(fig_concepto)
    plt.close(fig_concepto)

    # =========================================================
    # SECCIÓN EDUCATIVA: cómo influyen los parámetros físicos
    # =========================================================
    with st.expander("⚙️ ¿Cómo influye cada parámetro en la velocidad y frecuencia?"):
        col_t, col_d, col_l = st.columns(3)
        with col_t:
            st.markdown("**Tensión (T)**")
            st.markdown(
                "Cuerda más tensa → onda **más rápida** y **más aguda**.\n\n"
                r"$v = \sqrt{T/\mu}$"
            )
        with col_d:
            st.markdown("**Densidad lineal (μ)**")
            st.markdown(
                "Cuerda más gruesa/pesada → onda **más lenta** y **más grave**.\n\n"
                r"$v = \sqrt{T/\mu}$"
            )
        with col_l:
            st.markdown("**Longitud (L) y modo (n)**")
            st.markdown(
                "Cuerda más larga, o modo más alto → **más nodos y antinodos**, "
                "y la frecuencia sube.\n\n"
                r"$f_n = \dfrac{n}{2L}\sqrt{T/\mu}$"
            )
        st.caption(
            f"Con tus valores actuales: v = {velocidad:.2f} m/s, f = {f_osc:.2f} Hz, "
            f"T = {T_per:.6f} s."
        )