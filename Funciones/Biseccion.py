# MÉTODO DE BISECCIÓN EN PYTHON

import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols
from sympy import lambdify
from sympy import sympify

def metodo_biseccion(funcion_str, a, b, crit):
    from sympy import symbols, sympify, lambdify

    x = symbols('x')
    fn = sympify(funcion_str)
    f = lambdify(x, fn)

    i = 0
    x_anterior = 0
    ea = None
    tabla = []

    if f(a) * f(b) < 0:
        print("\n{:^60}".format("MÉTODO DE BISECCIÓN"))
        print("{:10} {:^10} {:^10} {:^10} {:^10}".format("i", "a", "b", "xr", "ea(%)"))

        # Primera iteración (i=0)
        xr = (a + b) / 2
        fa = f(a)
        fxr = f(xr)
        
        # Guardar valores ANTES de actualizar a/b
        tabla.append((1, a, b, xr, fxr, "-"))
        
        # Actualizar intervalo
        if fa * fxr < 0:
            b = xr
        else:
            a = xr

        x_anterior = xr
        i = 1

        # Mostrar primera iteración en consola
        print("{:^10} {:^10f} {:^10f} {:^10f} {:^10}".format(1, a, b, xr, "-"))

        # Iteraciones siguientes
        while True:
            xr = (a + b) / 2
            fxr = f(xr)
            fa = f(a)
            ea = abs((xr - x_anterior) / xr)
            error_mostrado = round(ea * 100, 9)

            # Guardar valores ANTES de actualizar a/b
            tabla.append((i+1, a, b, xr, fxr, error_mostrado))
            
            # Actualizar intervalo
            if fa * fxr < 0:
                b = xr
            else:
                a = xr

            x_anterior = xr

            # Mostrar en consola
            print("{:^10} {:^10f} {:^10f} {:^10f} {:^10}".format(
                i+1, a, b, xr, f"{error_mostrado:.6f}"))

            if error_mostrado < crit * 100:
                break

            i += 1

        print(f"\nEl valor de x es {round(xr, 9)} con un error de {round(error_mostrado, 9)}%")
        return xr, tabla
    else:
        print(f"\nLa función no tiene una raíz en el intervalo x = {a} a x = {b}")
        return None, []

def graficar_biseccion(funcion_str, xr=None):
    x = symbols('x')
    fn = sympify(funcion_str)
    f = lambdify(x, fn)

    xpts = np.linspace(-10, 10, 400)
    ypts = f(xpts)

    plt.plot(xpts, ypts, label="f(x)")
    plt.title("Gráfica de la función")
    plt.axhline(color="black")
    plt.axvline(color="black")
    
    if xr is not None:
        plt.scatter(xr, 0, color='red', zorder=5)
        plt.annotate(f"Raíz ≈ {round(xr, 6)}", xy=(xr, 0.5), color='red')

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True, which="both")
    plt.ylim([-15, 15])
    plt.legend()
    plt.show()