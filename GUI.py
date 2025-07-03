import customtkinter as ctk
from customtkinter import CTkImage

import tkinter as tk
from tkinter import messagebox, simpledialog

import numpy as np
import sympy as sym
from sympy import latex, nsimplify

import matplotlib.pyplot as plt
import matplotlib

from Diferencias_divididadN import diferencias_divididas_sucesion, construir_polinomio
from PolinomioTaylor import politaylor, mostrar_polinomio, calcular_error_real, cota_error_maximo, buscar_grado_para_error, graficar
from diferencias_finitas import *
from PIL import Image

ctk.set_appearance_mode("light")  # o "dark"
ctk.set_default_color_theme("blue")  # o "green", "dark-blue", etc.

#? Colores
AZUL = "#7986CB"   # Azul oscuro
CELESTE = "#4DD0E1"  # Azul claro
ROSA = "#ffc3bd"
ROSA_HOVER = "#ff9f97"
TEXTO = "black"
FUENTE_TEXTO = ("Dongle", 28)
FUENTE_TITULO = ("Chicle", 40)
FUENTE_SUBTITULO = ("Dongle", 40, "bold")
ESPACIO = 15

matplotlib.use("TkAgg")

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

#? Mostrar polinomio en notación bonita
def mostrar_formula_latex(expr, titulo="Resultado"):
    expr = nsimplify(expr)
    latex_str = latex(expr, mode='plain')
    plt.figure(figsize=(6, 1.5))
    plt.axis('off')
    plt.title(titulo, fontsize=14)
    plt.text(0.5, 0.5, f"${latex_str}$", fontsize=22, ha='center', va='center')
    plt.tight_layout()
    plt.show()

def lanzar_taylor():
    root.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Método de Taylor")
    ventana.configure(fg_color="white")
    centrar_ventana(ventana, 1000, 600)
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), root.deiconify()))
    
    # Fondo de imagen
    fondo_img = ctk.CTkImage(Image.open("Images/Wallpaper.png"), size=(1000, 600))
    fondo_label = ctk.CTkLabel(ventana, image=fondo_img, text="")
    fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    fondo_label.lower()
    
    # TÍTULO
    ctk.CTkLabel(ventana, text="Método de Taylor", font=FUENTE_TITULO, fg_color="white", text_color='black').pack(pady=10)

    # CONTENEDOR PRINCIPAL
    contenedor = ctk.CTkFrame(ventana, fg_color="white", corner_radius=15)
    contenedor.pack(pady=5)
    
    # COLUMNA IZQUIERDA (ENTRADAS)
    columna_izquierda = ctk.CTkFrame(contenedor, fg_color="white", corner_radius=15)
    columna_izquierda.pack(side="left", padx=20, expand=True)
    
    ctk.CTkLabel(columna_izquierda, text="Ingrese los Datos:", font=FUENTE_SUBTITULO, fg_color="white", text_color='black').pack(pady=5)

    entradas = {}

    def agregar_campo(texto, clave):
        frame = ctk.CTkFrame(columna_izquierda, fg_color="white", corner_radius=15)
        frame.pack(pady=5)
        ctk.CTkLabel(frame, text=texto, fg_color="white", anchor="w", font=FUENTE_TEXTO, text_color='black').pack()
        entrada = ctk.CTkEntry(frame, width=250, height=40, font=("Dongle Ligth", 16), corner_radius=10)
        entrada.pack()
        entradas[clave] = entrada

    agregar_campo("Función f(x):", "funcion")
    agregar_campo("Grado del polinomio (n):", "n")
    agregar_campo("x0 (punto de expansión):", "x0")
    agregar_campo("xi (punto a evaluar):", "xi")

    # BOTONES Confirmar / Vaciar / Volver
    frame_botones_izq = ctk.CTkFrame(columna_izquierda, fg_color="white", corner_radius=15)
    frame_botones_izq.pack(pady=5)

    def volver():
        ventana.destroy()
        root.deiconify()

    ctk.CTkButton(
        frame_botones_izq,
        text="Confirmar datos",
        command=lambda: procesar_datos(),
        corner_radius=10, width=100, height=30,
        fg_color=AZUL,
        hover_color=CELESTE,
        text_color=TEXTO,
        font=FUENTE_TEXTO
    ).grid(row=0, column=0, padx=10, pady=5)

    ctk.CTkButton(
        frame_botones_izq,
        text="Volver",
        command=volver,
        corner_radius=10, width=100, height=30,
        fg_color=AZUL,
        hover_color=CELESTE,
        text_color=TEXTO,
        font=FUENTE_TEXTO
    ).grid(row=0, column=1, padx=10, pady=5)


    # COLUMNA DERECHA (OPCIONES)
    columna_derecha = ctk.CTkFrame(contenedor, fg_color="white", corner_radius=15)
    columna_derecha.pack(side="right", padx=20, expand=True)

    ctk.CTkLabel(columna_derecha, text="¿Qué deseas hacer?", font=FUENTE_SUBTITULO, fg_color="white", text_color='black').pack(pady=5)

    botones_opciones = []

    def crear_boton_opcion(texto, comando):
        b = ctk.CTkButton(columna_derecha, text=texto, command=comando,font=FUENTE_TEXTO, width=100, height=30, 
                          corner_radius=10, fg_color=AZUL, hover_color=CELESTE, text_color='black')
        botones_opciones.append(b)
        b.pack(pady=5)

    # Este frame se usa para actualizar las funciones al confirmar datos
    def procesar_datos():
        try:
            fx = sym.sympify(entradas["funcion"].get())
            x0_expr = sym.sympify(entradas["x0"].get())
            xi_expr = sym.sympify(entradas["xi"].get())
            n = int(entradas["n"].get())

            # Conversión para funciones que usan float/NumPy
            x0 = float(x0_expr)
            xi = float(xi_expr)
            polinomio = politaylor(fx, x0_expr, n)

            # Actualiza los botones con las funciones correctas
            for b in botones_opciones:
                b.destroy()

            crear_boton_opcion("Mostrar polinomio de Taylor", lambda: (
                mostrar_formula_latex(polinomio, titulo="Polinomio de Taylor"),
                graficar(fx, polinomio, x0, xi) if messagebox.askyesno("Gráfica", "¿Deseas ver la gráfica?") else None
            ))

            crear_boton_opcion("Calcular error absoluto", lambda: (
                lambda r, e, er: messagebox.showinfo("Error Absoluto",
                    f"Aproximación p({xi}) = {e:.6f}\nValor real f({xi}) = {r:.6f}\nError absoluto = {abs(er):.6f}")
                )(*calcular_error_real(fx, polinomio, xi))
            )

            crear_boton_opcion("Calcular cota máxima del error", lambda: (
                messagebox.showinfo("Cota máxima del error", f"{cota_error_maximo(fx, x0, xi, n):.6e}")
            ))

            crear_boton_opcion("Buscar grado para error dado", lambda: (
                lambda t: (
                    (lambda grado, cota: messagebox.showinfo("Resultado", f"Grado requerido: {grado}\nCota estimada: {cota:.6e}")
                    if grado is not None else messagebox.showwarning("No encontrado", "No se encontró un grado con ese error.")
                )(*buscar_grado_para_error(fx, x0, xi, float(t))) if t else None)
            )(simpledialog.askstring("Tolerancia", "Ingrese el error máximo permitido:"))
            )

        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos:\n{e}")

