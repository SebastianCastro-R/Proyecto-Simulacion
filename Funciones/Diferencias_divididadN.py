import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def diferencias_divididas_sucesion(x, y):
    n = len(x)
    tabla = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        tabla[i][0] = y[i]
    for j in range(1, n):
        for i in range(n - j):
            tabla[i][j] = (tabla[i+1][j-1] - tabla[i][j-1]) / (x[i+j] - x[i])
    coeficientes = [tabla[0][j] for j in range(n)]
    return coeficientes, tabla

def construir_polinomio(coeficientes, x_vals):
    x = sp.Symbol('n')  # usamos "n" como variable de secuencia
    polinomio = coeficientes[0]
    producto = 1
    for i in range(1, len(coeficientes)):
        producto *= (x - x_vals[i - 1])
        polinomio += coeficientes[i] * producto
    return sp.simplify(polinomio)

def mostrar_tabla(tabla):
    print("\n Tabla de Diferencias Divididas:")
    for fila in tabla:
        fila_mostrada = [f"{elem:.6f}" if isinstance(elem, float) else str(elem) for elem in fila if elem != 0]
        print(fila_mostrada)

def Menu_diferencias_Divididas():
    print("\n====== Descubrir fórmula de una secuencia con Diferencias divididas de Newton ======")
    
    secuencia_input = input("Ingresa los términos de la secuencia separados por comas (por ejemplo: 1, 3*2, 5**2, 7/2): ")
    
    try:
        y_vals = list(map(lambda s: eval(s.strip()), secuencia_input.split(',')))
    except Exception as e:
        print(f" Error al evaluar las expresiones: {e}")
        return
    
    n_vals = list(range(1, len(y_vals) + 1))  # n empieza en 1

    coef, tabla = diferencias_divididas_sucesion(n_vals, y_vals)
    mostrar_tabla(tabla)

    polinomio = construir_polinomio(coef, n_vals)

    print("\n Polinomio que representa la secuencia:")
    print("Forma expandida:   S(n) =", sp.expand(polinomio))
    print("Forma factorizada: S(n) =", sp.factor(polinomio))

    try:
        n_eval = float(input("\n¿Deseas evaluar S(n)? Ingresa un valor de n (o deja vacío para omitir): ") or "nan")
        if not np.isnan(n_eval):
            f = sp.lambdify(sp.Symbol('n'), polinomio, modules=['numpy'])
            print(f"S({n_eval}) = {f(n_eval)}")
    except:
        pass

    mostrar = input("¿Deseas ver la gráfica de la secuencia? (s/n): ").strip().lower()
    if mostrar == 's':
        x_plot = np.linspace(min(n_vals), max(n_vals) + 2, 300)
        f = sp.lambdify(sp.Symbol('n'), polinomio, modules=['numpy'])
        y_plot = f(x_plot)

        plt.plot(x_plot, y_plot, label="Polinomio interpolante")
        plt.scatter(n_vals, y_vals, color="red", label="Términos dados")
        plt.title("Interpolación de Newton - Sucesión")
        plt.xlabel("n")
        plt.ylabel("S(n)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


    

