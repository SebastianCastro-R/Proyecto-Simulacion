
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import math

def interpolacion_lagrange():
    def lagrange_simbolico(xi, fi):
        x = sp.Symbol('x')
        n = len(xi)
        polinomio = 0

        for i in range(n):
            termino = 1
            for j in range(n):
                if i != j:
                    termino *= (x - xi[j]) / (xi[i] - xi[j])
            polinomio += termino * fi[i]

        return sp.simplify(polinomio), polinomio.expand()

    def calcular_cota_error(xi, grado, x_eval, derivada_max):
        producto = 1
        for xi_i in xi:
            producto *= abs(x_eval - xi_i)
        factorial = math.factorial(grado + 1)
        error = (derivada_max / factorial) * producto
        return error

    def mostrar_menu():
        print("\nElige una opción:")
        print("1. Mostrar polinomio de Lagrange (forma simbólica)")
        print("2. Mostrar gráfica")
        print("3. Mostrar cota máxima del error")
        print("4. Salir")

    def graficar_polinomio(poli_simplificado, xi, fi):
        x = sp.Symbol('x')
        f = sp.lambdify(x, poli_simplificado, modules=['numpy'])

        x_vals = np.linspace(min(xi) - 2, max(xi) + 2, 500)
        y_vals = f(x_vals)

        plt.plot(x_vals, y_vals, label="Polinomio interpolado")
        plt.scatter(xi, fi, color='red', label="Puntos")
        plt.title("Interpolación de Lagrange")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.legend()
        plt.show()

    def pedir_puntos():
        print("Introduce los valores de xi separados por comas (ejemplo: 6,10,13):")
        xi = list(map(float, input("xi: ").split(',')))

        print("Introduce los valores de fi separados por comas (ejemplo: 6.67,15.11,18.89):")
        fi = list(map(float, input("fi: ").split(',')))

        if len(xi) != len(fi):
            print("Error: la cantidad de valores xi y fi debe coincidir.")
            exit()

        return np.array(xi), np.array(fi)

    print("\n================= Interpolación de Lagrange ======================")
    xi, fi = pedir_puntos()
    poli_simb, poli_simplificado = lagrange_simbolico(xi, fi)

    while True:
        mostrar_menu()
        opcion = input("Opción: ")

        if opcion == "1":
            print("\nPolinomio de Lagrange (forma simbólica):")
            print(str(poli_simplificado).replace("**", "^"))
        elif opcion == "2":
            graficar_polinomio(poli_simplificado, xi, fi)
        elif opcion == "3":
            try:
                x_eval = float(input("Ingresa el valor de x donde quieres estimar el error: "))
                derivada_max = input("Ingresa una cota estimada de la derivada de orden n+1 (por defecto usa 0.1): ")
                derivada_max = float(derivada_max) if derivada_max else 0.1
                grado = len(xi) - 1
                error = calcular_cota_error(xi, grado, x_eval, derivada_max)
                print(f"Cota máxima del error en x = {x_eval}: {error:.6f}")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == "4":
            print("Hasta luego")
            break
        else:
            print("Opción inválida, intenta de nuevo.")