def lanzar_newton():
    root.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Método de Newton-Raphson")
    ventana.configure(fg_color="white")
    centrar_ventana(ventana, 1000, 600)
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), root.deiconify()))

    # Fondo de imagen
    fondo_img = ctk.CTkImage(Image.open("Images/Rosa.png"), size=(1000, 600))
    fondo_label = ctk.CTkLabel(ventana, image=fondo_img, text="")
    fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    fondo_label.lower()

    ctk.CTkLabel(ventana, text="Método de Newton-Raphson", font=FUENTE_TITULO, fg_color="white", text_color='black').pack(pady=15)

    # CONTENEDOR GENERAL
    contenedor = ctk.CTkFrame(ventana, fg_color="white", corner_radius=15)
    contenedor.pack(pady=10)
    contenedor.grid_columnconfigure((0, 1), weight=1)

    # Función para agregar campos
    entradas = {}

    def agregar_entrada(frame, texto, clave):
        f = ctk.CTkFrame(frame, fg_color="white")
        f.pack(pady=10)
        ctk.CTkLabel(f, text=texto, font=FUENTE_TEXTO, text_color="black").pack(anchor="w")
        entrada = ctk.CTkEntry(f, width=200, height=40, font=("Dongle Ligth", 16), corner_radius=10)
        entrada.pack()
        entradas[clave] = entrada

    # Crear dos columnas
    col1 = ctk.CTkFrame(contenedor, fg_color="white")
    col1.grid(row=0, column=0, padx=20, pady=10, sticky="n")

    col2 = ctk.CTkFrame(contenedor, fg_color="white")
    col2.grid(row=0, column=1, padx=20, pady=10, sticky="n")

    # Campos en col1
    agregar_entrada(col1, "Función f(x):", "funcion")
    agregar_entrada(col1, "Valor inicial x1:", "x1")
    agregar_entrada(col1, "Error máximo permitido:", "emax")
    agregar_entrada(col1, "Máx. iteraciones:", "imax")

    # Campos en col2
    agregar_entrada(col2, "Límite inferior a (para gráfica):", "a")
    agregar_entrada(col2, "Límite superior b (para gráfica):", "b")
    agregar_entrada(col2, "Cantidad de puntos (gráfica):", "n")

    # Botones en col2
    def ejecutar_newton():
        try:
            from MetodoNewtonRaphson import convertir_funcion, NewtonRaphson, graficar_newton_raphson
            funcion_str = entradas["funcion"].get()
            f, df, fx_expr = convertir_funcion(funcion_str)

            x1 = float(entradas["x1"].get())
            emax = float(entradas["emax"].get())
            imax = int(entradas["imax"].get())
            a = float(entradas["a"].get())
            b = float(entradas["b"].get())
            n = int(entradas["n"].get())

            xr, yr, tabla = NewtonRaphson(f, df, x1, emax, imax)

            messagebox.showinfo("Resultado",
                f"Raíz aproximada: {xr:.6f}\nf({xr:.6f}) = {yr:.6e}")

            mostrar_tabla_iteraciones(tabla)

            if messagebox.askyesno("Gráfica", "¿Deseas ver la gráfica de f(x)?"):
                graficar_newton_raphson(f, xr, yr, a, b, n, fx_expr)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

    def volver():
        ventana.destroy()
        root.deiconify()

    # Botones
    frame_botones = ctk.CTkFrame(col2, fg_color="white")
    frame_botones.pack(pady=20)

    # Botón Calcular
    ctk.CTkButton(frame_botones, text="Calcular", command=ejecutar_newton,
                width=150, height=45, font=FUENTE_TEXTO,
                corner_radius=10, fg_color=ROSA, hover_color=ROSA_HOVER,
                text_color='black').grid(row=0, column=0, padx=10)

    # Botón Volver
    ctk.CTkButton(frame_botones, text="Volver", command=volver,
                width=150, height=45, font=FUENTE_TEXTO,
                corner_radius=10, fg_color=ROSA, hover_color=ROSA_HOVER,
                text_color='black').grid(row=0, column=1, padx=10)


