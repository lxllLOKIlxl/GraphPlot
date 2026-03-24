import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from io import BytesIO

# Glassmorphism + м'який темний градієнт
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #232946 0%, #273469 70%, #a7a7a7 100%);
        color: #f4faff;
    }
    .block-container {
        max-width: 900px;
        margin: auto;
        background: rgba(255,255,255,0.13);
        border-radius: 18px;
        padding: 36px 24px 24px 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.19);
        backdrop-filter: blur(6px);
    }
    label, .stTextInput label, .stNumberInput label {
        color: #202448 !important;
        font-weight: 600;
    }
    h1, .stApp h1 {
        font-family: 'Arial Black', sans-serif !important;
        color: #eeb96b;
        text-align:center;
        letter-spacing: 1px;
        text-shadow: 1px 2px 15px #000A;
    }
    .stButton>button {
        border-radius: 22px !important;
        font-weight: 700 !important;
        background: #ffb700;
        color: #222 !important;
        box-shadow: 1px 1px 9px #0009;
        padding: 0.5em 2em;
    }
    </style>
    """, unsafe_allow_html=True)

# ---- Sidebar: Інструкція ----
with st.sidebar:
    st.markdown(
        "<h2 style='color:#ffea80;text-align:center;'>📚 Інструкція використання</h2>", 
        unsafe_allow_html=True
    )
    st.markdown("""
1. **Введіть функції** через кому, наприклад:
    - `sin(x)`
    - `x**2 + 3*x - 2`
    - `exp(-x)*cos(x)`  
    _💡 Можна ввести кілька: `sin(x), cos(x), ln(x)`_

2. **Встановіть межі графіка:**
    - Виберіть X<sub>min</sub> і X<sub>max</sub> (наприклад, від -5 до 5).

3. **Налаштуйте стиль:**
    - Можна зафарбувати підграфік чи додати похідну.

4. **Натисніть `��обудувати графік`**
    ---
    🔗 *Графік можна завантажити як PNG.*

    <br>
    <small style="color:#f6e27a;">Підтримка функцій: sin, cos, tan, exp, ln, sqrt, abs, log(x,осн.)</small>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("Автор: Шаблінський 2 курс | Версія 2.1", icon="🎓")

# ---- ГОЛОВНА ----
def main():
    st.markdown("<h1>GraphPlot – Візуалізація математичних функцій</h1>", unsafe_allow_html=True)
    st.info("Введіть одну або декілька функцій та побудуйте їх графіки на обраних межах.", icon="🔔")

    st.subheader("🔢 Ваші функції")
    st.text("➡�� Введіть математичні вирази через кому (наприклад: sin(x), cos(x), x**2)")
    func_input = st.text_input("Функції для побудови:", "sin(x), exp(-x)*cos(x)")

    latex_show = st.checkbox("Показати формули у LaTeX", value=True)

    st.subheader("📐 Межі графіка X")
    c1, c2 = st.columns(2)
    x_min = c1.number_input("Мінімум X", value=-10.0, help="Введіть найменше X для графіка (наприклад, -10)")
    x_max = c2.number_input("Максимум X", value=10.0, help="Введіть найбільше X для графіка (наприклад, 10)")
    num_points = st.slider("Кількість точок на графіку", 100, 2000, 400)

    st.subheader("🎨 Стиль графіка")
    fill_area = st.checkbox("Зафарбувати область під першою функцією", value=False)
    show_derivative = st.checkbox("Додати похідну першої функції", value=False)
    download_graph = st.checkbox("Дозволити завантаження графіка", value=True)

    with st.expander("ℹ️ Приклади для полів", expanded=False):
        st.markdown(
            "**Функції**:  \n"
            "`sin(x)`, `x**2-5`, `exp(-x)*cos(2*x)`, `abs(x/2)+3`, `sqrt(x)`  \n"
            "**Межі X**:  \n"
            "`Мінімум X`: -6, `Максимум X`: 6"
        )

    # --- Побудова ---
    if st.button("🎨 Побудувати графік 🚀"):
        x = sp.symbols('x')
        xx = np.linspace(x_min, x_max, num_points)
        fig, ax = plt.subplots(figsize=(9,5))
        colors = ["#d7263d", "#305aa5", "#198c2e", "#8338ec", "#ff9700", "#808000", "#1e656d"]
        error_cnt = 0

        functions = [f.strip() for f in func_input.split(",") if f.strip()]
        for i, fstr in enumerate(functions):
            try:
                expr = sp.sympify(
                    fstr,
                    locals={'sin':sp.sin, 'cos':sp.cos, 'tan':sp.tan, 'exp':sp.exp, 'log':sp.log, 'sqrt':sp.sqrt, 'abs':sp.Abs, 'ln':sp.ln}
                )
                f_lambd = sp.lambdify(x, expr, 'numpy')
                y = f_lambd(xx)
                if latex_show:
                    st.latex(f"f_{i+1}(x) = {sp.latex(expr)}")
                label = f"f{i+1}(x) = {fstr}"
                ax.plot(xx, y, color=colors[i%len(colors)], lw=2, label=label)
                if i==0 and fill_area:
                    ax.fill_between(xx, y, color=colors[0], alpha=0.10)
                if i==0 and show_derivative:
                    diff = sp.diff(expr, x)
                    df_lambd = sp.lambdify(x, diff, 'numpy')
                    yd = df_lambd(xx)
                    ax.plot(xx, yd, '--', color="#ec5e00", lw=2, label='Похідна')
                    st.latex(r"f_1'(x) = " + sp.latex(diff))
            except Exception as e:
                error_cnt += 1
                st.error(f"Помилка у функції {i+1}:\n**{fstr}**\n{e}")

        ax.legend()
        ax.set_xlabel("X", fontsize=12)
        ax.set_ylabel("Y", fontsize=12)
        ax.set_title("Графік(-и) функцій", fontsize=16)
        ax.grid(True, linestyle="--", alpha=0.7)
        st.pyplot(fig)

        if download_graph:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            st.download_button(
                label="⬇️ Завантажити графік PNG",
                data=buf.getvalue(),
                file_name="graphplot.png",
                mime="image/png"
            )
        if error_cnt==0:
            st.success("Графік(и) побудовано успішно! 👌")

    st.markdown("---")
    st.caption("© Шаблінський, 2 курс | Стиль UX/UI — Copilot Pro")

if __name__ == "__main__":
    main()
