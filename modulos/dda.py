import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

"""
Instalación de librerías necesarias (ejecutar en cmd):
    pip install matplotlib
    pip install numpy
    pip install streamlit
"""

# ------------------------------------------------------------------------------
# Constante gravitacional
# ------------------------------------------------------------------------------
g = 9.81  # m/s²

# ------------------------------------------------------------------------------
# Defino el integrando de la fuerza total sobre el dique.
# Este término representa la fuerza diferencial por unidad de altura:
#   f(y) = 80·g·L·(0.25·y³ - y + 10)·(H - y)
# donde (0.25·y³ - y + 10) modela la densidad variable del fluido
# y (H - y) es la presión hidrostática a la profundidad (H - y).
# ------------------------------------------------------------------------------
def integrando(y, L, H):
    return 80.0 * g * L * (0.250 * y**3 - y + 10.0) * (H - y)

# ------------------------------------------------------------------------------
# Calculo la fuerza total usando la Regla del Trapecio.
# Divido el intervalo [0, H] en n subintervalos de ancho h = H/n.
# En cada subintervalo aproximo el área bajo f(y) como un trapecio:
#   Área_i ≈ (f(y_i) + f(y_{i+1})) / 2 · h
# La suma de todas esas áreas da la integral numérica.
# Los extremos se cuentan una vez, los puntos intermedios se duplican.
# ------------------------------------------------------------------------------
def fuerza_trapecio(L, H, n):
    a = 0.0        # límite inferior: base del dique
    b = H          # límite superior: superficie del fluido
    h = (b - a) / n
    suma = integrando(a, L, H) + integrando(b, L, H)
    for i in range(1, n):
        yi = a + i * h
        suma += 2.0 * integrando(yi, L, H)
    return (h / 2.0) * suma

# ------------------------------------------------------------------------------
# Solución analítica exacta (teórica) de la integral:
#   F_total = 80·g·L·(0.0125·H³ - H/6 + 5)·H²
# Esta fórmula se obtiene integrando f(y) de 0 a H de forma exacta.
# La uso para comparar con el resultado numérico y calcular el error.
# ------------------------------------------------------------------------------
def fuerza_teorica(L, H):
    return 80.0 * g * L * (0.0125 * H**3 - H / 6.0 + 5.0) * H**2

# ------------------------------------------------------------------------------
# Calculo el porcentaje de error entre la aproximación y la solución exacta.
# Mide qué tan buena es mi aproximación numérica.
# ------------------------------------------------------------------------------
def porcentaje_error(valor_aprox, valor_teorico):
    return abs((valor_teorico - valor_aprox) / valor_teorico) * 100.0