def lanzar_lagrange():
    root.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Método de Lagrange")
    ventana.configure(fg_color="white")
    centrar_ventana(ventana, 1000, 600)
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), root.deiconify()))

    contenedor = ctk.CTkFrame(ventana, fg_color="white")
    contenedor.pack(fill="both", expand=True)

    izquierdo = ctk.CTkFrame(contenedor, fg_color="white")
    izquierdo.pack(side="left", fill="both", expand=True)

    formulario = ctk.CTkFrame(izquierdo, fg_color="white")
    formulario.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(formulario, text="Método de Lagrange",
                 font=FUENTE_TITULO, text_color='black').pack(pady=10)

    ctk.CTkLabel(formulario, text="Función objetivo f(x, y):",
                 font=FUENTE_TEXTO, text_color='black').pack(anchor="w")
    entrada_f = ctk.CTkEntry(formulario, width=300, height=40,
                             font=("Dongle Ligth", 16), corner_radius=12)
    entrada_f.pack(pady=10)

    ctk.CTkLabel(formulario, text="Restricción g(x, y) = c:",
                 font=FUENTE_TEXTO, text_color='black').pack(anchor="w")
    entrada_g = ctk.CTkEntry(formulario, width=300, height=40,
                             font=("Dongle Ligth", 16), corner_radius=12)
    entrada_g.pack(pady=10)

    ctk.CTkLabel(formulario, text="Constante c:", font=FUENTE_TEXTO, text_color='black').pack(anchor="w")
    entrada_c = ctk.CTkEntry(formulario, width=300, height=40,
                             font=("Dongle Ligth", 16), corner_radius=12)
    entrada_c.pack(pady=10)

    def ejecutar_lagrange():
        try:
            import LANGRAGE_POLINOMIO_TAYLOR as lagr
            from importlib import reload
            reload(lagr)  # Recargar por si se está ejecutando muchas veces desde GUI

            # Pasar valores ingresados a variables de ese script
            lagr.input_override = {
                "f": entrada_f.get(),
                "g": entrada_g.get(),
                "c": entrada_c.get(),
            }

            lagr.run_desde_gui(entrada_f.get(), entrada_g.get(), float(entrada_c.get()))

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al ejecutar: {e}")

    def volver():
        ventana.destroy()
        root.deiconify()

    ctk.CTkButton(formulario, text="Calcular", command=ejecutar_lagrange,
                  fg_color=AZUL, hover_color=CELESTE, text_color='white',
                  width=200, height=50, font=FUENTE_TEXTO,
                  corner_radius=10).pack(pady=20)

    ctk.CTkButton(formulario, text="Volver", command=volver,
                  fg_color=AZUL, hover_color=CELESTE, text_color='white',
                  width=200, height=50, font=FUENTE_TEXTO,
                  corner_radius=10).pack()

    derecho = ctk.CTkFrame(contenedor, fg_color="white", width=500)
    derecho.pack(side="right", fill="both", expand=False)

    imagen = ctk.CTkImage(Image.open("Images/Math.jpeg"), size=(500, 600))
    ctk.CTkLabel(derecho, image=imagen, text="").pack(fill="both", expand=True)

