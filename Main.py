from PolinomioTaylor import *
from MetodoNewtonRaphson import *
from langrage import *
import sympy as sym
import Binarios
from Biseccion import *
from minimos_cuadrados import *
from diferencias_finitas import *
import sys

def mostrar_menu():
    print("\n" + "="*50)
    print("       SIMULACIÓN Y COMPUTACIÓN NUMÉRICA")
    print("="*50)
    print("¿Cómo deseas ejecutar el programa?")
    print("  1. Interfaz Gráfica (GUI)")
    print("  2. Terminal (Modo Consola)")
    print("  3. Salir")
    print("="*50)

def ejecutar_gui():
    try:
        from GUI import root
        root.mainloop()
    except Exception as e:
        print(f"\n❌ Error al iniciar la interfaz gráfica: {e}")

def ejecutar_terminal():
    print("\n" + "="*50)
    print("   MÉTODOS DISPONIBLES EN MODO TERMINAL")
    print("="*50)
    print("  1. Método de Taylor")
    print("  2. Método de Newton-Raphson")
    print("  3. Método de Lagrange")
    print("  4. Operaciones Binarias")
    print("  5. Método de Bisección")
    print("  6. Diferencias Finitas")
    print("  7. Mínimos Cuadrados")
    print("  0. Volver al menú principal")
    print("="*50)

    while True:
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            from PolinomioTaylor import politaylor, mostrar_polinomio, calcular_error_real, cota_error_maximo, buscar_grado_para_error, graficar
            # Aquí puedes pedir inputs manuales y usar las funciones
            print("🔧 Este módulo está diseñado principalmente para la GUI.")
        elif opcion == '2':
            from MetodoNewtonRaphson import convertir_funcion, NewtonRaphson, graficar_newton_raphson
            fx_str = input("Ingrese la función f(x): ")
            x0 = float(input("Ingrese el valor inicial: "))
            tol = float(input("Ingrese la tolerancia: "))
            imax = int(input("Ingrese el número máximo de iteraciones: "))
            f, df, fx_expr = convertir_funcion(fx_str)
            xr, yr = NewtonRaphson(f, df, x0, tol, imax)
            graficar_newton_raphson(f, xr, yr, x0-5, x0+5, 100, fx_expr)
        elif opcion == '3':
            
            f, g, puntos = lagrange()
            if puntos:
                graficar_lagrange(f, g, puntos)
        elif opcion == '4':
            import Binarios as bin
            print("Opciones:")
            print("  1. Decimal a Binario")
            print("  2. Binario a Decimal")
            print("  3. Sumar binarios")
            print("  4. Restar binarios")
            print("  5. Multiplicar binarios")
            print("  6. Dividir binarios")
            subop = input("Elige una opción: ")
            if subop == '1':
                n = int(input("Ingrese un número decimal: "))
                print(f"Binario: {bin.decimal_a_binario(n)}")
            elif subop == '2':
                b = input("Ingrese un número binario: ")
                print(f"Decimal: {bin.binario_a_decimal(b)}")
            elif subop in ['3', '4', '5', '6']:
                b1 = input("Ingrese binario 1: ")
                b2 = input("Ingrese binario 2: ")
                if subop == '3':
                    print(f"Resultado: {bin.sumar_binarios(b1, b2)}")
                elif subop == '4':
                    print(f"Resultado: {bin.restar_binarios(b1, b2)}")
                elif subop == '5':
                    print(f"Resultado: {bin.multiplicar_binarios(b1, b2)}")
                elif subop == '6':
                    print(f"Resultado: {bin.dividir_binarios(b1, b2)}")
        elif opcion == '5':
            from Biseccion import metodo_biseccion, graficar_biseccion
            f = input("Ingrese la función f(x): ")
            a = float(input("Ingrese el valor a: "))
            b = float(input("Ingrese el valor b: "))
            crit = float(input("Ingrese la tolerancia: "))
            xr, tabla = metodo_biseccion(f, a, b, crit)
            if xr is not None:
                graficar_biseccion(f, xr)
        elif opcion == '6':
            
            diferencias_finitas_edo2()
        elif opcion == '7':
            from minimos_cuadrados import menu_minimos_cuadrados
            menu_minimos_cuadrados()
        elif opcion == '0':
            break
        else:
            print("⚠️ Opción no válida.")

if __name__ == '__main__':
    while True:
        mostrar_menu()
        eleccion = input("Seleccione una opción (1-3): ").strip()
        if eleccion == '1':
            ejecutar_gui()
            break
        elif eleccion == '2':
            ejecutar_terminal()
        elif eleccion == '3':
            print("¡Hasta luego!")
            sys.exit()
        else:
            print("❌ Opción no válida. Intenta de nuevo.")
