import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title("GraphPlot - Function Visualization")

    # Поле для введення функції
    func_input = st.text_input("Введіть функцію (наприклад: sin(x), x**2, exp(x))", "sin(x)")

    # Межі графіка
    x_min = st.number_input("Мінімальне значення X", value=-10)
    x_max = st.number_input("Максимальне значення X", value=10)

    # Кнопка побудови
    if st.button("Побудувати графік"):
        try:
            x = np.linspace(x_min, x_max, 400)
            # Використовуємо eval для обчислення функції
            y = [eval(func_input, {"x": val, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp}) for val in x]

            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.set_title(f"Графік функції: {func_input}")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Помилка: {e}")

if __name__ == "__main__":
    main()