def lanzar_binarios():
    root.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Operaciones Binarias")
    centrar_ventana(ventana, 1000, 600)
    ventana.configure(fg_color="white")
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), root.deiconify()))

    # CONTENEDOR PRINCIPAL
    contenedor = ctk.CTkFrame(ventana, fg_color="white")
    contenedor.pack(fill="both", expand=True)

    # FRAME IZQUIERDO CON IMAGEN (pegada totalmente a la izquierda)
    izquierdo = ctk.CTkFrame(contenedor, fg_color="white", width=500)
    izquierdo.pack(side="left", fill="both", expand=False)

    img = ctk.CTkImage(Image.open("Images/math.jpeg"), size=(500, 600))
    ctk.CTkLabel(izquierdo, image=img, text="").pack(fill="both", expand=True)

    # FRAME DERECHO CON CAMPOS CENTRADOS
    derecho = ctk.CTkFrame(contenedor, fg_color="white")
    derecho.pack(side="right", fill="both", expand=True)

    # CONTENEDOR CENTRALIZADO
    centrado = ctk.CTkFrame(derecho, fg_color="white")
    centrado.place(relx=0.5, rely=0.5, anchor="center")  # ← CENTRADO TOTAL

    ctk.CTkLabel(centrado, text="Operaciones Binarias", font=FUENTE_TITULO, text_color="black").pack(pady=10)

    opciones = [
        "Decimal a Binario",
        "Binario a Decimal",
        "Sumar Binarios",
        "Restar Binarios",
        "Multiplicar Binarios",
        "Dividir Binarios"
    ]

    variable_opcion = ctk.StringVar(value=opciones[0])
    menu = ctk.CTkOptionMenu(
        centrado,
        values=opciones,
        variable=variable_opcion,
        width=300,
        height=45,
        corner_radius=12,
        fg_color="gray75",  # Color de fondo del menú
        hover=False,
        button_color=AZUL,
        button_hover_color=CELESTE,
        font=("Dongle", 26),  # Más grande pero no exagerado
        dropdown_font=("Dongle", 24),
        dropdown_fg_color="white",
        dropdown_hover_color=CELESTE,
        text_color="black"
    )
    menu.pack(pady=15)


    # FUNCIONES AUXILIARES
    def crear_campo(placeholder):
        entrada = ctk.CTkEntry(centrado, width=300, height=40, font=("Dongle Ligth", 16), corner_radius=10)
        entrada.insert(0, placeholder)
        entrada.bind("<FocusIn>", lambda e: entrada.delete(0, "end") if entrada.get() == placeholder else None)
        entrada.pack(pady=10)
        return entrada

    entrada1 = crear_campo("Ingrese el primer número")
    entrada2 = crear_campo("Ingrese el segundo número (si aplica)")

    def operar():
        from Binarios import (
            decimal_a_binario,
            binario_a_decimal,
            sumar_binarios,
            restar_binarios,
            multiplicar_binarios,
            dividir_binarios,
        )

        op = variable_opcion.get()
        val1 = entrada1.get().strip()
        val2 = entrada2.get().strip()

        try:
            if op == "Decimal a Binario":
                resultado = decimal_a_binario(int(val1))

            elif op == "Binario a Decimal":
                resultado = binario_a_decimal(val1)

            elif op == "Sumar Binarios":
                resultado = sumar_binarios(val1, val2)

            elif op == "Restar Binarios":
                resultado = restar_binarios(val1, val2)

            elif op == "Multiplicar Binarios":
                resultado = multiplicar_binarios(val1, val2)

            elif op == "Dividir Binarios":
                resultado = dividir_binarios(val1, val2)

            else:
                resultado = "Operación no válida"

            messagebox.showinfo("Resultado", f"Resultado: {resultado}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")


    def volver():
        ventana.destroy()
        root.deiconify()

    ctk.CTkButton(centrado, text="Calcular", command=operar,
                  width=200, height=50, font=FUENTE_TEXTO,
                  fg_color=AZUL, hover_color=CELESTE, text_color='black').pack(pady=20)

    ctk.CTkButton(centrado, text="Volver", command=volver,
                  width=200, height=50, font=FUENTE_TEXTO,
                  fg_color=AZUL, hover_color=CELESTE, text_color='black').pack()

def lanzar_biseccion():
    root.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Método de Bisección")
    centrar_ventana(ventana, 1000, 600)
    ventana.configure(fg_color="white")
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), root.deiconify()))

    # CONTENEDOR PRINCIPAL
    contenedor = ctk.CTkFrame(ventana, fg_color="white")
    contenedor.pack(fill="both", expand=True)

    # IZQUIERDA: IMAGEN COMPLETA
    izquierdo = ctk.CTkFrame(contenedor, fg_color="white", width=500)
    izquierdo.pack(side="left", fill="both", expand=False)

    imagen_fondo = ctk.CTkImage(Image.open("Images/Rosa2.jpg"), size=(500, 600))
    ctk.CTkLabel(izquierdo, image=imagen_fondo, text="").pack(fill="both", expand=True)

    # DERECHA: FORMULARIO CENTRADO
    derecho = ctk.CTkFrame(contenedor, fg_color="white")
    derecho.pack(side="right", fill="both", expand=True)

    centrado = ctk.CTkFrame(derecho, fg_color="white")
    centrado.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(centrado, text="Método de Bisección", font=FUENTE_TITULO, text_color="black").pack(pady=10)

    entradas = {}

    def agregar_entrada(frame, texto, clave):
        fila = ctk.CTkFrame(frame, fg_color="white")
        fila.pack(pady=5)
        ctk.CTkLabel(fila, text=texto, font=FUENTE_TEXTO, text_color="black").pack(anchor="w")
        entrada = ctk.CTkEntry(fila, width=300, height=40, font=("Dongle Ligth", 16), corner_radius=10)
        entrada.pack()
        entradas[clave] = entrada

    # Entradas
    agregar_entrada(centrado, "Función f(x):", "funcion")
    agregar_entrada(centrado, "Extremo izquierdo a:", "a")
    agregar_entrada(centrado, "Extremo derecho b:", "b")
    agregar_entrada(centrado, "Criterio de error:", "criterio")

    def ejecutar_biseccion():
        from Biseccion import metodo_biseccion, graficar_biseccion
        try:
            f_str = entradas["funcion"].get()
            a = float(entradas["a"].get())
            b = float(entradas["b"].get())
            criterio = float(entradas["criterio"].get())

            xr, tabla = metodo_biseccion(f_str, a, b, criterio)

            # Mostrar resultado final
            messagebox.showinfo("Resultado", f"Raíz aproximada: {xr:.6f}")

            # --- MOSTRAR TABLA EN OTRA VENTANA ---
            def mostrar_tabla(tabla):
                ventana_tabla = ctk.CTkToplevel()
                ventana_tabla.title("Tabla de iteraciones - Bisección")
                ventana_tabla.geometry("750x400")
                ventana_tabla.configure(fg_color="white")

                contenedor_tabla = ctk.CTkScrollableFrame(ventana_tabla, fg_color="white")
                contenedor_tabla.pack(fill="both", expand=True, padx=10, pady=10)

                headers = ["n", "a", "b", "xr", "f(xr)", "Error"]
                for j, h in enumerate(headers):
                    ctk.CTkLabel(contenedor_tabla, text=h, font=("Arial", 13, "bold"),
                                width=110, text_color="black").grid(row=0, column=j, padx=4, pady=4)

                for i, fila in enumerate(tabla):
                    for j, valor in enumerate(fila):
                        if isinstance(valor, float):
                            texto = f"{valor:.6f}"
                        elif valor is None:
                            texto = "-"
                        else:
                            texto = str(valor)
                        ctk.CTkLabel(contenedor_tabla, text=texto, font=("Arial", 12),
                                    width=110, text_color="black").grid(row=i + 1, column=j, padx=4, pady=4)

            # Llamada correcta (fuera de la función)
            mostrar_tabla(tabla)

            # Mostrar gráfica si el usuario quiere
            if messagebox.askyesno("Gráfica", "¿Deseas ver la gráfica con la raíz?"):
                graficar_biseccion(f_str, xr)

        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos:\n{e}")

    def volver():
        ventana.destroy()
        root.deiconify()

    # BOTONES
    ctk.CTkButton(centrado, text="Calcular", command=ejecutar_biseccion,
                  fg_color=ROSA, hover_color=ROSA_HOVER, text_color="black",
                  width=200, height=40, font=FUENTE_TEXTO).pack(pady=20)

    ctk.CTkButton(centrado, text="Volver", command=volver,
                  fg_color=ROSA, hover_color=ROSA_HOVER, text_color="black",
                  width=200, height=40, font=FUENTE_TEXTO).pack()


