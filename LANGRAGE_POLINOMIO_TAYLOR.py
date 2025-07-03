import numpy as np
import sympy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D

x_s, y_s, lambda_s = sympy.symbols('x y lambda_s')

# ----------------- FUNCIONES DE INPUT --------------------
def get_user_function(prompt_message, variable_names=("x", "y")):
    while True:
        try:
            expr_str = input(prompt_message + f" (usa las variables {', '.join(variable_names)}): ")
            allowed_names = {*variable_names,
                             "sin", "cos", "tan", "exp", "log", "sqrt", "pi",
                             "asin", "acos", "atan", "atan2",
                             "sinh", "cosh", "tanh", "asinh", "acosh", "atanh",
                             "Abs", "Min", "Max", "Heaviside", "Piecewise"} 
            local_dict = {name: sympy.Symbol(name) for name in variable_names}
            local_dict.update({name: getattr(sympy, name) for name in allowed_names if hasattr(sympy, name)})
            local_dict['pi'] = sympy.pi
            parsed_expr = sympy.parse_expr(expr_str, local_dict=local_dict, transformations='all')
            print(f"Interpretado como: {parsed_expr}")
            return parsed_expr
        except Exception as e:
            print(f"Error al interpretar la expresión: {e}. Intenta de nuevo.")

def get_float_input(prompt_message, default_value=None):
    while True:
        try:
            val_str = input(prompt_message + (f" (default: {default_value})" if default_value is not None else "") + ": ")
            if not val_str and default_value is not None:
                return float(default_value)
            return float(val_str)
        except ValueError:
            print("Entrada inválida. Ingresa un número.")

def get_int_input(prompt_message, default_value=None, min_val=None, max_val=None):
    while True:
        try:
            val_str = input(prompt_message + (f" (default: {default_value})" if default_value is not None else "") + ": ")
            if not val_str and default_value is not None:
                val = int(default_value)
            else:
                val = int(val_str)
            if min_val is not None and val < min_val:
                print(f"Debe ser >= {min_val}."); continue
            if max_val is not None and val > max_val:
                print(f"Debe ser <= {max_val}."); continue
            return val
        except ValueError:
            print("Entrada inválida. Ingresa un entero.")

# ----------------- FUNCION PRINCIPAL DESDE GUI --------------------
def run_desde_gui(f_expr_str, g_expr_str, constraint_c):
    from types import SimpleNamespace
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)

    # Preprocesamiento desde GUI
    f_expr_sym = sympy.sympify(f_expr_str)
    g_expr_sym = sympy.sympify(g_expr_str)
    f_simbolica_user = f_expr_sym
    g_simbolica_user = g_expr_sym - constraint_c
    L = f_simbolica_user - lambda_s * g_simbolica_user
    dL_dx = sympy.diff(L, x_s)
    dL_dy = sympy.diff(L, y_s)
    dL_dlambda = sympy.diff(L, lambda_s)

    _grad_L = sympy.lambdify((x_s, y_s, lambda_s), [dL_dx, dL_dy, dL_dlambda], modules=['numpy'])
    def grad_L_func(vec):
        try:
            return np.array(_grad_L(*vec), dtype=float)
        except:
            return np.array([np.nan, np.nan, np.nan])

    # Punto inicial por defecto (puedes hacer esto dinámico desde GUI si lo deseas)
    guess = [1.0, 1.0, 1.0]
    sol = fsolve(grad_L_func, guess)
    g_func = sympy.lambdify((x_s, y_s), g_simbolica_user, modules=['numpy'])
    if not np.isclose(g_func(sol[0], sol[1]), 0, atol=1e-4):
        print("No cumple la restricción, intenta con otro punto inicial.")
        return

    x0, y0 = sol[0], sol[1]
    orden = 2
    fxy = f_simbolica_user
    dfdx = sympy.diff(fxy, x_s)
    dfdy = sympy.diff(fxy, y_s)
    taylor = fxy.subs({x_s:x0, y_s:y0}) + dfdx.subs({x_s:x0,y_s:y0})*(x_s-x0) + dfdy.subs({x_s:x0,y_s:y0})*(y_s-y0)

    if orden >= 2:
        d2fdx2 = sympy.diff(dfdx, x_s).subs({x_s:x0, y_s:y0})
        d2fdy2 = sympy.diff(dfdy, y_s).subs({x_s:x0, y_s:y0})
        d2fdxdy = sympy.diff(dfdx, y_s).subs({x_s:x0, y_s:y0})
        taylor += (1/2)*(d2fdx2*(x_s-x0)**2 + 2*d2fdxdy*(x_s-x0)*(y_s-y0) + d2fdy2*(y_s-y0)**2)

    print(f"Polinomio de Taylor orden {orden} en ({x0:.4f},{y0:.4f}):")
    print(sympy.expand(taylor))

    # Gráfica 2D
    f_func = sympy.lambdify((x_s, y_s), fxy, modules=['numpy'])
    taylor_func = sympy.lambdify((x_s, y_s), taylor, modules=['numpy'])
    g_func = sympy.lambdify((x_s, y_s), g_simbolica_user, modules=['numpy'])

    x_vals = np.linspace(x0 - 2, x0 + 2, 100)
    y_vals = np.linspace(y0 - 2, y0 + 2, 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z_f = f_func(X, Y)
    Z_t = taylor_func(X, Y)
    Z_g = g_func(X, Y)

    plt.figure(figsize=(8, 6))
    plt.contour(X, Y, Z_f, levels=20, cmap='viridis')
    plt.contour(X, Y, Z_t, levels=20, cmap='plasma', linestyles='--')
    plt.contour(X, Y, Z_g, levels=[0], colors='red')
    plt.plot(x0, y0, 'mo', label='Punto de Expansión')
    plt.legend(); plt.title('f(x,y), Taylor y Restricción')
    plt.grid(); plt.show()

# ----------------- EJECUCIÓN INTERACTIVA DESDE TERMINAL --------------------
if __name__ == "__main__":
    print("--- MODO CONSOLA ---")
    f_expr_str = get_user_function("Ingresa f(x,y)", ("x", "y"))
    g_expr_str = get_user_function("Ingresa g(x,y)", ("x", "y"))
    c_val = get_float_input("Ingresa el valor c en g(x,y) = c")
    run_desde_gui(str(f_expr_str), str(g_expr_str), c_val)
