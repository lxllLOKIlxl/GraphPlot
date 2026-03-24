import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Додаємо кастомний фон через CSS
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f0f8ff, #e6e6fa, #fff0f5);
}
h1 {
    font-family: 'Arial Black', sans-serif;
    color: #8B0000;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

def main():
    # Заголовок програми
    st.markdown("<h1 style='text-align: center;'>GraphPlot – Візуалізація математичних функцій</h1>", unsafe_allow_html=True)

    # Опис програми
    st.info("Ця програма дозволяє вводити одну або кілька математичних функцій та будувати їх графіки у заданих межах.")

    # Поле для введення функцій
    st.subheader("🔢 Введення функцій")
    st.write("У це поле потрібно вводити математичні вирази через кому. "
             "Наприклад: `sin(x), cos(x), x**2`")
    st.write("Де `x` – змінна, яку програма буде використовувати для побудови графіка.")
    func_input = st.text_input("Функції:", "sin(x), cos(x)")

    # Межі графіка
    st.subheader("📐 Межі графіка")
    x_min = st.number_input("Мінімальне значення X", value=-10)
    x_max = st.number_input("Максимальне значення X", value=10)

    # Кнопка побудови
    if st.button("🎨 Побудувати графік"):
        try:
            x = np.linspace(x_min, x_max, 400)
            fig, ax = plt.subplots()

            # Розділяємо функції по комах
            functions = [f.strip() for f in func_input.split(",")]

            colors = ["crimson", "darkblue", "darkgreen", "purple", "orange"]
            for i, f in enumerate(functions):
                y = [eval(f, {"x": val, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp}) for val in x]
                ax.plot(x, y, color=colors[i % len(colors)], linewidth=2, label=f)

            ax.set_title("Графіки функцій", fontsize=14, color="darkred")
            ax.set_xlabel("X", fontsize=12, color="navy")
            ax.set_ylabel("Y", fontsize=12, color="navy")
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.7)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Помилка: {e}")

    # Інформація про програму внизу
    st.markdown("---")
    st.success("**Версія:** v1.1  \n**Розробник:** Шаблінський, 2 курс")

if __name__ == "__main__":
    main()