def lanzar_dif_divididas():
    root.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Diferencias Divididas")
    ventana.configure(fg_color="white")
    centrar_ventana(ventana, 1000, 600)
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), root.deiconify()))

    contenedor = ctk.CTkFrame(ventana, fg_color="white")
    contenedor.pack(fill="both", expand=True)

    # --- Imagen a la izquierda ---
    izquierdo = ctk.CTkFrame(contenedor, fg_color="white", width=500)
    izquierdo.pack(side="left", fill="both", expand=False)

    imagen = ctk.CTkImage(Image.open("Images/math.jpeg"), size=(500, 600))
    ctk.CTkLabel(izquierdo, image=imagen, text="").pack(fill="both", expand=True)

    # --- Formulario a la derecha ---
    derecho = ctk.CTkFrame(contenedor, fg_color="white")
    derecho.pack(side="right", fill="both", expand=True)

    formulario = ctk.CTkFrame(derecho, fg_color="white")
    formulario.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(formulario, text="Diferencias Divididas", font=FUENTE_TITULO, text_color="black").pack(pady=5)

    # Entrada de sucesión
    ctk.CTkLabel(formulario, text="Secuencia de valores y (separados por comas):", font=FUENTE_TEXTO, text_color="black").pack(anchor="w", pady=(10, 0))
    entrada_y = ctk.CTkEntry(formulario, width=400, height=40, font=("Dongle Ligth", 16), corner_radius=10)
    entrada_y.insert(0, "1, 3*2, 5**2, 7/2")
    entrada_y.bind("<FocusIn>", lambda e: entrada_y.delete(0, "end") if entrada_y.get() == "1, 3*2, 5**2, 7/2" else None)
    entrada_y.pack(pady=10)

    def ejecutar_dif_divididas():
        try:
            y_vals = [eval(s.strip()) for s in entrada_y.get().split(",")]
            x_vals = list(range(1, len(y_vals) + 1))

            coef, tabla = diferencias_divididas_sucesion(x_vals, y_vals)
            polinomio = construir_polinomio(coef, x_vals)

            # Mostrar polinomio en notación LaTeX
            mostrar_formula_latex(polinomio, titulo="Polinomio Interpolante")

            # Mostrar tabla en ventana emergente
            tabla_ventana = ctk.CTkToplevel()
            tabla_ventana.title("Tabla de Diferencias Divididas")
            tabla_ventana.configure(fg_color="white")
            centrar_ventana(tabla_ventana, 600, 400)

            tabla_scroll = ctk.CTkScrollableFrame(tabla_ventana, fg_color="white")
            tabla_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Mostrar encabezados de columnas
            # Crear encabezados bonitos
            for col in range(len(tabla[0])):
                if col == 0:
                    titulo = "xₖ / S[xₖ]"
                else:
                    indices = ", ".join([f"x{i}" for i in range(col + 1)])
                    titulo = f"S[{indices}]"
                ctk.CTkLabel(tabla_scroll, text=titulo, font=("Arial", 16, "bold"),
                            text_color="black").grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

            # Agregar los valores fila por fila
            for i, fila in enumerate(tabla):
                for j, val in enumerate(fila):
                    texto = f"{val:.4f}" if isinstance(val, float) else str(val)
                    ctk.CTkLabel(tabla_scroll, text=texto, font=("Arial", 16),
                                text_color="black").grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")

            if messagebox.askyesno("Gráfica", "¿Deseas ver la gráfica?"):
                x_plot = np.linspace(min(x_vals), max(x_vals) + 2, 300)
                f_interp = sym.lambdify(sym.Symbol('n'), polinomio, modules=["numpy"])
                y_plot = f_interp(x_plot)

                plt.plot(x_plot, y_plot, label="Polinomio interpolante")
                plt.scatter(x_vals, y_vals, color="red", label="Datos")
                plt.title("Diferencias Divididas - Sucesión")
                plt.xlabel("n")
                plt.ylabel("S(n)")
                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")


    def volver():
        ventana.destroy()
        root.deiconify()

    # Botones
    botones_frame = ctk.CTkFrame(formulario, fg_color="white")
    botones_frame.pack(pady=20)

    ctk.CTkButton(botones_frame, text="Calcular", command=ejecutar_dif_divididas,
                  fg_color=AZUL, hover_color=CELESTE, text_color="black",
                  width=150, height=40, font=FUENTE_TEXTO).pack(side="left", padx=10)

    ctk.CTkButton(botones_frame, text="Volver", command=volver,
                  fg_color=AZUL, hover_color=CELESTE, text_color="black",
                  width=150, height=40, font=FUENTE_TEXTO).pack(side="left", padx=10)

