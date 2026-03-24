import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Заголовок програми
    st.title("GraphPlot – Візуалізація математичних функцій")

    # Поле для введення функції
    st.subheader("Введення функції")
    st.write("У це поле потрібно вводити математичний вираз, використовуючи синтаксис Python.")
    st.write("Приклади правильного вводу:")
    st.write("- sin(x)")
    st.write("- x**2")
    st.write("- exp(x)")
    st.write("Де `x` – змінна, яку програма буде використовувати для побудови графіка.")

    func_input = st.text_input("Функція:", "sin(x)")

    # Межі графіка
    st.subheader("Межі графіка")
    x_min = st.number_input("Мінімальне значення X", value=-10)
    x_max = st.number_input("Максимальне значення X", value=10)

    # Кнопка побудови
    if st.button("Побудувати графік"):
        try:
            x = np.linspace(x_min, x_max, 400)
            # Обчислення функції
            y = [eval(func_input, {"x": val, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp}) for val in x]

            fig, ax = plt.subplots()
            ax.plot(x, y, color="darkblue", linewidth=2)  # кольоровий графік
            ax.set_title(f"Графік функції: {func_input}", fontsize=14, color="darkred")
            ax.grid(True, linestyle="--", alpha=0.7)  # сітка для краси
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Помилка: {e}")

    # Інформація про програму внизу
    st.markdown("---")
    st.write("**Версія:** v1.0")
    st.write("**Розробник:** Шаблінський, 2 курс")

if __name__ == "__main__":
    main()
