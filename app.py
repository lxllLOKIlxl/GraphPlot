import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Заголовок програми
    st.markdown("<h1 style='text-align: center; color: darkblue;'>GraphPlot – Візуалізація математичних функцій</h1>", unsafe_allow_html=True)

    # Опис програми
    st.info("Ця програма дозволяє вводити математичну функцію та будувати її графік у заданих межах.")

    # Поле для введення функції
    st.subheader("🔢 Введення функції")
    st.write("У це поле потрібно вводити математичний вираз, використовуючи синтаксис Python.")
    st.write("Приклади правильного вводу:")
    st.code("sin(x)\nx**2\nexp(x)", language="python")

    func_input = st.text_input("Функція:", "sin(x)")

    # Межі графіка
    st.subheader("📐 Межі графіка")
    x_min = st.number_input("Мінімальне значення X", value=-10)
    x_max = st.number_input("Максимальне значення X", value=10)

    # Кнопка побудови
    if st.button("🎨 Побудувати графік"):
        try:
            x = np.linspace(x_min, x_max, 400)
            # Обчислення функції
            y = [eval(func_input, {"x": val, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp}) for val in x]

            fig, ax = plt.subplots()
            ax.plot(x, y, color="crimson", linewidth=2, label=f"{func_input}")
            ax.set_title(f"Графік функції: {func_input}", fontsize=14, color="darkgreen")
            ax.set_xlabel("X", fontsize=12, color="navy")
            ax.set_ylabel("Y", fontsize=12, color="navy")
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.7)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Помилка: {e}")

    # Інформація про програму внизу
    st.markdown("---")
    st.success("**Версія:** v1.0  \n**Розробник:** Шаблінський, 2 курс")

if __name__ == "__main__":
    main()