def lanzar_diferencias_finitas():
    root.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Diferencias Finitas")
    ventana.configure(fg_color="white")
    centrar_ventana(ventana, 1000, 600)
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), root.deiconify()))

    contenedor = ctk.CTkFrame(ventana, fg_color="white")
    contenedor.pack(fill="both", expand=True)

    # --- Imagen a la izquierda ---
    izquierdo = ctk.CTkFrame(contenedor, fg_color="white", width=500)
    izquierdo.pack(side="left", fill="both", expand=False)

    imagen = ctk.CTkImage(Image.open("Images/Rosa2.jpg"), size=(500, 600))
    ctk.CTkLabel(izquierdo, image=imagen, text="").pack(fill="both", expand=True)

    # --- Formulario a la derecha ---
    derecho = ctk.CTkFrame(contenedor, fg_color="white")
    derecho.pack(side="right", fill="both", expand=True)

    formulario = ctk.CTkFrame(derecho, fg_color="white")
    formulario.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(formulario, text="Diferencias Finitas", font=FUENTE_TITULO, text_color="black").pack(pady=5)

    # Entradas
    entradas = {}
    def entrada(texto, clave):
        ctk.CTkLabel(formulario, text=texto, font=FUENTE_TEXTO, text_color="black").pack(anchor="w", pady=(5, 0))
        campo = ctk.CTkEntry(formulario, width=300, height=40, font=("Dongle Ligth", 16), corner_radius=10)
        campo.pack()
        entradas[clave] = campo
        
    # Entradas necesarias
    entrada("Longitud de la barra (L):", "l")
    entrada("Cantidad de nodos (n):", "n")
    entrada("Temperatura inicial (T0):", "t0")
    entrada("Temperatura final (Tf):", "tf")
    entrada("Fuente térmica Q(x):", "q")  # Puede ser 0 o una función

    def ejecutar_diferencias_finitas():
        from diferencias_finitas import diferencias_finitas
        try:
            L = float(entradas["l"].get())
            n = int(entradas["n"].get())
            T0 = float(entradas["t0"].get())
            Tf = float(entradas["tf"].get())
            Q = entradas["q"].get()

            diferencias_finitas(L, n, T0, Tf, Q)

        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos:\n{e}")

    def volver():
        ventana.destroy()
        root.deiconify()

    # BOTONES
    botones_frame = ctk.CTkFrame(formulario, fg_color="white")
    botones_frame.pack(pady=20)

    ctk.CTkButton(botones_frame, text="Calcular", command=ejecutar_diferencias_finitas,
                fg_color=ROSA, hover_color=ROSA_HOVER, text_color="black",
                width=150, height=40, font=FUENTE_TEXTO).pack(side="left", padx=10)

    ctk.CTkButton(botones_frame, text="Volver", command=volver,
                fg_color=ROSA, hover_color=ROSA_HOVER, text_color="black",
                width=150, height=40, font=FUENTE_TEXTO).pack(side="left", padx=10)



