import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
import streamlit as st

# =========================================================
# FÍSICA PARA CIENCIAS DE LA COMPUTACIÓN
# DDD - Parte 1
# Espejismos y refracción de la luz
# Método numérico: Runge-Kutta de cuarto orden (RK4)
# =========================================================

# Índice de refracción en la base
n0 = 1.00030
# Constante de variación del índice de refracción
alpha = 5.00e-3        # 1/m
# Condición inicial
x0 = 0.00              # m
y0 = 3.00              # m
theta0 = -0.150        # rad
# Condición final
xf = 60.0              # m
# Paso de integración
dx = 5.00e-3           # m

def mostrar():

    # =========================================================
    # SIDEBAR — CÓDIGO MATEMÁTICO PARA LA EXPOSICIÓN
    # =========================================================
    with st.sidebar:
        st.divider()
        st.subheader("1️⃣ Parámetros del problema")
        st.code("""
n0     = 1.00030   # índice en y=0
alpha  = 5.00e-3   # variación (1/m)
x0, y0 = 0.00, 3.00
theta0 = -0.150    # rad
xf     = 60.0      # m
dx     = 5.00e-3   # paso (m)
        """, language="python")
        st.divider()
        st.subheader("2️⃣ Índice de refracción")
        st.code("""
def indice_refraccion(y):
    return n0 + alpha * y
        """, language="python")
        st.divider()
        st.subheader("3️⃣ Sistema de EDOs")
        st.code("""
def sistema_ecuaciones(x, u):
    y, theta = u[0], u[1]
    n_y = indice_refraccion(y)
    dy_dx     = np.tan(theta)
    dtheta_dx = alpha / n_y
    return np.array([dy_dx, dtheta_dx])
        """, language="python")
        st.divider()
        st.subheader("4️⃣ RK4 — paso completo")
        st.code("""
k1 = F(x, u)
k2 = F(x+dx/2, u+(dx/2)*k1)
k3 = F(x+dx/2, u+(dx/2)*k2)
k4 = F(x+dx,   u+dx*k3)
u  = u + (dx/6)*(k1+2*k2+2*k3+k4)
        """, language="python")
        st.divider()
        st.subheader("5️⃣ Verificación del espejismo")
        st.code("""
alpha_min = (
    n0*(1-cos(theta0))
    / (y0*cos(theta0))
)
# debe cumplirse: alpha > alpha_min
        """, language="python")
        st.divider()
        st.subheader("6️⃣ y_min teórico")
        st.code("""
y_min_teo = (
    (n0 + alpha*y0)*cos(theta0) - n0
) / alpha
        """, language="python")
        st.divider()

    # =========================================================
    # BLOQUE 1 — TÍTULO E INTRODUCCIÓN
    # =========================================================
    st.markdown("# 🌅 DDD — Espejismos y refracción de la luz")
    st.markdown("---")
    st.markdown("""
### 🏜️ ¿De qué trata?

Un **espejismo** ocurre en el desierto o en el asfalto caliente: el suelo
calienta el aire cercano, haciendo que su densidad (y su **índice de
refracción**) sea menor que el del aire frío de arriba.

Cuando un rayo de luz viaja a través de este gradiente de índice, se curva
gradualmente — en vez de llegar al suelo, **da vuelta hacia arriba** y llega
al ojo del observador desde abajo, simulando el reflejo de agua.

El objetivo es simular numéricamente la trayectoria del rayo usando
**Runge-Kutta de 4to orden (RK4)** y encontrar la altura mínima que alcanza
antes de curvarse, comparándola con el valor teórico.
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
<tr><td style="padding:8px;">n₀</td><td style="padding:8px;">Índice de refracción en y = 0 (base)</td><td style="padding:8px;">1,00030</td></tr>
<tr><td style="padding:8px;">α (alpha)</td><td style="padding:8px;">Constante de variación del índice con la altura (m⁻¹)</td><td style="padding:8px;">5,00×10⁻³ m⁻¹</td></tr>
<tr><td style="padding:8px;">n(y)</td><td style="padding:8px;">Índice de refracción a la altura y</td><td style="padding:8px;">n₀ + α·y</td></tr>
<tr><td style="padding:8px;">y(x)</td><td style="padding:8px;">Altura del rayo en la posición horizontal x (m)</td><td style="padding:8px;">variable de estado</td></tr>
<tr><td style="padding:8px;">θ(x)</td><td style="padding:8px;">Ángulo de inclinación del rayo respecto a la horizontal (rad)</td><td style="padding:8px;">variable de estado</td></tr>
<tr><td style="padding:8px;">x₀, y₀</td><td style="padding:8px;">Posición inicial del rayo (m)</td><td style="padding:8px;">0,00 m, 3,00 m</td></tr>
<tr><td style="padding:8px;">θ₀</td><td style="padding:8px;">Ángulo inicial de disparo (rad)</td><td style="padding:8px;">-0,150 rad</td></tr>
<tr><td style="padding:8px;">xf</td><td style="padding:8px;">Posición horizontal final de la simulación (m)</td><td style="padding:8px;">60,0 m</td></tr>
<tr><td style="padding:8px;">Δx</td><td style="padding:8px;">Paso de integración del método RK4 (m)</td><td style="padding:8px;">5,00×10⁻³ m</td></tr>
<tr><td style="padding:8px;">y_min</td><td style="padding:8px;">Altura mínima que alcanza el rayo antes de curvarse (m)</td><td style="padding:8px;">calculada</td></tr>
<tr><td style="padding:8px;">x_retorno</td><td style="padding:8px;">Posición horizontal del punto de retorno (m)</td><td style="padding:8px;">calculada</td></tr>
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
        st.markdown("**Paso 1 — Índice de refracción variable**")
        st.markdown("En el desierto el aire caliente tiene menor densidad → menor n:")
        st.latex(r"n(y) = n_0 + \alpha \cdot y \quad (\alpha > 0)")
        st.caption("📌 α > 0 significa que n crece con la altura: abajo (caliente) n chico, arriba (frío) n grande.")

        st.markdown("**Paso 2 — Ley de Snell diferencial (ecuación dinámica)**")
        st.markdown("La tasa de cambio del ángulo depende del gradiente de n:")
        st.latex(r"\frac{d\theta}{dx} = \frac{1}{n(y)} \cdot \frac{dn}{dy} = \frac{\alpha}{n(y)}")
        st.caption("📌 Como n(y) = n₀ + α·y, entonces dn/dy = α (constante).")

    with col_f2:
        st.markdown("**Paso 3 — Ecuación cinemática**")
        st.markdown("La altura cambia con la posición horizontal según el ángulo:")
        st.latex(r"\frac{dy}{dx} = \tan\theta")
        st.caption("📌 Si θ < 0 el rayo baja; si θ > 0 sube; en θ = 0 está en el punto más bajo.")

        st.markdown("**Paso 4 — Sistema acoplado de EDOs**")
        st.markdown("Las dos ecuaciones forman un sistema que se resuelve simultáneamente:")
        st.latex(r"\frac{d}{dx}\begin{pmatrix}y\\\theta\end{pmatrix} = \begin{pmatrix}\tan\theta \\ \alpha/n(y)\end{pmatrix}")

    st.markdown("**Invariante de Snell** — cantidad que se conserva a lo largo de toda la trayectoria:")
    st.latex(r"n(y) \cdot \cos\theta = \text{constante} = n(y_0)\cdot\cos\theta_0")

    st.markdown("**Altura mínima teórica** — en el punto de retorno θ = 0, entonces cos(0) = 1:")
    st.latex(
        r"y_{\min} = \frac{(n_0 + \alpha \cdot y_0)\cdot\cos\theta_0 - n_0}{\alpha}"
    )

    st.markdown("**Condición de existencia del espejismo** — para que y_min > 0 antes del suelo:")
    st.latex(
        r"\alpha > \frac{n_0 \cdot (1 - \cos\theta_0)}{y_0 \cdot \cos\theta_0}"
    )

    st.info("""
💡 Si α no cumple esa condición, el rayo llega al suelo sin curvarse
y no hay espejismo. Con los parámetros elegidos se verifica que sí se cumple.
""")

    # =========================================================
    # BLOQUE 4 — MÉTODO NUMÉRICO RK4
    # =========================================================
    st.markdown("---")
    st.markdown("### 🔢 Método numérico: Runge-Kutta de 4to orden (RK4)")
    st.markdown("""
El sistema de EDOs no tiene solución analítica simple, por eso lo resuelvo
numéricamente. RK4 avanza el vector de estado `u = (y, θ)` desde x₀ hasta xf
en pasos de Δx, evaluando **4 pendientes intermedias** en cada paso y
promediándolas con pesos (1, 2, 2, 1)/6:
""")
    st.latex(
        r"\vec{u}_{i+1} = \vec{u}_i + \frac{\Delta x}{6}(\vec{k}_1 + 2\vec{k}_2 + 2\vec{k}_3 + \vec{k}_4)"
    )
    st.markdown("""
donde las 4 pendientes se calculan como:
""")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.latex(r"\vec{k}_1 = F(x_i,\, \vec{u}_i)")
        st.latex(r"\vec{k}_2 = F\!\left(x_i+\tfrac{\Delta x}{2},\, \vec{u}_i+\tfrac{\Delta x}{2}\vec{k}_1\right)")
    with col_k2:
        st.latex(r"\vec{k}_3 = F\!\left(x_i+\tfrac{\Delta x}{2},\, \vec{u}_i+\tfrac{\Delta x}{2}\vec{k}_2\right)")
        st.latex(r"\vec{k}_4 = F(x_i+\Delta x,\, \vec{u}_i+\Delta x\,\vec{k}_3)")

    st.markdown("""
- **k₁** usa la pendiente al inicio del paso
- **k₂ y k₃** refinan en el punto medio (peso doble → mayor precisión)
- **k₄** evalúa al final del paso
- Con Δx = 5×10⁻³ m se hacen **12.000 pasos** en los 60 m de recorrido
""")

    # =========================================================
    # BLOQUE 5 — CONEXIÓN CÓDIGO-FÍSICA
    # =========================================================
    st.markdown("---")
    st.markdown("### 💻 ¿Cómo se conecta el código con la física?")
    st.markdown("""
| Concepto físico | Línea en el código |
|---|---|
| n(y) = n₀ + α·y | `indice_refraccion(y): return n0 + alpha * y` |
| dy/dx = tan(θ) | `dy_dx = np.tan(theta)` |
| dθ/dx = α/n(y) | `dtheta_dx = alpha / n_y` |
| Pendiente k₁ | `k1 = sistema_ecuaciones(x, u)` |
| Avance RK4 | `u = u + (dx/6)*(k1 + 2*k2 + 2*k3 + k4)` |
| y_min teórico | `y_min_teo = ((n0+alpha*y0)*cos(theta0) - n0) / alpha` |
| Verificación espejismo | `alpha > n0*(1-cos(theta0)) / (y0*cos(theta0))` |
""")
    st.caption("📌 Abrí el sidebar para señalar esas líneas exactas durante la exposición.")

    # =========================================================
    # FUNCIONES DEL MODELO FÍSICO (sin cambios)
    # =========================================================
    def formato_3cs(valor, posicion=None):
        if abs(valor) < 1e-12:
            return "0,00"
        cifras = 3
        decimales = cifras - int(np.floor(np.log10(abs(valor)))) - 1
        decimales = max(decimales, 0)
        return f"{valor:.{decimales}f}".replace(".", ",")

    def aplicar_formato_grafica(ax):
        ax.xaxis.set_major_formatter(FuncFormatter(formato_3cs))
        ax.yaxis.set_major_formatter(FuncFormatter(formato_3cs))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=8))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=7))
        ax.grid(True, alpha=0.35)

    def indice_refraccion(y):
        """Índice de refracción variable con la altura. n(y) = n0 + alpha*y"""
        return n0 + alpha * y

    def sistema_ecuaciones(x, u):
        """
        Sistema de ecuaciones diferenciales:
        dy/dx = tan(theta)
        dtheta/dx = (1/n(y))*(dn/dy)
        Como n(y) = n0 + alpha*y, entonces dn/dy = alpha.
        """
        y = u[0]
        theta = u[1]
        n_y = indice_refraccion(y)
        dy_dx = np.tan(theta)
        dtheta_dx = alpha / n_y
        return np.array([dy_dx, dtheta_dx])

    def rk4(x0, y0, theta0, xf, dx):
        """Resuelve el sistema usando RK4. Devuelve arreglos de x, y y theta."""
        x_vals = []
        y_vals = []
        theta_vals = []
        x = x0
        u = np.array([y0, theta0], dtype=float)
        while x <= xf:
            x_vals.append(x)
            y_vals.append(u[0])
            theta_vals.append(u[1])
            k1 = sistema_ecuaciones(x, u)
            k2 = sistema_ecuaciones(x + dx/2, u + (dx/2)*k1)
            k3 = sistema_ecuaciones(x + dx/2, u + (dx/2)*k2)
            k4 = sistema_ecuaciones(x + dx, u + dx*k3)
            u = u + (dx/6)*(k1 + 2*k2 + 2*k3 + k4)
            x = x + dx
        return np.array(x_vals), np.array(y_vals), np.array(theta_vals)

    # =========================================================
    # EJECUTAR SIMULACIÓN
    # =========================================================
    x_vals, y_vals, theta_vals = rk4(x0, y0, theta0, xf, dx)

    indice_minimo  = np.argmin(y_vals)
    y_min_simulado = y_vals[indice_minimo]
    x_retorno      = x_vals[indice_minimo]
    theta_retorno  = theta_vals[indice_minimo]

    y_min_teorico   = ((n0 + alpha*y0)*np.cos(theta0) - n0) / alpha
    error_porcentual = abs((y_min_teorico - y_min_simulado) / y_min_teorico) * 100

    alpha_min = (n0 * (1 - np.cos(theta0))) / (y0 * np.cos(theta0))

    # =========================================================
    # BLOQUE 6 — VERIFICACIÓN Y RESULTADOS
    # =========================================================
    st.markdown("---")
    st.markdown("### 📊 Verificación del espejismo y resultados")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if alpha > alpha_min:
            st.success(f"""
✅ **El espejismo existe**

α utilizado = {alpha:.2e} m⁻¹ > α_mínimo = {alpha_min:.6e} m⁻¹

La condición se cumple: el rayo se curvará antes de tocar el suelo.
""")
        else:
            st.error("❌ El espejismo NO existe con estos parámetros.")

    with col_v2:
        st.markdown(f"""
| Resultado | Valor |
|---|---|
| x_retorno (simulado) | {formato_3cs(x_retorno)} m |
| y_min (simulado, RK4) | {formato_3cs(y_min_simulado)} m |
| y_min (teórico, Ec. v) | {formato_3cs(y_min_teorico)} m |
| Error porcentual | {error_porcentual:.3f} % |
""")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("x_retorno", f"{formato_3cs(x_retorno)} m")
    col_m2.metric("y_min simulado", f"{formato_3cs(y_min_simulado)} m")
    col_m3.metric("y_min teórico",  f"{formato_3cs(y_min_teorico)} m")
    col_m4.metric("Error (%)",      f"{error_porcentual:.3f}")

    # =========================================================
    # FUNCIONES DE DIBUJO (sin cambios en física)
    # =========================================================
    x_min = float(x_vals.min())
    x_max = float(x_vals.max())
    y_min_grafica = -0.30
    y_max_grafica = float(max(y_vals) + 0.50)
    x_observador  = x_max + 1.50
    y_observador  = 1.20

    def dibujar_fondo_aire(ax):
        """Dibuja el fondo con gradiente: aire caliente abajo y aire frío arriba."""
        ax.set_xlim(x_min, x_max + 2.00)
        ax.set_ylim(y_min_grafica, y_max_grafica)
        gradiente = np.linspace(0, 1, 300).reshape(300, 1)
        mapa_aire = LinearSegmentedColormap.from_list(
            "gradiente_aire", ["#ffd1a3", "#fff7ec", "#dbe9ff"]
        )
        ax.imshow(gradiente,
                  extent=[x_min, x_max + 2.00, y_min_grafica, y_max_grafica],
                  origin="lower", aspect="auto", cmap=mapa_aire, alpha=0.75, zorder=0)
        ax.axhline(0, linewidth=3, color="#8B4513", label="Suelo (y = 0 m)", zorder=3)
        ax.text(x_min + 0.02*(x_max - x_min), y_max_grafica - 0.35,
                "Aire FRÍO (n grande)", fontsize=11, color="navy", weight="bold")
        ax.text(x_min + 0.02*(x_max - x_min), 0.12,
                "Aire CALIENTE (n pequeño)", fontsize=11, color="#8B4513", weight="bold")

    def anotar_angulo_con_tangente(ax, indice, desplazamiento_x, desplazamiento_y, longitud_tangente=4.0):
        """Dibuja un punto sobre la trayectoria, una recta tangente local y el valor de θ."""
        x_p     = x_vals[indice]
        y_p     = y_vals[indice]
        theta_p = theta_vals[indice]
        theta_p_deg = np.degrees(theta_p)
        ax.scatter(x_p, y_p, color="black", s=35, zorder=7)
        dx_t = longitud_tangente / 2
        x_tan = np.array([x_p - dx_t, x_p + dx_t])
        y_tan = y_p + np.tan(theta_p) * (x_tan - x_p)
        ax.plot(x_tan, y_tan, color="black", linewidth=3, solid_capstyle="round", zorder=6)
        ax.annotate(
            r"$\theta$ = " + formato_3cs(theta_p_deg) + "°",
            xy=(x_p, y_p),
            xytext=(x_p + desplazamiento_x, y_p + desplazamiento_y),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2),
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gray", alpha=0.85),
            zorder=8
        )

    def formato_theta_retorno(theta):
        """Si el ángulo es muy pequeño, lo muestro como cero (físicamente θ_retorno = 0)."""
        if abs(theta) < 5e-4:
            return "0,000"
        return formato_3cs(theta)

    # =========================================================
    # GRÁFICA 1 — Trayectoria y vs x
    # =========================================================
    st.markdown("---")
    st.markdown("### 📈 Gráfica 1 — Trayectoria del rayo (y vs x)")
    st.caption(
        "El fondo muestra el gradiente térmico: naranja (aire caliente, n pequeño) → celeste "
        "(aire frío, n grande). La curva roja es la trayectoria simulada por RK4. "
        "Las líneas negras con ángulo muestran la inclinación local del rayo en dos puntos."
    )
    fig1 = plt.figure(figsize=(12, 6.5))
    ax = fig1.add_axes([0.08, 0.12, 0.88, 0.80])
    dibujar_fondo_aire(ax)
    ax.plot(x_vals, y_vals, color="crimson", linewidth=3,
            label="Trayectoria del rayo (RK4)", zorder=5)
    ax.scatter(x_retorno, y_min_simulado, color="black", s=70, zorder=8,
               label=r"Punto de retorno $(x_{\mathrm{retorno}}, y_{\min})$")
    ax.axvline(x_retorno, linestyle="--", linewidth=1.3, color="gray", alpha=0.8, zorder=4)
    ax.axhline(y_min_simulado, linestyle="--", linewidth=1.3, color="gray", alpha=0.8, zorder=4)
    ax.annotate(
        r"$y_{\min}$ = " + formato_3cs(y_min_simulado) + " m\n"
        r"$x_{\mathrm{retorno}}$ = " + formato_3cs(x_retorno) + " m",
        xy=(x_retorno, y_min_simulado),
        xytext=(x_retorno + 0.13*(x_max - x_min),
                y_min_simulado + 0.28*(y_max_grafica - y_min_grafica)),
        arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5),
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.85),
        zorder=9
    )
    anotar_angulo_con_tangente(ax, int(0.10*len(x_vals)),  2.0,  0.20, longitud_tangente=4.0)
    anotar_angulo_con_tangente(ax, int(0.68*len(x_vals)),  2.0, -0.10, longitud_tangente=4.0)
    ax.set_title("Altura del rayo vs posición horizontal", fontsize=14, weight="bold")
    ax.set_xlabel("Posición horizontal, x (m)", fontsize=12)
    ax.set_ylabel("Altura del rayo, y (m)", fontsize=12)
    ax.legend(loc="upper right", fontsize=10, framealpha=0.95)
    aplicar_formato_grafica(ax)
    st.pyplot(fig1)
    plt.close(fig1)

    # =========================================================
    # GRÁFICA 2 — Evolución angular θ vs x
    # =========================================================
    st.markdown("### 📈 Gráfica 2 — Evolución angular del rayo (θ vs x)")
    st.caption(
        "Muestra cómo varía el ángulo de inclinación del rayo a lo largo del recorrido. "
        "θ < 0 → rayo bajando; θ = 0 → punto más bajo (retorno); θ > 0 → rayo subiendo. "
        "La curva es casi lineal porque n(y) varía menos del 2% en todo el recorrido."
    )
    fig2 = plt.figure(figsize=(12, 6.5))
    ax = fig2.add_axes([0.08, 0.12, 0.88, 0.80])
    ax.plot(x_vals, theta_vals, linewidth=2, label="Ángulo local de propagación del rayo")
    ax.axhline(0, linestyle="--", linewidth=1.5, label="Condición de retorno: θ = 0 rad")
    ax.scatter(x_retorno, theta_retorno, s=60, zorder=5,
               label=f"Ángulo en el retorno: θ = {formato_theta_retorno(theta_retorno)} rad")
    ax.set_title("Ángulo de Propagación vs Posición Horizontal", fontsize=14, weight="bold")
    ax.set_xlabel("Posición horizontal, x (m)", fontsize=12)
    ax.set_ylabel("Ángulo de propagación, θ (rad)", fontsize=12)
    ax.legend(loc="upper left", fontsize=10, framealpha=0.95)
    aplicar_formato_grafica(ax)
    st.pyplot(fig2)
    plt.close(fig2)

    # =========================================================
    # GRÁFICA 3 — Animación interactiva con slider
    # =========================================================
    st.markdown("### 📈 Gráfica 3 — Exploración interactiva: ángulo local del rayo")
    st.caption(
        "Mové el slider para recorrer la trayectoria. La línea punteada gris es la referencia "
        "horizontal (θ = 0°) y la línea negra sólida es la dirección real del rayo. "
        "La línea celeste punteada muestra la dirección aparente hacia el observador — "
        "eso es lo que el ojo interpreta como un reflejo de agua."
    )

    x_st = st.slider(
        "Posición x (m)",
        float(x_vals.min()), float(x_vals.max()), float(x_vals.min())
    )

    elementos_animacion = {}
    modo_actual = ["Animacion"]

    fig3 = plt.figure(figsize=(12, 6.5))
    ax = fig3.add_axes([0.08, 0.12, 0.88, 0.80])

    dibujar_fondo_aire(ax)
    ax.set_xlim(x_min, x_max + 2.00)
    ax.set_ylim(y_min_grafica, y_max_grafica)
    ax.set_title("Espejismo: exploración interactiva del rayo de luz", fontsize=14, weight="bold")
    ax.set_xlabel("Posición horizontal, x (m)", fontsize=12)
    ax.set_ylabel("Altura del rayo, y (m)", fontsize=12)
    ax.plot(x_vals, y_vals, color="crimson", linewidth=2.5, zorder=5, label="Trayectoria real del rayo")
    ax.plot(x_retorno, y_min_simulado, marker="x", markersize=10, markeredgewidth=2,
            color="darkred", zorder=7, label="Punto de retorno")
    ax.plot(x_observador, y_observador, "o", color="green", markersize=10, zorder=7, label="Observador")

    punto_rayo,      = ax.plot([], [], "o", color="black", markersize=8, zorder=9)
    linea_aparente,  = ax.plot([], [], "--", linewidth=2, color="deepskyblue", zorder=6, label="Dirección aparente")
    linea_ref_angulo,= ax.plot([], [], "--", color="gray", linewidth=1.4, zorder=7, label="Referencia horizontal")
    linea_dir_angulo,= ax.plot([], [], color="black", linewidth=2.2, zorder=8, label="Dirección real del rayo")
    texto_angulo = ax.annotate("", xy=(0, 0), fontsize=10, fontweight="bold", color="black", zorder=10)
    texto_info   = ax.text(0.02, 0.97, "", transform=ax.transAxes, va="top", fontsize=11,
                           bbox=dict(facecolor="white", alpha=0.85), zorder=10)

    elementos_animacion = {
        "punto_rayo": punto_rayo,
        "linea_aparente": linea_aparente,
        "linea_ref_angulo": linea_ref_angulo,
        "linea_dir_angulo": linea_dir_angulo,
        "texto_angulo": texto_angulo,
        "texto_info": texto_info,
    }

    LARGO_ANGULO = 5.0
    indice = np.argmin(np.abs(x_vals - x_st))
    x_p    = x_vals[indice]
    y_p    = y_vals[indice]
    theta  = theta_vals[indice]
    theta_deg = np.degrees(theta)

    punto_rayo.set_data([x_p], [y_p])
    linea_aparente.set_data([x_p, x_observador], [y_p, y_observador])
    linea_ref_angulo.set_data([x_p, x_p + LARGO_ANGULO], [y_p, y_p])
    linea_dir_angulo.set_data([x_p, x_p + LARGO_ANGULO*np.cos(theta)],
                               [y_p, y_p + LARGO_ANGULO*np.sin(theta)])
    r_etiqueta = LARGO_ANGULO * 0.35
    texto_angulo.set_text(r"$\theta$ = " + formato_3cs(theta_deg) + "°")
    texto_angulo.set_position((x_p + r_etiqueta*np.cos(theta/2),
                                y_p + r_etiqueta*np.sin(theta/2)))
    texto_info.set_text(
        "x = " + formato_3cs(x_p) + " m\n"
        "y = " + formato_3cs(y_p) + " m\n"
        r"$\theta$ = " + formato_3cs(theta) + " rad\n"
        r"$\theta$ = " + formato_3cs(theta_deg) + "°"
    )
    ax.legend(loc="upper right", fontsize=9, framealpha=0.95)
    aplicar_formato_grafica(ax)
    st.pyplot(fig3)
    plt.close(fig3)

    # =========================================================
    # BLOQUE 7 — CONCLUSIONES
    # =========================================================
    st.markdown("---")
    st.markdown("### ✅ Conclusiones")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.success(f"""
**¿Se cumplió el objetivo?**
Sí. Se simuló correctamente la trayectoria del rayo con RK4 usando
Δx = {dx:.3e} m (12.000 pasos en 60 m).
El y_min simulado ({formato_3cs(y_min_simulado)} m) coincide con el teórico
({formato_3cs(y_min_teorico)} m) con un error de solo {error_porcentual:.3f}%,
confirmando que el modelo físico está bien implementado.
""")
        st.info("""
**¿Por qué el error es tan bajo?**
RK4 tiene error de truncamiento de orden 4 en Δx. Con un paso tan
pequeño (5 mm), la acumulación de error a lo largo de 60 m es
prácticamente nula.
""")
    with col_c2:
        st.warning("""
**Limitación del método**
Si α fuera tan pequeño que no cumpliera la condición de existencia
del espejismo, el rayo llegaría al suelo y la simulación perdería
sentido físico. Por eso se verifica la condición antes de simular.
""")
        st.info(f"""
**Ventaja computacional**
El código resuelve simultáneamente las dos EDOs acopladas (y y θ)
en cada paso, usando solo evaluaciones de la función F(x,u) —
sin necesidad de calcular derivadas superiores como haría Taylor.
Eso hace a RK4 preciso y eficiente a la vez.
""")
