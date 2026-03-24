import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from io import BytesIO

# === ЮЗЕРСЬКИЙ ВИБІР ТЕМИ (світла/темна) ===
with st.sidebar:
    st.markdown("## 🎨 Вибір теми")
    theme = st.radio("Виберіть стиль фону:", ("Світла", "Темна"), horizontal=True)
    custom_css = ""
    if theme == "Світла":
        custom_css = """
        <style>
        .block-container {
            background: rgba(255,255,255,0.94);
            border-radius: 18px;
            box-shadow: 0 4px 20px 0 rgba(180,190,200,0.09);
        }
        h1, .stApp h1 {
            color: #232946;
        }
        </style>
        """
    else:
        custom_css = """
        <style>
        .block-container {
            background: linear-gradient(120deg, #232946 0%, #273469 70%, #b2c2e6 100%);
            border-radius: 18px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.13);
        }
        h1, .stApp h1 {
            color: #eeb96b;
            text-shadow: 1px 2px 15px #000A;
        }
        label, .stTextInput label, .stNumberInput label {
            color: #eeb96b !important;
        }
        </style>
        """
    st.markdown("---")
    st.markdown(
        "<h2 style='color:#ffea80;text-align:center;'>📚 Інструкція</h2>"
        "<ol>"
        "<li><b>Введіть функції</b> через кому: <code>sin(x), cos(x), ln(x)</code></li>"
        "<li><b>Задайте межі X</b></li>"
        "<li><b>Обирайте стиль</b>, натискайте <b>Побудувати графік</b></li>"
        "</ol>"
        "<small style='color:#ffeebb;'>Доступні: sin, cos, tan, exp, ln, sqrt, abs...</small>",
        unsafe_allow_html=True
    )
    st.info("Автор: Шаблінський | Версія 2.8", icon="🎓")

st.markdown(custom_css, unsafe_allow_html=True)

# --- СЛУЖБОВІ ФУНКЦІЇ ---
ALLOWED_FUNCS = {
    'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
    'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt, 'abs': sp.Abs, 'ln': sp.ln
}
ALLOWED_FUNCNAMES = set(ALLOWED_FUNCS.keys())

def clean_function_input(raw):
    return raw.replace('^', '**')

def is_supported_functions(expr):
    for func in expr.atoms(sp.Function):
        if func.func.__name__ not in ALLOWED_FUNCNAMES:
            return False, func.func.__name__
    return True, None

# --- ГОЛОВНА ПРОГРАМА ---
def main():
    st.markdown("<h1>GraphPlot – Візуалізація математичних функцій</h1>", unsafe_allow_html=True)
    st.info("Введіть одну або декілька функцій, побудуйте графіки. Все просто та безпечно!", icon="🔔")
    st.subheader("🔢 Ваші функції")
    st.text("Введіть через кому, напр.: sin(x), cos(x), x^2")
    func_input = st.text_input("Функції для побудови:", "sin(x), exp(-x)*cos(x)")
    latex_show = st.checkbox("Показати формули у LaTeX", value=True)

    st.subheader("📐 Межі графіка X")
    c1, c2 = st.columns(2)
    x_min = c1.number_input("Мінімум X", value=-10.0)
    x_max = c2.number_input("Максимум X", value=10.0)
    if x_min >= x_max:
        st.warning("❗ Мінімум X має бути меншим, ніж Максимум X!")
        st.stop()
    num_points = st.slider("Кількість точок на графіку", 100, 2000, 400)

    st.subheader("🎨 Стиль графіка")
    fill_area = st.checkbox("Зафарбувати область під першою функцією", value=False)
    show_derivative = st.checkbox("Додати похідну першої функції", value=False)
    download_graph = st.checkbox("Дозволити завантаження графіка", value=True)

    with st.expander("ℹ️ Приклади для полів", expanded=False):
        st.markdown(
            "**Функції**:  \n"
            "`sin(x)`, `x^2-5`, `exp(-x)*cos(2*x)`, `abs(x/2)+3`, `sqrt(x)`  \n"
            "**Межі X**:  \n"
            "`Мінімум X`: -6, `Максимум X`: 6"
        )

    # --- Підготовка даних ---
    x = sp.symbols('x')
    xx = np.linspace(x_min, x_max, num_points)
    functions = [s for s in [clean_function_input(f.strip()) for f in func_input.split(",")] if s]

    if st.button("🎨 Побудувати графік 🚀"):
        fig, ax = plt.subplots(figsize=(9,5))
        colors = ["#d7263d", "#305aa5", "#198c2e", "#8338ec", "#ff9700", "#808000", "#1e656d"]
        error_cnt = 0
        for i, fstr in enumerate(functions):
            try:
                expr = sp.sympify(fstr, locals=ALLOWED_FUNCS)
                is_ok, bad_func = is_supported_functions(expr)
                if not is_ok:
                    st.warning(f"Вираз містить невідому функцію `{bad_func}`. Дозволені: {sorted(ALLOWED_FUNCNAMES)}")
                    continue
                f_lambd = sp.lambdify(x, expr, 'numpy')
                y = f_lambd(xx)
                if not np.any(np.isfinite(y)):
                    st.error(f"Функція **{fstr}** не має дійсних значень на цьому проміжку.")
                    continue
                if latex_show:
                    st.latex(f"f_{i+1}(x) = {sp.latex(expr)}")
                label = f"f{i+1}(x) = {fstr}"
                ax.plot(xx, y, color=colors[i%len(colors)], lw=2, label=label)
                if i==0 and fill_area:
                    ax.fill_between(xx, y, color=colors[0], alpha=0.08)
                if i==0 and show_derivative:
                    diff = sp.diff(expr, x)
                    df_lambd = sp.lambdify(x, diff, 'numpy')
                    yd = df_lambd(xx)
                    ax.plot(xx, yd, '--', color="#ec5e00", lw=2, label='Похідна')
                    st.latex(r"f_1'(x) = " + sp.latex(diff))
            except Exception as e:
                msg = str(e)
                if "could not parse" in msg or "unexpected EOF" in msg:
                    st.error(f"❌ Схоже, помилка синтаксису: **{fstr}** (приклад: x^2+3*x-2 → x**2+3*x-2)")
                else:
                    st.error(f"❌ Помилка у функції {i+1}: {msg}")
                error_cnt += 1

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
    st.caption("© Шаблінський, 2 курс  graphplot 2026")

if __name__ == "__main__":
    main()
