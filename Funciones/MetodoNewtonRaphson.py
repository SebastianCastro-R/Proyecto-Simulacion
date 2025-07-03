# MetodoNewtonRaphson.py
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import sympy as sym

def convertir_funcion(funcion_str):
    x = sym.symbols('x')
    fx_expr = sym.sympify(funcion_str)
    f = sym.lambdify(x, fx_expr, modules=["numpy"])
    df_expr = sym.diff(fx_expr, x)
    df = sym.lambdify(x, df_expr, modules=["numpy"])
    return f, df, fx_expr

def NewtonRaphson(f, df, x1, es, imax):
    x = x1
    xv = []
    ea = 2 * es
    i = 0
    Newton_table = []

    # Primera fila (sin error todavía)
    Newton_table.append([i, x, df(x), f(x), None, None])
    xv.append(x)

    while ea > es and i < imax:
        x = x - f(x) / df(x)
        xv.append(x)
        i += 1

        if x != 0:
            ea = abs(xv[i] - xv[i - 1])
            er = abs((xv[i] - xv[i - 1]) / xv[i]) * 100
        else:
            ea = None
            er = None

        Newton_table.append([i, x, df(x), f(x), ea, er])

    # Impresión opcional (consola)
    print("\nMétodo Newton-Raphson")
    print(tabulate(
        [[i, x, dx, fx, f"{ea:.6f}" if ea else "--", f"{er:.6f}" if er else "--"]
         for i, x, dx, fx, ea, er in Newton_table],
        headers=["Iteración", "x", "f'(x)", "f(x)", "e abs", "er (%)"]
    ))

    return x, f(x), Newton_table

def graficar_newton_raphson(f, xr, yr, a, b, n, fx_expr):
    x_vals = np.linspace(a, b, n)
    y_vals = f(x_vals)

    plt.figure(figsize=(10, 8))
    plt.plot(x_vals, y_vals, label=f"f(x) = {fx_expr}")
    plt.axhline(0, color='k', linestyle='--', label="y = 0")
    plt.plot(xr, yr, 'ro', label="Raíz (Newton)")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Gráfica de f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()
