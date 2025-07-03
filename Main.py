from Funciones.PolinomioTaylor import *
from Funciones.MetodoNewtonRaphson import *
import sympy as sym
import Funciones.Binarios as Binarios
from Funciones.Biseccion import *
from Funciones.minimos_cuadrados import *
from Funciones.diferencias_finitas import *
from Funciones.Diferencias_divididadN import *
from Funciones.Interpolacion_Lagrange import *
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
    while True:
        print("----------------------------------------------")
        print("---------------- MENÚ PRINCIPAL --------------")
        print("----------------------------------------------")
        print("1. Método de Taylor")
        print("2. Método de Newton-Raphson")
        print("3. Método de Lagrange")
        print("4. Operaciones con números binarios")
        print("5. Método de Bisección")
        print("6. Diferencias Finitas (EDO 2º Orden)")
        print("7. Mínimos Cuadrados")
        print("8. Interpolacion: Direfencias divididas de Newton")
        print("9. Interpolacion: Método Lagrange")
        print("0. Salir")
        print("----------------------------------------------")
        opcion = input("Seleccione una opción: ")
        print("----------------------------------------------")
        
        if opcion == '1':
            fx_input = input("Ingrese la función f(x): ")
            x0_input = input("Ingrese el valor de x0 (punto de referencia): ")
            xi_input = input("Ingrese el valor de xi (donde se evalúa la aproximación): ")
            try:
                fx = sym.sympify(fx_input)
                x0 = float(sym.sympify(x0_input))
                xi = float(sym.sympify(xi_input))
                n = int(input("Ingrese el grado del polinomio de Taylor (entero): "))
                submenu_taylor(fx, x0, xi, n)
            except Exception as e:
                print("Error en los datos:", e)
        elif opcion == '2':
            print("\n--- Parámetros para el método de Newton-Raphson ---")
            try:
                funcion_str = input("Ingrese la función f(x): ")
                f, df, fx_expr = convertir_funcion(funcion_str)

                a = float(input("Ingresa el valor inicial del rango de x (a): ") or -1)
                b = float(input("Ingresa el valor final del rango de x (b): ") or 10)
                n = int(input("Ingresa la cantidad de puntos para graficar (n): ") or 50)

                emax = float(input("Ingresa el error máximo permitido: ") or 0.001)
                itermax = int(input("Ingresa el número máximo de iteraciones: ") or 20)
                x1 = float(input("Ingresa el valor inicial x1 para Newton-Raphson: ") or 0)

                xr, yr = NewtonRaphson(f, df, x1, emax, itermax)

                ver_grafica = input("¿Deseas ver la gráfica? (s/n): ").lower()
                if ver_grafica == 's':
                    graficar_newton_raphson(f, xr, yr, a, b, n, fx_expr)

            except Exception as e:
                print("Error en los datos ingresados:", e)
        elif opcion == '3':
            try:
                import LANGRAGE_POLINOMIO_TAYLOR as lagr
                from importlib import reload
                reload(lagr)
                lagr.main()  # o el nombre de tu función principal en ese archivo
            except Exception as e:
                print("Ocurrió un error al ejecutar el método de Lagrange:", e)


        elif opcion == '4':
            while True:
                print("----------------------------------------------")
                print("------ OPERACIONES CON NÚMEROS BINARIOS ------")
                print("----------------------------------------------")
                print("1. Decimal a Binario")
                print("2. Binario a Decimal")
                print("3. Sumar Binarios")
                print("4. Restar Binarios")
                print("5. Multiplicar Binarios")
                print("6. Dividir Binarios")
                print("7. Volver al menú principal")
                print("----------------------------------------------")
                opcion_bin = input("Selecciona una opción: ")
                print("----------------------------------------------")

                if opcion_bin == '1':
                    dec = int(input("Ingrese un número decimal: "))
                    print("Binario:", Binarios.decimal_a_binario(dec))
                elif opcion_bin == '2':
                    binario = input("Ingrese un número binario: ")
                    print("Decimal:", Binarios.binario_a_decimal(binario))
                elif opcion_bin == '3':
                    b1 = input("Primer binario: ")
                    b2 = input("Segundo binario: ")
                    print("Suma:", Binarios.sumar_binarios(b1, b2))
                elif opcion_bin == '4':
                    b1 = input("Minuendo binario: ")
                    b2 = input("Sustraendo binario: ")
                    print("Resta:", Binarios.restar_binarios(b1, b2))
                elif opcion_bin == '5':
                    b1 = input("Primer binario: ")
                    b2 = input("Segundo binario: ")
                    print("Producto:", Binarios.multiplicar_binarios(b1, b2))
                elif opcion_bin == '6':
                    b1 = input("Dividendo binario: ")
                    b2 = input("Divisor binario: ")
                    print("Cociente:", Binarios.dividir_binarios(b1, b2))
                elif opcion_bin == '7':
                    break
                else:
                    print("Opción inválida.")
        elif opcion == '5':
            print("\n--- MÉTODO DE BISECCIÓN ---")
            from Funciones.Biseccion import metodo_biseccion, graficar_biseccion
            try:
                f = input("Ingrese la función f(x): ")
                a = float(input("Ingrese el valor a (inicio del intervalo): "))
                b = float(input("Ingrese el valor b (fin del intervalo): "))
                crit = float(input("Ingrese la tolerancia (error aceptado): "))
                xr, tabla = metodo_biseccion(f, a, b, crit)
                if xr is not None:
                    graficar_biseccion(f, xr)
            except Exception as e:
                print("❌ Error:", e)

        elif opcion == '6':
            print("\n--- DIFERENCIAS FINITAS PARA EDO 2º ORDEN ---")
            diferencias_finitas_edo2()

        elif opcion == '7':
            print("\n--- MÉTODO DE MÍNIMOS CUADRADOS ---")
            from Funciones.minimos_cuadrados import menu_minimos_cuadrados
            menu_minimos_cuadrados()
        elif opcion ==  '8':
            Menu_diferencias_Divididas()
        elif opcion ==  '9':
            interpolacion_lagrange()
        elif opcion == '0':
            print("Saliendo del programa...")
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
