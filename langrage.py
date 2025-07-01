import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def lagrange():
    x, y, λ = sp.symbols('x y λ')

    print("Método de Lagrange para encontrar máximos y mínimos")
    print("---------------------------------------------------\n")

    f_expr = input("Ingresa la función objetivo f(x, y), ej: x**2 + y**2: ")
    g_expr = input("Ingresa la restricción g(x, y) = 0, ej: x + y - 1: ")

    try:
        f = sp.sympify(f_expr)
        g = sp.sympify(g_expr)

        df_dx = sp.diff(f, x)
        df_dy = sp.diff(f, y)
        dg_dx = sp.diff(g, x)
        dg_dy = sp.diff(g, y)

        eq1 = sp.Eq(df_dx, λ * dg_dx)
        eq2 = sp.Eq(df_dy, λ * dg_dy)
        eq3 = sp.Eq(g, 0)

        soluciones = sp.solve([eq1, eq2, eq3], (x, y, λ), dict=True)

        puntos_criticos = []
        for sol in soluciones:
            x_val = sol[x]
            y_val = sol[y]
            if x_val.is_real and y_val.is_real:
                puntos_criticos.append((float(x_val), float(y_val)))

        if not puntos_criticos:
            print("\nNo se encontraron puntos críticos reales.")
            return f, g, []
        else:
            valores_f = [f.subs({x: p[0], y: p[1]}).evalf() for p in puntos_criticos]
            maximo = max(valores_f)
            minimo = min(valores_f)

            maximos = [p for p, v in zip(puntos_criticos, valores_f) if v == maximo]
            minimos = [p for p, v in zip(puntos_criticos, valores_f) if v == minimo]

            print("\nResultados:")
            print(f"Valor máximo encontrado: {maximo:.4f}")
            for p in maximos:
                print(f"Máximo en: ({p[0]:.4f}, {p[1]:.4f})")

            print(f"\nValor mínimo encontrado: {minimo:.4f}")
            for p in minimos:
                print(f"Mínimo en: ({p[0]:.4f}, {p[1]:.4f})")

            return f, g, puntos_criticos

    except Exception as e:
        print("\nError:", str(e))
        print("Verifica que las funciones ingresadas sean válidas.")
        return None, None, []


def graficar_lagrange(f, g, puntos_criticos):
    x, y = sp.symbols('x y')
    try:
        f_np = sp.lambdify((x, y), f, 'numpy')
        g_np = sp.lambdify((x, y), g, 'numpy')

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')

        margen = 2
        xs = [p[0] for p in puntos_criticos]
        ys = [p[1] for p in puntos_criticos]
        x_min = min(xs) - margen if xs else -5
        x_max = max(xs) + margen if xs else 5
        y_min = min(ys) - margen if ys else -5
        y_max = max(ys) + margen if ys else 5

        x_grid = np.linspace(x_min, x_max, 50)
        y_grid = np.linspace(y_min, y_max, 50)
        X, Y = np.meshgrid(x_grid, y_grid)
        Z = f_np(X, Y)

        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, edgecolor='none')

        try:
            fig_contour, ax_contour = plt.subplots()
            G = g_np(X, Y)
            contorno = ax_contour.contour(X, Y, G, levels=[0], colors='r')
            plt.close(fig_contour)

            if contorno.allsegs[0]:
                for segmento in contorno.allsegs[0]:
                    x_line = segmento[:, 0]
                    y_line = segmento[:, 1]
                    z_line = f_np(x_line, y_line)
                    ax.plot(x_line, y_line, z_line, 'r-', lw=2, label='Restricción')

        except Exception as e:
            print("\nAdvertencia: No se pudo graficar la restricción completa:", str(e))

        for p in puntos_criticos:
            z_p = f_np(p[0], p[1])
            ax.scatter(p[0], p[1], z_p, color='black', s=100,
                       label='Puntos críticos' if p == puntos_criticos[0] else "")

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('f(x,y)')
        ax.set_title('Superficie de f(x,y) con restricción y puntos críticos')

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())

        plt.show()

    except Exception as e:
        print("\nError al graficar:", str(e))
