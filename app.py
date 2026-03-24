import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from io import BytesIO

# Кастомний фон через CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f0f8ff 0%, #e6e6fa 60%, #fff0f5 100%);
}
h1 {font-family: 'Arial Black', sans-serif; color: #121262;}
</style>
""", unsafe_allow_html=True)

# --- Головна програма ---
def main():
    st.markdown("<h1 style='text-align:center;'>GraphPlot – Професійна візуалізація функцій</h1>", unsafe_allow_html=True)
    st.info(
        "Додавайте **одну або кілька** математичних функцій для побудови графіків. "
        "Підтримуються `sin`, `cos`, `tan`, `exp`, `ln`, `sqrt`, `abs`, `log`, тощо.<br>"
        "Приклади: `sin(x)`, `x**2+3*x-2`, `exp(-x)*cos(x)`",
        icon="ℹ️"
    )

    # Ввід функцій
    st.subheader("🔢 Введіть функції через кому")
    func_input = st.text_input("Функції:", "sin(x), exp(-x)*cos(x)")
    latex_show = st.checkbox("Показати формули у LaTeX", value=True)

    # Межі графіка
    st.subheader("📐 Межі графіка")
    c1, c2 = st.columns(2)
    x_min = c1.number_input("Мінімальне X", value=-10.0)
    x_max = c2.number_input("Максимальне X", value=10.0)
    num_points = st.slider("Кількість точок", 100, 2000, 400)

    # Візуальні налаштування
    st.subheader("🎨 Налаштування стилю")
    fill_area = st.checkbox("Зафарбувати область під першою функцією", value=False)
    show_derivative = st.checkbox("Додати графік похідної першої функції", value=False)
    download_graph = st.checkbox("Дати можливість зберегти графік", value=True)

    # Підказки для прикладів
    with st.expander("ℹ️ Натисніть, щоб побачити приклади функцій"):
        st.code("1/x\nsqrt(x)\nexp(-x)*cos(x)\nabs(x)\nsin(x)+sin(2*x)\nlog(x, 10)  # логарифм за основою 10", language="python")

    # Побудова
    if st.button("Побудувати графік 🚀"):
        x = sp.symbols('x')
        xx = np.linspace(x_min, x_max, num_points)
        fig, ax = plt.subplots(figsize=(8,5))
        colors = ["#d7263d", "#305aa5", "#198c2e", "#8338ec", "#ff9700", "#808000", "#1e656d"]
        error_cnt = 0

        # Розбір функцій
        functions = [f.strip() for f in func_input.split(",") if f.strip()]
        for i, fstr in enumerate(functions):
            try:
                # Безпечний розбір виразу!
                expr = sp.sympify(fstr, locals={'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'exp':sp.exp,'log':sp.log,'sqrt':sp.sqrt,'abs':sp.Abs,'ln':sp.ln})
                f_lambd = sp.lambdify(x, expr, 'numpy')
                y = f_lambd(xx)

                # LaTeX вивід
                if latex_show:
                    st.latex(f"f_{i+1}(x) = {sp.latex(expr)}")
                # Графік функції
                label = f"f{i+1}(x) = {fstr}"
                ax.plot(xx, y, color=colors[i%len(colors)], lw=2, label=label)
                # Площа під графіком (для першої функції)
                if i==0 and fill_area:
                    ax.fill_between(xx, y, color=colors[0], alpha=0.15)

                # Похідна для першої функції
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
        ax.set_title("Графік(-и) функцій", fontsize=15)
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
        # Підказка про успіх
        if error_cnt==0:
            st.success("Графік(и) побудовано успішно!")

    st.markdown("---")
    st.info(
        "**Версія:** v2.0<br>"
        "**Розробник:** Шаблінський, 2 курс"
        "<br>**Бібліотеки:** sympy, numpy, matplotlib, streamlit", 
        icon="🎓"
    )

if __name__ == "__main__":
    main()
