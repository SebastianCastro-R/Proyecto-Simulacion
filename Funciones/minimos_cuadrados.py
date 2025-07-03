import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
import re

def ajuste_lineal(x, y):
    coef = np.polyfit(x, y, 1)
    p = np.poly1d(coef)
    ecm = np.mean((p(x) - y) ** 2)
    return p, ecm

def ajuste_polinomico(x, y, grado):
    coef = np.polyfit(x, y, grado)
    p = np.poly1d(coef)
    ecm = np.mean((p(x) - y) ** 2)
    return p, ecm

def ajuste_exponencial(x, y):
    y_log = np.log(y)
    coef = np.polyfit(x, y_log, 1)
    a = np.exp(coef[1])
    b = coef[0]
    def modelo(x_val): return a * np.exp(b * x_val)
    ecm = np.mean((modelo(x) - y) ** 2)
    return modelo, ecm, a, b

def ajuste_simbolico_manual(x_data, y_data, modelo_input):
    import numpy as np
    import sympy as sym
    import matplotlib.pyplot as plt

    x = sym.Symbol('x')

    try:
        expr = sym.sympify(modelo_input, locals={'sqrt': sym.sqrt})
    except Exception as e:
        print(f"❌ Error al interpretar la expresión: {e}")
        return "Error", None

    coeficientes = sorted(expr.free_symbols - {x}, key=lambda s: str(s))
    if not coeficientes:
        print("❌ No se detectaron parámetros (como 'a', 'b') en la expresión.")
        return "Sin parámetros detectados", None

    A = []
    for xi in x_data:
        fila = [float(expr.subs({x: xi, c: 1, **{s: 0 for s in coeficientes if s != c}})) for c in coeficientes]
        A.append(fila)

    A = np.array(A)
    y_data = np.array(y_data)

    try:
        AtA = A.T @ A
        Aty = A.T @ y_data
        solucion = np.linalg.solve(AtA, Aty)
    except np.linalg.LinAlgError:
        print("❌ El sistema no tiene solución única.")
        return "Sistema sin solución única", None

    modelo_final = expr
    for c, v in zip(coeficientes, solucion):
        modelo_final = modelo_final.subs(c, v)

    f_lamb = sym.lambdify(x, modelo_final, modules=['numpy'])
    y_aprox = f_lamb(np.array(x_data))
    ecm = np.mean((y_aprox - y_data) ** 2)

    modelo_simplificado = sym.simplify(modelo_final)

    # Imprimir por consola (opcional)
    print("\n✅ Modelo ajustado:")
    print(f"  ➔ y = {modelo_simplificado}")
    print(f"  ➔ Error cuadrático medio (ECM): {ecm:.6e}")

    # Gráfica
    x_vals = np.linspace(min(x_data), max(x_data), 300)
    y_vals = f_lamb(x_vals)

    plt.scatter(x_data, y_data, color='red', label='Datos')
    plt.plot(x_vals, y_vals, color='black', label='Modelo ajustado')
    plt.title('Ajuste por Modelo Simbólico')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Devolver para mostrar en la GUI
    return str(modelo_simplificado), ecm
   
    
def menu_minimos_cuadrados():
    print("\n" + "-" * 50)
    print("         APROXIMACIÓN POR MÍNIMOS CUADRADOS")
    print("-" * 50)
    try:
        n = int(input("Ingrese el número de puntos: "))
        x = []
        y = []
        for i in range(n):
            xi = float(input(f"  ➤ Ingrese x[{i}]: "))
            yi = float(input(f"  ➤ Ingrese y[{i}]: "))
            x.append(xi)
            y.append(yi)
        x = np.array(x)
        y = np.array(y)

        repetir = True
        while repetir:
            print("\n" + "-" * 50)
            print("Seleccione el tipo de ajuste:")
            print("  1. Ajuste Lineal")
            print("  2. Ajuste Polinómico")
            print("  3. Ajuste Exponencial")
            print("  4. Ajuste por Modelo Ingresado Manualmente")
            print("-" * 50)
            opcion = input("Opción: ")

            if opcion == '1':
                p, ecm = ajuste_lineal(x, y)
                print("\n📈 Modelo lineal encontrado:")
                print(f"  ➤ y = {p}")
                print(f"  ➤ Error cuadrático medio (ECM): {ecm:.6e}")
                ver = input("\n¿Desea ver la gráfica? (s/n): ").lower()
                if ver == 's':
                    plt.scatter(x, y, color='red', label='Datos')
                    x_vals = np.linspace(min(x), max(x), 100)
                    plt.plot(x_vals, p(x_vals), color='blue', label='Ajuste Lineal')
                    plt.title('Ajuste Lineal por Mínimos Cuadrados')
                    plt.xlabel('x')
                    plt.ylabel('y')
                    plt.legend()
                    plt.grid(True)
                    plt.show()

            elif opcion == '2':
                grado = int(input("Ingrese el grado del polinomio: "))
                p, ecm = ajuste_polinomico(x, y, grado)
                print(f"\n📈 Modelo polinómico (grado {grado}) encontrado:")
                print(f"  ➤ y = {p}")
                print(f"  ➤ Error cuadrático medio (ECM): {ecm:.6e}")
                ver = input("\n¿Desea ver la gráfica? (s/n): ").lower()
                if ver == 's':
                    plt.scatter(x, y, color='red', label='Datos')
                    x_vals = np.linspace(min(x), max(x), 100)
                    plt.plot(x_vals, p(x_vals), color='purple', label='Ajuste Polinómico')
                    plt.title('Ajuste Polinómico por Mínimos Cuadrados')
                    plt.xlabel('x')
                    plt.ylabel('y')
                    plt.legend()
                    plt.grid(True)
                    plt.show()

            elif opcion == '3':
                modelo, ecm, a, b = ajuste_exponencial(x, y)
                print(f"\n📈 Modelo exponencial encontrado:")
                print(f"  ➤ y = {a:.4f} * e^({b:.4f} * x)")
                print(f"  ➤ Error cuadrático medio (ECM): {ecm:.6e}")
                ver = input("\n¿Desea ver la gráfica? (s/n): ").lower()
                if ver == 's':
                    plt.scatter(x, y, color='red', label='Datos')
                    x_vals = np.linspace(min(x), max(x), 100)
                    y_vals = [modelo(xi) for xi in x_vals]
                    plt.plot(x_vals, y_vals, color='green', label='Ajuste Exponencial')
                    plt.title('Ajuste Exponencial por Mínimos Cuadrados')
                    plt.xlabel('x')
                    plt.ylabel('y')
                    plt.legend()
                    plt.grid(True)
                    plt.show()

            elif opcion == '4':
                modelo_input = input("Ingrese el modelo simbólico (por ejemplo, a*x + b): ")
                ajuste_simbolico_manual(x, y, modelo_input)


            else:
                print("⚠️  Opción inválida. Intente nuevamente.")

            otra = input("\n¿Desea realizar otro ajuste con los mismos datos? (s/n): ").lower()
            repetir = (otra == 's')

    except Exception as e:
        print(f"\n❌ Ha ocurrido un error: {e}")
