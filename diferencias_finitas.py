import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import re

x = sym.Symbol('x')
y = sym.Function('y')

def diferencias_finitas_edo2():
    print("\n--- MÉTODO DE DIFERENCIAS FINITAS PARA EDO DE SEGUNDO ORDEN ---")
    print("Ingrese la ecuación en forma: y'' = expresión (por ejemplo: y' + 2*y + cos(x))")

    # Entrada de datos
    f_expr_str = input("Ingrese el lado derecho de la ecuación (sin y'' = ): ")

    # Reemplazar notaciones comunes para sympy
    f_expr_str = f_expr_str.replace("y'", "Derivative(y(x), x)")  # y' → Derivada
    f_expr_str = re.sub(r'(?<![\w_])y(?!\()', 'y(x)', f_expr_str)  # y → y(x), solo si no es y(...)

    try:
        f_expr = sym.sympify(f_expr_str)
    except Exception as e:
        print("\n❌ Error al interpretar la expresión:", e)
        return

    a = float(sym.sympify(input("Ingrese el extremo izquierdo del intervalo (a): ")))
    b = float(sym.sympify(input("Ingrese el extremo derecho del intervalo (b): ")))
    h = float(sym.sympify(input("Ingrese el valor del paso h: ")))
    alpha = float(sym.sympify(input(f"Ingrese la condición y({a}) = ")))
    beta = float(sym.sympify(input(f"Ingrese la condición y({b}) = ")))

    # Número de puntos internos
    n = int((b - a) / h) - 1
    xi = np.linspace(a + h, b - h, n)

    # Variables para sustituciones simbólicas
    yi = sym.symbols(f'y1:{n+1}')  # y1, y2, ..., yn

    eqs = []
    for i in range(n):
        y_i = yi[i]
        y_i_m1 = alpha if i == 0 else yi[i-1]
        y_i_p1 = beta if i == n-1 else yi[i+1]

        y_p = (y_i_p1 - y_i_m1)/(2*h)  # Aproximación y'
        y_val = y_i                  # y_i
        x_val = xi[i]               # x_i

        f_eval = f_expr.subs({y(x): y_val, sym.Derivative(y(x), x): y_p, x: x_val})
        lhs = (y_i_p1 - 2*y_i + y_i_m1) / h**2
        eq = lhs - f_eval
        eqs.append(eq)

    # Sistema lineal
    sol = sym.linsolve(eqs, yi)
    solucion = list(sol)[0]

    # Construir solución completa
    x_all = np.concatenate(([a], xi, [b]))
    y_all = np.concatenate(([alpha], [float(s) for s in solucion], [beta]))

    print("\n--- Solución Aproximada ---")
    for xi_, yi_ in zip(x_all, y_all):
        print(f"y({xi_:.4f}) ≈ {yi_:.6f}")

    # ¿Comparar con solución exacta?
    ver_exacta = input("\n¿Desea comparar con una solución exacta? (s/n): ").lower()
    if ver_exacta == 's':
        exacta_str = input("Ingrese la solución exacta en términos de x (ej: -1/10*(sin(x)+3*cos(x))): ")
        try:
            y_exacta = sym.sympify(exacta_str)
            f_exacta = sym.lambdify(x, y_exacta, 'numpy')
            x_vals = np.linspace(a, b, 100)
            y_vals = f_exacta(x_vals)

            plt.plot(x_vals, y_vals, label='Solución exacta', color='blue')
            plt.plot(x_all, y_all, 'o--', label='Aproximación', color='red')
            plt.legend()
            plt.grid(True)
            plt.title("Comparación: Aproximación vs Exacta")
            plt.xlabel("x")
            plt.ylabel("y(x)")
            plt.show()
        except Exception as e:
            print("No se pudo graficar la solución exacta:", e)
    else:
        # Solo graficar aproximación
        plt.plot(x_all, y_all, 'o--', label='Aproximación', color='red')
        plt.title("Solución Aproximada por Diferencias Finitas")
        plt.xlabel("x")
        plt.ylabel("y(x)")
        plt.grid(True)
        plt.legend()
        plt.show()



def resolver_dif_finitas_gui(f_expr, a, b, h, alpha, beta):
    import matplotlib.pyplot as plt
    x = sym.Symbol('x')
    y = sym.Function('y')

    n = int((b - a) / h) - 1
    xi = np.linspace(a + h, b - h, n)
    yi = sym.symbols(f'y1:{n+1}')

    eqs = []
    for i in range(n):
        y_i = yi[i]
        y_i_m1 = alpha if i == 0 else yi[i-1]
        y_i_p1 = beta if i == n-1 else yi[i+1]
        y_p = (y_i_p1 - y_i_m1)/(2*h)
        x_val = xi[i]
        f_eval = f_expr.subs({y(x): y_i, sym.Derivative(y(x), x): y_p, x: x_val})
        lhs = (y_i_p1 - 2*y_i + y_i_m1) / h**2
        eqs.append(lhs - f_eval)

    sol = sym.linsolve(eqs, yi)
    solucion = list(sol)[0]

    x_all = np.concatenate(([a], xi, [b]))
    y_all = np.concatenate(([alpha], [float(s) for s in solucion], [beta]))

    print("\n--- Solución Aproximada (GUI) ---")
    for xi_, yi_ in zip(x_all, y_all):
        print(f"y({xi_:.4f}) ≈ {yi_:.6f}")

    plt.plot(x_all, y_all, 'o--', label='Aproximación', color='red')
    plt.title("Solución Aproximada por Diferencias Finitas")
    plt.xlabel("x")
    plt.ylabel("y(x)")
    plt.grid(True)
    plt.legend()
    plt.show()