def mostrar():

    # ==========================================================================
    # DRAWER LATERAL
    # Muestra únicamente el código matemático principal utilizado en este módulo.
    # Durante la exposición permite señalar exactamente dónde se implementa
    # cada una de las fórmulas explicadas.
    # ==========================================================================
    codigo_matematico = '''
# CONSTANTE
g = 9.81  # m/s²

# INTEGRANDO: fuerza diferencial por unidad de altura
def integrando(y, L, H):
    return 80.0 * g * L * (0.250 * y**3 - y + 10.0) * (H - y)

# REGLA DEL TRAPECIO: suma de áreas trapezoidales
def fuerza_trapecio(L, H, n):
    a = 0.0
    b = H
    h = (b - a) / n

    suma = integrando(a, L, H) + integrando(b, L, H)

    for i in range(1, n):
        yi = a + i * h
        suma += 2.0 * integrando(yi, L, H)

    return (h / 2.0) * suma

# SOLUCIÓN TEÓRICA EXACTA
def fuerza_teorica(L, H):
    return 80.0 * g * L * (0.0125 * H**3 - H / 6.0 + 5.0) * H**2

# PORCENTAJE DE ERROR
def porcentaje_error(valor_aprox, valor_teorico):
    return abs((valor_teorico - valor_aprox) / valor_teorico) * 100.0
'''

    drawer_html = f"""
    <style>
    #drawer-wrapper {{
        position: fixed;
        top: 80px;
        left: 0;
        z-index: 9999;
        display: flex;
        align-items: flex-start;
    }}
    #drawer-panel {{
        width: 0px;
        overflow: hidden;
        transition: width 0.35s ease;
        background: #1e1e2e;
        border-radius: 0 12px 12px 0;
        box-shadow: 4px 0 18px rgba(0,0,0,0.5);
    }}
    #drawer-panel.open {{
        width: 440px;
    }}
    #drawer-inner {{
        width: 440px;
        padding: 16px;
        color: #cdd6f4;
        font-family: monospace;
        font-size: 12.5px;
        line-height: 1.6;
        white-space: pre-wrap;
        max-height: 80vh;
        overflow-y: auto;
    }}
    #drawer-btn {{
        width: 32px;
        min-height: 90px;
        background: #313244;
        color: #cdd6f4;
        border: none;
        border-radius: 0 8px 8px 0;
        cursor: pointer;
        font-size: 13px;
        writing-mode: vertical-rl;
        padding: 10px 6px;
        box-shadow: 4px 0 10px rgba(0,0,0,0.4);
        transition: background 0.2s;
        letter-spacing: 1px;
    }}
    #drawer-btn:hover {{ background: #45475a; }}
    #drawer-title {{
        color: #89b4fa;
        font-size: 13px;
        font-weight: bold;
        margin-bottom: 12px;
        border-bottom: 1px solid #45475a;
        padding-bottom: 6px;
    }}
    </style>

    <div id="drawer-wrapper">
        <div id="drawer-panel">
            <div id="drawer-inner">
                <div id="drawer-title">📐 Código matemático — dda.py</div>
<pre>{codigo_matematico}</pre>
            </div>
        </div>
        <button id="drawer-btn" onclick="toggleDrawer()">📄 VER CÓDIGO</button>
    </div>

    <script>
    function toggleDrawer() {{
        const panel = document.getElementById('drawer-panel');
        const btn   = document.getElementById('drawer-btn');
        panel.classList.toggle('open');
        btn.textContent = panel.classList.contains('open') ? '✖ CERRAR' : '📄 VER CÓDIGO';
    }}
    </script>
    """

    components.html(drawer_html, height=500)

    # ==========================================================================
    # BLOQUE 1 — INTRODUCCIÓN Y CONTEXTO
    # ==========================================================================
    st.markdown("# 📐 DDA — Fuerza de un fluido sobre un dique")
    st.markdown("---")

    st.markdown("""
### 🏗️ ¿De qué trata ?

Un **dique** es una estructura que contiene un fluido (agua, lodo, químicos).
Para diseñarlo correctamente necesito saber **con qué fuerza total** el fluido
empuja sobre esa pared — si subestimo esa fuerza, el dique falla.

El problema es que **la presión no es constante**: cuanto más abajo, mayor
presión. Eso significa que no puedo simplemente multiplicar presión × área.
Necesito **integrar** la presión a lo largo de toda la altura.
""")

    # ==========================================================================
    # BLOQUE 2 — FUNDAMENTO FÍSICO Y MODELO MATEMÁTICO
    # ==========================================================================
    st.markdown("---")
    st.markdown("### 📐 ¿De dónde salen las fórmulas?")

    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        st.markdown("""
**Paso 1 — Presión hidrostática**

La presión a una profundidad `(H - y)` es:
""")
        st.latex(r"P(y) = \rho(y) \cdot g \cdot (H - y)")
        st.markdown("""
En este fluido la densidad **no es constante** — varía con la altura `y`
según la función de densidad del enunciado:
""")
        st.latex(r"\rho(y) = 80 \cdot (0{,}25y^3 - y + 10)")

    with col_f2:
        st.markdown("""
**Paso 2 — Fuerza diferencial**

La fuerza sobre una franja infinitesimal de ancho `dy` y largo `L` es:
""")
        st.latex(r"dF = P(y) \cdot L \cdot dy")
        st.markdown("""
**Paso 3 — Fuerza total (integral)**

Sumo todos los aportes de `y = 0` hasta `y = H`:
""")
        st.latex(r"F_{total} = \int_0^H 80 \cdot g \cdot L \cdot (0{,}25y^3 - y + 10) \cdot (H-y) \; dy")

    st.markdown("**Solución analítica exacta** (integrando directamente):")
    st.latex(r"F_{total} = 80 \cdot g \cdot L \cdot \left(0{,}0125 H^3 - \frac{H}{6} + 5\right) \cdot H^2")

    st.info("""
💡 **¿Por qué método numérico si existe solución exacta?**
Porque en la práctica la función de densidad del fluido puede ser más
compleja y no tener solución analítica. La Regla del Trapecio permite
resolver cualquier caso sin importar qué tan complicada sea ρ(y).
""")

    # ==========================================================================
    # BLOQUE 3 — MÉTODO NUMÉRICO: REGLA DEL TRAPECIO
    # ==========================================================================
    st.markdown("---")
    st.markdown("### 🔢 Método numérico: Regla del Trapecio")

    st.markdown("""
En vez de integrar exactamente, **divido el intervalo [0, H] en n pedazos**
iguales de ancho `h = H/n` y en cada uno aproximo el área bajo la curva
como un trapecio:
""")
    st.latex(r"\int_0^H f(y)\,dy \;\approx\; \frac{h}{2}\left[f(y_0) + 2f(y_1) + 2f(y_2) + \cdots + 2f(y_{n-1}) + f(y_n)\right]")

    st.markdown("""
- Los **extremos** (y₀ e y_n) se cuentan **una vez**.
- Los **puntos intermedios** se cuentan **dos veces** (peso doble).
- Cuanto mayor es `n`, más delgados son los trapecios → menor error.
""")

    st.markdown("---")
    st.markdown("### 💻 ¿Cómo se conecta el código con la física?")
    st.markdown("""
| Concepto físico | Función en el código |
|---|---|
| Fuerza diferencial `dF = ρ(y)·g·(H-y)·L·dy` | `integrando(y, L, H)` |
| Suma de trapecios `Σ (f(yᵢ)+f(yᵢ₊₁))/2 · h` | `fuerza_trapecio(L, H, n)` -> bucle `for` |
| Solución analítica exacta | `fuerza_teorica(L, H)` |
| Validación numérica | `porcentaje_error(F_trap, F_teo)` |
""")
    st.caption("📌 Abrir el drawer lateral para señalar exactamente esas líneas en el código.")
    # ==========================================================================
    # PARÁMETROS INTERACTIVOS
    # ==========================================================================
    st.markdown("---")
    st.markdown("### ⚙️ Parámetros de la simulación")
    st.caption("Modificá los sliders y observá cómo cambian los resultados en tiempo real.")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        longitud = st.slider(
            "L — Longitud del dique (m)",
            min_value=1.50, max_value=3.50, value=2.00, step=0.10,
            help="Largo del dique en la dirección perpendicular al flujo"
        )
        altura = st.slider(
            "H — Altura del fluido (m)",
            min_value=1.00, max_value=4.80, value=3.00, step=0.10,
            help="Altura total del fluido contenido"
        )
    with col_p2:
        n = st.slider(
            "n — Número de trapecios",
            min_value=1, max_value=1000, value=6,
            help="Más trapecios = mayor precisión numérica"
        )
        trapecios_visibles = st.slider(
            "Trapecios visibles en la gráfica",
            min_value=1, max_value=n, value=min(6, n), step=1,
            help="Cuántos trapecios se colorean en la gráfica del integrando"
        )

    # ==========================================================================
    # CÁLCULOS
    # ==========================================================================
    F_trap = fuerza_trapecio(longitud, altura, n)
    F_teo  = fuerza_teorica(longitud, altura)
    error  = porcentaje_error(F_trap, F_teo)

    st.markdown("---")
    st.markdown("### 📊 Resultados")
    col1, col2, col3 = st.columns(3)
    col1.metric("F trapecio (N)", f"{F_trap:,.2f}")
    col2.metric("F teórica (N)",  f"{F_teo:,.2f}")
    col3.metric("Error (%)",      f"{error:.4f}")

    if error <= 2.0:
        st.success(f"✅ Con n={n} trapecios el error es {error:.4f}% — dentro del límite del 2%.")
    else:
        st.warning(f"⚠️ Con n={n} trapecios el error es {error:.4f}% — supera el 2%. Aumentá n.")

    # ==========================================================================
    # GRÁFICAS
    # ==========================================================================
    st.markdown("---")
    st.markdown("### 📈 Gráfica 1 — Fuerza total vs altura H")
    st.caption(
        "Comparo la curva del método numérico (trapecio) con la solución teórica exacta. "
        "Las áreas amarillas son los trapecios que el método usa para aproximar la integral."
    )

    H_vals       = np.linspace(1.00, 4.80, 200)
    F_trap_vals  = np.array([fuerza_trapecio(longitud, hv, n) for hv in H_vals])
    F_teo_vals   = np.array([fuerza_teorica(longitud, hv)     for hv in H_vals])
    H_trap       = np.linspace(1.00, 4.80, n + 1)
    F_trap_points = np.array([fuerza_trapecio(longitud, hv, n) for hv in H_trap])

    y_cont = np.linspace(0.00, altura, 400)
    f_cont = integrando(y_cont, longitud, altura)
    y_trap = np.linspace(0.00, altura, n + 1)
    f_trap = integrando(y_trap, longitud, altura)

    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    # ── Gráfica 1: F vs H ──
    axs[0].plot(H_vals, F_trap_vals, label=f"Método del trapecio (n={n})")
    axs[0].plot(H_vals, F_teo_vals, label="Ecuación teórica", linestyle="--")
    axs[0].scatter(H_trap, F_trap_points, color="blue", s=25, zorder=3,
                   label="Puntos evaluados")
    for i in range(len(H_trap)):
        axs[0].plot([H_trap[i], H_trap[i]], [0, F_trap_points[i]],
                    color="gray", linestyle=":", linewidth=0.8)
    for i in range(len(H_trap) - 1):
        axs[0].fill(
            [H_trap[i], H_trap[i], H_trap[i+1], H_trap[i+1]],
            [0, F_trap_points[i], F_trap_points[i+1], 0],
            color='yellow', edgecolor='darkblue', alpha=0.5
        )
    axs[0].set_xlabel("Altura del fluido H (m)")
    axs[0].set_ylabel("Fuerza total F (N)")
    axs[0].set_title(f"Fuerza total vs altura H  |  L = {longitud:.1f} m, n = {n}")
    axs[0].grid(True)
    axs[0].legend()

    # ── Gráfica 2: integrando f(y) ──
    st.markdown("### 📈 Gráfica 2 — Integrando f(y): fuerza diferencial por unidad de altura")
    st.caption(
        "Muestra la función que estoy integrando. "
        "Cada trapecio coloreado en azul es una de las áreas que el método suma "
        "para aproximar la integral. Más trapecios → mejor aproximación."
    )

    axs[1].plot(y_cont, f_cont, label="Integrando f(y)")
    axs[1].scatter(y_trap, f_trap, color="red", s=30, zorder=3,
                   label="Puntos del trapecio")
    for i in range(len(y_trap)):
        axs[1].plot([y_trap[i], y_trap[i]], [0, f_trap[i]],
                    color="gray", linestyle=":", linewidth=0.8)
    for i in range(trapecios_visibles):
        axs[1].fill(
            [y_trap[i], y_trap[i], y_trap[i+1], y_trap[i+1]],
            [0, f_trap[i], f_trap[i+1], 0],
            color='lightblue', edgecolor='red', alpha=0.5
        )
    axs[1].plot(y_trap, f_trap, color="orange", linestyle="--",
                label="Aproximación trapezoidal")
    axs[1].set_xlabel("Profundidad del fluido y (m)")
    axs[1].set_ylabel("Fuerza diferencial por unidad de altura f(y) (N/m)")
    axs[1].set_title(
        f"Integrando de la fuerza  |  H = {altura:.2f} m, n = {n}, "
        f"trapecios visibles = {trapecios_visibles}"
    )
    axs[1].grid(True)
    axs[1].legend()
    plt.tight_layout(pad=2.0, h_pad=2.0)
    st.pyplot(fig)
    plt.close(fig)

    # ==========================================================================
    # ANIMACIÓN DEL DIQUE
    # ==========================================================================
    st.markdown("---")
    st.markdown("### 🌊 Visualización: presión sobre el dique")
    st.caption(
        "Las flechas representan la fuerza que el fluido ejerce sobre el dique en cada altura. "
        "Flechas más largas y rápidas = mayor presión. "
        "Observá que la presión es mayor cerca de la base (mayor profundidad)."
    )

    presiones_lista = [
        float(80.0 * g * (0.250 * yi**3 - yi + 10.0) * (altura - yi))
        for yi in np.linspace(0.05, altura - 0.05, 40)
    ]
    presion_max_val = float(max(presiones_lista))

    html_dique = f"""
    <canvas id="dique" width="700" height="420"
            style="background:#0a0a1a;border-radius:10px;display:block;margin:auto;">
    </canvas>
    <script>
    const canvas = document.getElementById("dique");
    const ctx = canvas.getContext("2d");
    const W = canvas.width, H = canvas.height;
    const altura = {altura};
    const longitud = {longitud};
    const n = {n};
    const presiones = {presiones_lista};
    const presionMax = {presion_max_val};
    const dique_x = W * 0.62;
    const base_y  = H * 0.88;
    const escala_y = (H * 0.78) / altura;
    let flechas = [];
    let tiempo  = 0;
    function nuevaFlecha(yi, pi) {{
        const ratio      = pi / presionMax;
        const velocidad  = 1.5 + 4.5 * ratio;
        const largo_max  = 180 * ratio;
        const y_canvas   = base_y - yi * escala_y;
        return {{ x: dique_x - 10, y: y_canvas, largo_max, velocidad, ratio, progreso: 0 }};
    }}
    function dibujar() {{
        ctx.clearRect(0, 0, W, H);
        for (let i = 0; i < 60; i++) {{
            const y0 = base_y - (i/60)*altura*escala_y;
            const y1 = base_y - ((i+1)/60)*altura*escala_y;
            const prof = i/60;
            ctx.fillStyle = `rgb(0,${{Math.floor(60+80*prof)}},${{Math.floor(180+60*prof)}})`;
            ctx.fillRect(20, y1, dique_x-20, y0-y1);
        }}
        ctx.beginPath();
        ctx.strokeStyle = "rgba(180,230,255,0.7)";
        ctx.lineWidth = 2;
        const sup_y = base_y - altura*escala_y;
        for (let x=20; x<dique_x; x+=2) {{
            const ola = Math.sin((x+tiempo*2)*0.08)*4;
            if (x===20) ctx.moveTo(x, sup_y+ola); else ctx.lineTo(x, sup_y+ola);
        }}
        ctx.stroke();
        const grad = ctx.createLinearGradient(dique_x,0,dique_x+60,0);
        grad.addColorStop(0,"#777"); grad.addColorStop(1,"#aaa");
        ctx.fillStyle = grad;
        ctx.fillRect(dique_x, base_y-altura*escala_y*1.1, 60, altura*escala_y*1.2);
        ctx.fillStyle="#555";
        ctx.fillRect(20, base_y, dique_x+60, 20);
        ctx.strokeStyle="white"; ctx.lineWidth=1;
        ctx.beginPath(); ctx.moveTo(12,base_y); ctx.lineTo(12,base_y-altura*escala_y); ctx.stroke();
        ctx.fillStyle="white"; ctx.font="13px Arial";
        ctx.fillText("H="+altura.toFixed(1)+"m", 2, base_y-altura*escala_y/2);
        ctx.beginPath(); ctx.moveTo(20,base_y+8); ctx.lineTo(dique_x,base_y+8); ctx.stroke();
        ctx.fillText("L="+longitud.toFixed(1)+"m", 20+(dique_x-20)/2-20, base_y+20);
        for (let i=0; i<5; i++) {{
            const yi = altura*(i+0.5)/5;
            const pi = 80*9.81*(0.25*yi**3-yi+10)*(altura-yi);
            ctx.fillStyle=`rgba(255,255,255,${{0.25+0.4*(yi/altura)}})`;
            ctx.font="11px Arial";
            ctx.fillText((pi/1000).toFixed(1)+" kN/m²", 30, base_y-yi*escala_y);
        }}
        for (let f of flechas) {{
            f.progreso += f.velocidad;
            const largo = Math.min(f.progreso, f.largo_max);
            const r=255, g3=Math.floor(255*(1-f.ratio));
            const color=`rgb(${{r}},${{g3}},0)`;
            ctx.strokeStyle=color; ctx.lineWidth=1+3*f.ratio;
            ctx.beginPath(); ctx.moveTo(f.x-largo,f.y); ctx.lineTo(f.x,f.y); ctx.stroke();
            ctx.fillStyle=color;
            ctx.beginPath(); ctx.moveTo(f.x,f.y); ctx.lineTo(f.x-10,f.y-4); ctx.lineTo(f.x-10,f.y+4); ctx.closePath(); ctx.fill();
        }}
        flechas = flechas.filter(f => f.progreso < f.largo_max+20);
        tiempo++;
        const obj = Math.ceil((n/1000)*40);
        if (flechas.length < obj) {{
            const idx=Math.floor(Math.random()*presiones.length);
            const yi=altura*(idx+0.5)/presiones.length;
            const pi=presiones[idx];
            if (Math.random()<(0.3+0.7*(pi/presionMax)) && pi>0)
                flechas.push(nuevaFlecha(yi,pi));
        }}
        ctx.fillStyle="rgba(0,0,0,0.65)";
        ctx.fillRect(W-210,8,200,95);
        ctx.strokeStyle="rgba(255,255,255,0.3)"; ctx.lineWidth=1;
        ctx.strokeRect(W-210,8,200,95);
        ctx.fillStyle="white"; ctx.font="bold 12px Arial";
        ctx.fillText("📊 Parámetros",W-200,28);
        ctx.font="12px Arial";
        ctx.fillStyle="#aef"; ctx.fillText("H = "+altura.toFixed(2)+" m",W-200,48);
        ctx.fillStyle="#ffa"; ctx.fillText("n = "+n+" trapecios",W-200,65);
        ctx.fillStyle="#333"; ctx.fillRect(W-200,72,180,10);
        const grad2=ctx.createLinearGradient(W-200,0,W-20,0);
        grad2.addColorStop(0,"#00ff88"); grad2.addColorStop(0.5,"#ffaa00"); grad2.addColorStop(1,"#ff3300");
        ctx.fillStyle=grad2; ctx.fillRect(W-200,72,(n/1000)*180,10);
        ctx.fillStyle="white"; ctx.font="10px Arial";
        ctx.fillText("densidad de trapecios",W-200,95);
        requestAnimationFrame(dibujar);
    }}
    dibujar();
    </script>
    """
    components.html(html_dique, height=440)

    # ==========================================================================
    # BLOQUE 4 — CONCLUSIONES
    # ==========================================================================
    st.markdown("---")
    st.markdown("### ✅ Conclusiones")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.success("""
**¿Se cumplió el objetivo?**
Sí. Calculé la fuerza total sobre el dique usando la Regla del Trapecio
y la validé contra la solución teórica exacta obteniendo un error < 2%
con solo n = 6 trapecios.
""")
        st.info("""
**¿Por qué el error es tan bajo con n pequeño?**
El integrando f(y) es una función polinómica suave, sin cambios bruscos.
Los trapecios aproximan muy bien funciones suaves, por eso con pocos
intervalos ya se obtiene alta precisión.
""")
    with col_c2:
        st.warning("""
**Limitación del método**
Si la función de densidad del fluido tuviera discontinuidades o cambios
abruptos, necesitaría muchos más trapecios para mantener el error bajo el 2%.
""")
        st.info("""
**Ventaja computacional**
El código permite calcular F para cualquier combinación de L, H y n
en tiempo real, sin necesidad de resolver la integral manualmente
cada vez que cambian los parámetros.
""")