import math
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt

def mostrar_polinomio(polinomio, x):
    poli = sym.expand(polinomio)
    terminos = poli.as_ordered_terms()
    partes = []

    for termino in terminos:
        coef, exp = termino.as_coeff_exponent(x)
        coef = sym.nsimplify(coef)

        # Omitir coeficiente 1 salvo en términos independientes
        if exp == 0:
            parte = f"{coef}"
        elif coef == 1:
            parte = f"x" if exp == 1 else f"x**{exp}"
        elif coef == -1:
            parte = f"-x" if exp == 1 else f"-x**{exp}"
        else:
            parte = f"{coef}*x" if exp == 1 else f"{coef}*x**{exp}"
        
        partes.append(parte)

    # Armar el string con signos correctos
    resultado = partes[0]
    for parte in partes[1:]:
        if parte.startswith('-'):
            resultado += f" - {parte[1:]}"
        else:
            resultado += f" + {parte}"

    return "p(x) = " + resultado


x = sym.Symbol('x')  # Variable global para expresiones simbólicas

def politaylor(fx, x0, n):
    """Calcula el polinomio de Taylor de orden n para fx en x0"""
    polinomio = 0
    for k in range(n + 1):
        derivada = fx.diff(x, k)
        derivadax0 = derivada.subs(x, x0)
        termino = (derivadax0 / math.factorial(k)) * (x - x0) ** k
        polinomio += termino
    return polinomio


def calcular_error_real(fx, polinomio, xi):
    fxi = fx.subs(x, xi)
    pxi = polinomio.subs(x, xi)
    error = fxi - pxi
    return float(fxi), float(pxi), float(error)

def cota_error_maximo(fx, x0, xi, n):
    derivada_n1 = fx.diff(x, n+1)
    f_lamb = sym.lambdify(x, derivada_n1, 'numpy')
    puntos = np.linspace(min(x0, xi), max(x0, xi), 100)
    valores = np.abs(f_lamb(puntos))
    M = np.max(valores)
    error_max = (M * abs(xi - x0) ** (n+1)) / math.factorial(n+1)
    return float(error_max)

def buscar_grado_para_error(fx, x0, xi, error_max_permitido, max_grado=100):
    for n in range(max_grado + 1):
        try:
            cota = cota_error_maximo(fx, x0, xi, n)
            if cota < error_max_permitido:
                return n, cota
        except Exception as e:
            print(f"Error al calcular la derivada de orden {n+1}: {e}")
            break
    print(f"No se encontró un grado que cumpla el error menor a {error_max_permitido} en {max_grado} iteraciones.")
    return None, None

def graficar(fx, polinomio, x0, xi):
    """Grafica la función original y su aproximación de Taylor"""
    a = x0
    b = x0 + 3 * xi
    muestras = 51

    fxn = sym.lambdify(x, fx, 'numpy')
    pxn = sym.lambdify(x, polinomio, 'numpy')

    xin = np.linspace(a, b, muestras)
    fxni = fxn(xin)
    pxni = pxn(xin)

    plt.plot(xin, fxni, label='f(x)', color='blue')
    plt.plot(xin, pxni, label='p(x)', color='red', linestyle='--')
    plt.fill_between(xin, pxni, fxni, color='yellow', alpha=0.3)
    plt.axvline(x0, color='green', linestyle=':')
    plt.title('Polinomio de Taylor: f(x) vs p(x)')
    plt.xlabel('x')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    
def submenu_taylor(fx, x0, xi, n):
    polinomio = politaylor(fx, x0, n)

    while True:
        print("----------------------------------------------")
        print("------------ POLINOMIO DE TAYLOR -------------")
        print("----------------------------------------------")
        print("¿Que quieres hacer con estos datos? ")
        print("1. Mostrar el polinomio de Taylor")
        print("2. Calcular el error absoluto |f(xi) - p(xi)|")
        print("3. Calcular la cota máxima del error")
        print("4. Buscar grado mínimo para error específico")
        print("5. Volver al menú principal")
        print("----------------------------------------------")
        opcion = input("Seleccione una opción: ")
        print("----------------------------------------------")

        if opcion == '1':
            print(f"\nPolinomio de Taylor (grado {n}):")
            print(mostrar_polinomio(polinomio, x))
            graficar_opcion = input("\n¿Desea ver la gráfica? (s/n): ").lower()
            if graficar_opcion == 's':
                graficar(fx, polinomio, x0, xi)

        elif opcion == '2':
            real, estimado, error = calcular_error_real(fx, polinomio, xi)
            resultado = polinomio.subs(x, xi)
            print(f"\nAproximación de f({xi}) ≈ p({xi}) = {resultado}")
            print(f"\nEvaluación en {xi}:")
            print(f" f({xi}) real     = {real}")
            print(f" p({xi}) estimado = {estimado}")
            print(f" Error absoluto  |f({xi})-p({xi})|   = {error*-1}")
            
        elif opcion == '3':
            cota = cota_error_maximo(fx, x0, xi, n)
            print(f"\nCota máxima del error: {cota}")

        elif opcion == '4':
            try:
                tolerancia = float(input("Ingrese el error máximo permitido: "))
                grado, cota = buscar_grado_para_error(fx, x0, xi, tolerancia)
                print(f"\nGrado mínimo necesario: {grado} (con cota {cota})")
            except ValueError:
                print("Entrada inválida.")

        elif opcion == '5':
            break

        else:
            print("Opción inválida.")