def lanzar_minimos_cuadrados():
    root.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Mínimos Cuadrados")
    ventana.configure(fg_color="white")
    centrar_ventana(ventana, 1000, 600)
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), root.deiconify()))

    # CONTENEDOR PRINCIPAL
    contenedor = ctk.CTkFrame(ventana, fg_color="white")
    contenedor.pack(fill="both", expand=True)

    # FORMULARIO A LA IZQUIERDA
    izquierdo = ctk.CTkFrame(contenedor, fg_color="white")
    izquierdo.pack(side="left", fill="both", expand=True)

    formulario = ctk.CTkFrame(izquierdo, fg_color="white")
    formulario.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(formulario, text="Ajuste por Mínimos Cuadrados",
                 font=FUENTE_TITULO, text_color='black').pack(pady=10)

    ctk.CTkLabel(formulario, text="Ingrese los puntos (x, y):", font=FUENTE_TEXTO, text_color='black').pack(anchor="w")
    entrada_puntos = ctk.CTkEntry(formulario, width=400, height=40, font=("Arial", 16), corner_radius=10)
    entrada_puntos.pack(pady=10)
    entrada_puntos.insert(0, "Ej: 1,2  2,3  3,5")

    # ETIQUETA AGRUPADA
    ctk.CTkLabel(formulario, text="Tipo de ajuste y grado polinómico:", font=FUENTE_TEXTO, text_color='black').pack(anchor="w", pady=(10, 5))

    # CONTENEDOR HORIZONTAL
    tipo_grado_frame = ctk.CTkFrame(formulario, fg_color="white")
    tipo_grado_frame.pack(pady=10)

    # MENÚ DE OPCIONES
    tipo_var = ctk.StringVar(value="lineal")
    opciones = ["Lineal", "Polinómico", "Exponencial", "Simbolico"]
    
    def actualizar_visibilidad_modelo(opcion):
        if opcion == "Simbolico":
            label_modelo.pack(anchor="w", pady=(5, 0))
            modelo_entry.pack(pady=(0, 10))
        else:
            label_modelo.pack_forget()
            modelo_entry.pack_forget()

    menu_tipos = ctk.CTkOptionMenu(
        tipo_grado_frame,
        values=opciones,
        variable=tipo_var,
        command=actualizar_visibilidad_modelo,
        width=220,
        height=40,
        corner_radius=12,
        fg_color=ROSA,
        hover=False,
        button_color=ROSA_HOVER,
        font=("Dongle", 26),
        dropdown_font=("Dongle", 22),
        dropdown_fg_color="white",
        dropdown_hover_color=ROSA_HOVER,
        text_color="black"
    )
    menu_tipos.pack(side="left", padx=10)

    # CAMPO DE GRADO POLINÓMICO
    grado_entry = ctk.CTkEntry(tipo_grado_frame, width=120, height=40, font=("Dongle Ligth", 20), corner_radius=10)
    grado_entry.pack(side="left", padx=10)


    label_modelo = ctk.CTkLabel(formulario, text="Modelo simbólico:", font=FUENTE_TEXTO, text_color='black')
    modelo_entry = ctk.CTkEntry(formulario, width=400, height=40, font=("Dongle Ligth", 16), corner_radius=10)

    def ejecutar_ajuste():
        from minimos_cuadrados import ajuste_lineal, ajuste_polinomico, ajuste_exponencial, ajuste_simbolico_manual
        try:
            puntos_str = entrada_puntos.get()
            puntos = [tuple(map(float, p.split(','))) for p in puntos_str.split()]
            x = np.array([p[0] for p in puntos])
            y = np.array([p[1] for p in puntos])

            tipo = tipo_var.get()
            if tipo == "Lineal":
                p, ecm = ajuste_lineal(x, y)
                mostrar_grafico_lineal(x, y, p, ecm)

            elif tipo == "Polinómico":
                grado = int(grado_entry.get())
                p, ecm = ajuste_polinomico(x, y, grado)
                mostrar_grafico_lineal(x, y, p, ecm)

            elif tipo == "Exponencial":
                modelo, ecm, a, b = ajuste_exponencial(x, y)
                mostrar_grafico_exponencial(x, y, modelo, a, b, ecm)

            elif tipo == "Simbolico":
                modelo = modelo_entry.get().strip()
                if not modelo:
                    messagebox.showwarning("Advertencia", "Por favor ingrese un modelo simbólico.")
                    return
                modelo_ajustado, ecm = ajuste_simbolico_manual(x, y, modelo)
                messagebox.showinfo("Resultado",
                    f"✅ Modelo ajustado:\n"
                    f"  ➤ y = {modelo_ajustado}\n"
                    f"  ➤ Error cuadrático medio (ECM): {ecm:.6e}")

        except Exception as e:
            messagebox.showerror("Error", f"❌ Error en datos:\n{e}")

    def mostrar_grafico_lineal(x, y, modelo, ecm):
        x_vals = np.linspace(min(x), max(x), 100)
        plt.scatter(x, y, color='red', label='Datos')
        plt.plot(x_vals, modelo(x_vals), color='blue', label='Modelo')
        plt.title(f"Modelo Ajustado\nECM: {ecm:.3e}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.legend()
        plt.show()

    def mostrar_grafico_exponencial(x, y, modelo, a, b, ecm):
        x_vals = np.linspace(min(x), max(x), 100)
        y_vals = [modelo(xi) for xi in x_vals]
        plt.scatter(x, y, color='red', label='Datos')
        plt.plot(x_vals, y_vals, color='green', label=f'y = {a:.3f} * exp({b:.3f}x)')
        plt.title(f"Modelo Exponencial\nECM: {ecm:.3e}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.legend()
        plt.show()

    def volver():
        ventana.destroy()
        root.deiconify()

    # CONTENEDOR HORIZONTAL PARA LOS BOTONES
    botones_frame = ctk.CTkFrame(formulario, fg_color="white")
    botones_frame.pack(pady=20)

    ctk.CTkButton(botones_frame, text="Calcular", command=ejecutar_ajuste,
                width=150, height=40, font=FUENTE_TEXTO,
                fg_color=ROSA, hover_color=ROSA_HOVER, text_color='black').pack(side="left", padx=10)

    ctk.CTkButton(botones_frame, text="Volver", command=volver,
                width=150, height=40, font=FUENTE_TEXTO,
                fg_color=ROSA, hover_color=ROSA_HOVER, text_color='black').pack(side="left", padx=10)


    # IMAGEN A LA DERECHA
    derecho = ctk.CTkFrame(contenedor, fg_color="white", width=500)
    derecho.pack(side="right", fill="both", expand=False)

    imagen = ctk.CTkImage(Image.open("Images/math.jpeg"), size=(500, 600))
    ctk.CTkLabel(derecho, image=imagen, text="").pack(fill="both", expand=True)


def mostrar_tabla_iteraciones(tabla):
    ventana_tabla = ctk.CTkToplevel()
    ventana_tabla.title("Tabla de Iteraciones - Newton-Raphson")
    ventana_tabla.geometry("950x400")
    ventana_tabla.configure(fg_color="white")

    contenedor_tabla = ctk.CTkScrollableFrame(ventana_tabla, fg_color="white")
    contenedor_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    headers = ["Iteración", "x", "f'(x)", "f(x)", "Error abs", "Error rel (%)"]
    for j, h in enumerate(headers):
        ctk.CTkLabel(contenedor_tabla, text=h, font=("Arial", 13, "bold"),
                     width=150, text_color="black").grid(row=0, column=j, padx=5, pady=5)

    for i, fila in enumerate(tabla):
        for j, valor in enumerate(fila):
            if valor is None:
                texto = "--"
            elif isinstance(valor, float):
                texto = f"{valor:.6f}"
            else:
                texto = str(valor)
            ctk.CTkLabel(contenedor_tabla, text=texto, font=("Dongle Ligth", 12),
                         width=150, text_color="black").grid(row=i+1, column=j, padx=5, pady=3)

def run_desde_gui(f_expr_str, g_expr_str, c_val):
    global input  # Para que no pida input por consola
    original_input = input

    def input_simulada(prompt):
        if "función objetivo" in prompt.lower():
            return f_expr_str
        elif "restricción" in prompt.lower() and "c" not in prompt.lower():
            return g_expr_str
        elif "valor 'c'" in prompt.lower():
            return str(c_val)
        elif "¿cuántos puntos iniciales" in prompt.lower():
            return "3"
        elif "guess" in prompt.lower():
            return "1 1 1"
        elif "salir" in prompt.lower():
            return "s"
        elif "orden del polinomio" in prompt.lower():
            return "2"
        elif "elige el índice" in prompt.lower():
            return "0"
        return ""

    input = input_simulada
    try:
        exec(open(__file__, encoding="utf-8").read(), globals())
    finally:
        input = original_input


#? Crear ventana principal
root = ctk.CTk()
root.title("Simulación")
root.configure(fg_color="white")
# Tamaño deseado de la ventana principal
ANCHO = 1380  
ALTO = 720

# Centrar la ventana principal en pantalla
centrar_ventana(root, ANCHO, ALTO)

# Fondo de imagen
fondo_img = ctk.CTkImage(Image.open("Images/Blue2.png"), size=(ANCHO, ALTO))
fondo_label = ctk.CTkLabel(root, image=fondo_img, text="")
fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)
fondo_label.lower()

# Título principal
titulo = ctk.CTkLabel(root, text="Simulación y Computación Numérica", font=FUENTE_TITULO, fg_color="white", text_color='black')
titulo.pack(pady=20)

img = CTkImage(Image.open("Images/Image.png"), size=(425, 425))
imagen_label = ctk.CTkLabel(root, image=img, text="")
imagen_label.pack(pady=10)

img1 = tk.PhotoImage(file="Images/Books.png")
img2 = tk.PhotoImage(file="Images/funtion.png")

# Frame central para botones
frame_botones = ctk.CTkFrame(root, fg_color="white", corner_radius=15)
frame_botones.pack()

# Lista de métodos con nombre, color y función
metodos = [
    ("Método de Taylor", CELESTE, lanzar_taylor),
    ("Método de Newton-Raphson", AZUL, lanzar_newton),
    ("Método de Lagrange", CELESTE, lanzar_lagrange),
    ("Mínimos Cuadrados", AZUL, lanzar_minimos_cuadrados),
    ("Operaciones Binarias", CELESTE, lanzar_binarios),
    ("Método de Bisección", AZUL, lanzar_biseccion),
    ("Diferencias Divididas", CELESTE, lanzar_dif_divididas),
    ("Diferencias Finitas", AZUL, lanzar_diferencias_finitas),
]

# Crear botones en una cuadrícula de 2 filas x 4 columnas
for i, (texto, color, funcion) in enumerate(metodos):
    hover = AZUL if color == CELESTE else CELESTE
    btn = ctk.CTkButton(frame_botones, text=texto, fg_color=color, text_color=TEXTO,
                    width=270, height=60, font=FUENTE_TEXTO,
                    command=funcion, corner_radius=10, hover_color=hover)

    btn.grid(row=i//4, column=i%4, padx=10, pady=10)

root.mainloop()