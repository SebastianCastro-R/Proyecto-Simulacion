import numpy as np
import sympy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import matplotlib.colors # 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D 

# --- 0. Configuración de Símbolos ---
x_s, y_s, lambda_s = sympy.symbols('x y lambda_s')

def get_user_function(prompt_message, variable_names=("x", "y")):
    """Solicita al usuario una función como cadena y la convierte a una expresión SymPy."""
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
            local_dict['pi'] = sympy.pi # Asegurar que pi sea la constante de sympy

            parsed_expr = sympy.parse_expr(expr_str, local_dict=local_dict, transformations='all')
            print(f"Interpretado como: {parsed_expr}")
            return parsed_expr
        except (SyntaxError, TypeError, sympy.SympifyError) as e:
            print(f"Error al interpretar la expresión: {e}. Por favor, inténtalo de nuevo.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}. Por favor, inténtalo de nuevo.")


def get_float_input(prompt_message, default_value=None):
    while True:
        try:
            val_str = input(prompt_message + (f" (default: {default_value})" if default_value is not None else "") + ": ")
            if not val_str and default_value is not None:
                return float(default_value)
            return float(val_str)
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")

def get_int_input(prompt_message, default_value=None, min_val=None, max_val=None):
    while True:
        try:
            val_str = input(prompt_message + (f" (default: {default_value})" if default_value is not None else "") + ": ")
            if not val_str and default_value is not None:
                val = int(default_value)
            else:
                val = int(val_str)
            
            if min_val is not None and val < min_val:
                print(f"El valor debe ser al menos {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"El valor no debe exceder {max_val}.")
                continue
            return val
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número entero.")

# Datos del Usuario ---
print("--- Configuración del Problema ---")
f_expr_str = get_user_function("Ingresa la función objetivo f(x,y)", ("x", "y"))
g_expr_str = get_user_function("Ingresa la expresión de la restricción g(x,y)", ("x", "y"))
constraint_c = get_float_input("Ingresa el valor 'c' para la restricción g(x,y) = c (ej. si g(x,y)-c=0, ingresa c)", 0)

f_simbolica_user = f_expr_str
g_simbolica_user = g_expr_str - constraint_c

print(f"\nFunción objetivo f(x,y): {f_simbolica_user}")
print(f"Restricción g(x,y) = 0: {g_simbolica_user} = 0")

# Multiplicadores de Lagrange ---
L = f_simbolica_user - lambda_s * g_simbolica_user
print(f"\nLagrangiano L(x,y,lambda): {L}")

dL_dx = sympy.diff(L, x_s)
dL_dy = sympy.diff(L, y_s)
dL_dlambda = sympy.diff(L, lambda_s)

print(f"dL/dx: {dL_dx}")
print(f"dL/dy: {dL_dy}")
print(f"dL/dlambda: {dL_dlambda}")

_temp_grad_L_func_sympy = sympy.lambdify((x_s, y_s, lambda_s),
                                         [dL_dx, dL_dy, dL_dlambda],
                                         modules=['numpy', 'sympy'])

def grad_L_func(vars_vec):
    x_val, y_val, lambda_val = vars_vec
    try:
        result = _temp_grad_L_func_sympy(x_val, y_val, lambda_val)
        return np.array(result, dtype=float)
    except (TypeError, ValueError, AttributeError, ZeroDivisionError) as e: # Añadido ZeroDivisionError
        return np.array([np.nan, np.nan, np.nan], dtype=float)


num_guesses = get_int_input("¿Cuántos puntos iniciales (guesses) para fsolve quieres probar?", 5, min_val=1)
initial_guesses = []
print("Ingresa los puntos iniciales (x y lambda) separados por espacios:")
for i in range(num_guesses):
    while True:
        try:
            guess_str = input(f"Guess {i+1} (ej: 1.0 1.0 1.0): ")
            parts = list(map(float, guess_str.split()))
            if len(parts) == 3:
                initial_guesses.append(parts)
                break
            else:
                print("Por favor, ingresa 3 números para x, y, lambda.")
        except ValueError:
            print("Entrada inválida. Ingresa números separados por espacios.")


print("\n--- Puntos Críticos Encontrados (x, y, lambda) ---")
critical_points = []
g_eval_func_user = sympy.lambdify((x_s, y_s), g_simbolica_user, modules=['numpy', 'sympy'])

for guess in initial_guesses:
    try:
        current_guess = np.array(guess, dtype=float)
        solution, infodict, ier, mesg = fsolve(grad_L_func, current_guess, full_output=True, xtol=1.49012e-08)

        if ier == 1:
            g_val_at_sol = g_eval_func_user(solution[0], solution[1])
            if np.isclose(g_val_at_sol, 0, atol=1e-4):
                is_new_point = True
                for cp_sol, cp_lambda_val in critical_points:
                    if np.allclose(cp_sol, solution[:2], atol=1e-3):
                        is_new_point = False
                        break
                if is_new_point:
                    critical_points.append((solution[:2], solution[2]))
                    print(f"Solución con guess {guess}: x={solution[0]:.4f}, y={solution[1]:.4f}, lambda={solution[2]:.4f}, g(x,y)={g_val_at_sol:.2e}")
    except Exception as e:
        print(f"Error procesando guess {guess}: {e}")

if not critical_points:
    print("No se encontraron puntos críticos que satisfagan la restricción.")
    if input("¿Quieres salir (s/n)? ").lower() == 's':
        exit()
    else:
        print("Reinicia el script para probar con otros guesses o funciones.")
        exit()

print("\n--- Selección del Punto de Expansión para Taylor ---")
if len(critical_points) == 1:
    point_of_expansion_data = critical_points[0]
    print("Solo se encontró un punto crítico, usándolo para la expansión de Taylor.")
else:
    print("Puntos críticos encontrados:")
    for i, (cp_xy, cp_lambda) in enumerate(critical_points):
        print(f"{i}: (x={cp_xy[0]:.4f}, y={cp_xy[1]:.4f}), lambda={cp_lambda:.4f}")
    choice_idx = -1
    while choice_idx < 0 or choice_idx >= len(critical_points):
        choice_idx = get_int_input(f"Elige el índice del punto para la expansión (0 a {len(critical_points)-1})", 0, 0, len(critical_points)-1)
    point_of_expansion_data = critical_points[choice_idx]

point_of_expansion = point_of_expansion_data[0]
x0, y0 = point_of_expansion
lambda_at_expansion = point_of_expansion_data[1]
print(f"Punto de Expansión seleccionado: ({x0:.4f}, {y0:.4f}) con lambda={lambda_at_expansion:.4f}")

taylor_order = get_int_input("Ingresa el orden del polinomio de Taylor (ej. 1, 2)", 2, 1, 5)

# Polinomio de Taylor para f(x,y) alrededor de (x0, y0) ---
f_at_x0y0 = f_simbolica_user.subs({x_s: x0, y_s: y0})
dfdx_s_expr = sympy.diff(f_simbolica_user, x_s) 
dfdy_s_expr = sympy.diff(f_simbolica_user, y_s)
dfdx_at_x0y0 = dfdx_s_expr.subs({x_s: x0, y_s: y0})
dfdy_at_x0y0 = dfdy_s_expr.subs({x_s: x0, y_s: y0})

taylor_poly_s = f_at_x0y0 + \
                dfdx_at_x0y0 * (x_s - x0) + \
                dfdy_at_x0y0 * (y_s - y0)

if taylor_order >= 2:
    d2fdx2_s_expr = sympy.diff(dfdx_s_expr, x_s)
    d2fdy2_s_expr = sympy.diff(dfdy_s_expr, y_s)
    d2fdxdy_s_expr = sympy.diff(dfdx_s_expr, y_s)
    
    d2fdx2_at_x0y0 = d2fdx2_s_expr.subs({x_s: x0, y_s: y0})
    d2fdy2_at_x0y0 = d2fdy2_s_expr.subs({x_s: x0, y_s: y0})
    d2fdxdy_at_x0y0 = d2fdxdy_s_expr.subs({x_s: x0, y_s: y0})
    
    taylor_poly_s += (1/sympy.factorial(2)) * (
                        d2fdx2_at_x0y0 * (x_s - x0)**2 + \
                        2 * d2fdxdy_at_x0y0 * (x_s - x0) * (y_s - y0) + \
                        d2fdy2_at_x0y0 * (y_s - y0)**2
                    )
if taylor_order > 2:
    print(f"Advertencia: La construcción manual de Taylor está implementada solo hasta orden 2. El polinomio será de orden 2.")

taylor_poly_s = sympy.expand(taylor_poly_s)
print(f"\nPolinomio de Taylor de orden (hasta) {min(taylor_order, 2)} para f(x,y) alrededor de ({x0:.4f}, {y0:.4f}):")
print(f"T(x,y) = {taylor_poly_s}")

f_num = sympy.lambdify((x_s, y_s), f_simbolica_user, modules=['numpy', 'sympy'])
g_num_constraint_only = sympy.lambdify((x_s, y_s), g_simbolica_user, modules=['numpy', 'sympy'])
taylor_poly_num = sympy.lambdify((x_s, y_s), taylor_poly_s, modules=['numpy', 'sympy'])

#4. Visualización ---
print("\nGenerando visualizaciones...")

if critical_points:
    all_x_coords = [cp_data[0][0] for cp_data in critical_points] + [x0]
    all_y_coords = [cp_data[0][1] for cp_data in critical_points] + [y0]
    x_range_padding = max(1.5, 0.2 * (max(all_x_coords) - min(all_x_coords))) if len(all_x_coords)>1 and max(all_x_coords) != min(all_x_coords) else 1.5
    y_range_padding = max(1.5, 0.2 * (max(all_y_coords) - min(all_y_coords))) if len(all_y_coords)>1 and max(all_y_coords) != min(all_y_coords) else 1.5
    x_min_plot, x_max_plot = min(all_x_coords) - x_range_padding, max(all_x_coords) + x_range_padding
    y_min_plot, y_max_plot = min(all_y_coords) - y_range_padding, max(all_y_coords) + y_range_padding
else:
    x_min_plot, x_max_plot = x0 - 1.5, x0 + 1.5 # Centrar en el punto de expansión si no hay críticos
    y_min_plot, y_max_plot = y0 - 1.5, y0 + 1.5
    if not critical_points: # Solo imprimir si realmente no hay
      print("No hay puntos críticos para guiar el rango de graficación. Usando un rango por defecto alrededor del punto de expansión.")


x_vals = np.linspace(x_min_plot, x_max_plot, 100)
y_vals = np.linspace(y_min_plot, y_max_plot, 100)
X, Y = np.meshgrid(x_vals, y_vals)


try:
    Z_f = f_num(X, Y)
    if np.any(~np.isfinite(Z_f)):
        print("Advertencia: f(x,y) contiene valores no finitos. Intentando reemplazarlos para graficar.")
        Z_f = np.nan_to_num(Z_f, nan=np.nan, posinf=np.nan, neginf=np.nan) # Reemplazar con NaN
except Exception as e:
    print(f"Error al evaluar f_num para graficar: {e}. Se usarán NaNs.")
    Z_f = np.full_like(X, np.nan)

try:
    Z_g_constraint = g_num_constraint_only(X, Y)
except Exception as e:
    print(f"Error al evaluar g_num_constraint_only para graficar: {e}. Se usarán NaNs.")
    Z_g_constraint = np.full_like(X, np.nan)

try:
    Z_taylor = taylor_poly_num(X, Y)
    if np.any(~np.isfinite(Z_taylor)):
        print("Advertencia: Taylor(x,y) contiene valores no finitos. Intentando reemplazarlos para graficar.")
        Z_taylor = np.nan_to_num(Z_taylor, nan=np.nan, posinf=np.nan, neginf=np.nan) # Reemplazar con NaN
except Exception as e:
    print(f"Error al evaluar taylor_poly_num para graficar: {e}. Se usarán NaNs.")
    Z_taylor = np.full_like(X, np.nan)



plt.figure(figsize=(10, 8))
try:
    valid_Z_f = np.isfinite(Z_f)
    if np.any(valid_Z_f): # Solo si hay algún valor finito
        contour_f = plt.contour(X[valid_Z_f].reshape(X.shape)[0,:], Y[valid_Z_f].reshape(Y.shape)[:,0], Z_f[valid_Z_f].reshape(Z_f.shape), levels=20, cmap='viridis')
        # La reestructuración anterior es compleja, una forma más simple es:
        plt.colorbar(contour_f, label='f(x,y) values')
    else:
        print("f(x,y) es completamente no finita en el rango, no se pueden dibujar contornos.")
except (ValueError, TypeError) as ve:
    print(f"No se pudieron generar contornos para f(x,y): {ve}.")

try:
    if np.any(np.isfinite(Z_g_constraint)):
      plt.contour(X, Y, Z_g_constraint, levels=[0], colors='red', linewidths=2)
except (ValueError, TypeError) as ve:
    print(f"No se pudieron generar contornos para g(x,y): {ve}.")


if critical_points:
    for i, (cp_xy, cp_lambda) in enumerate(critical_points):
        plt.plot(cp_xy[0], cp_xy[1], 'bo', markersize=8, label='Punto Crítico' if i == 0 else "")
plt.plot(x0, y0, 'm*', markersize=12, label=f'Punto Expansión Taylor ({x0:.2f}, {y0:.2f})')
plt.title(f'f(x,y), Restricción (g-({constraint_c}))=0, y Puntos Críticos')
plt.xlabel('x'); plt.ylabel('y')
current_handles, current_labels = plt.gca().get_legend_handles_labels()
legend_elements_fig1 = [
    Line2D([0], [0], color='red', lw=2, label=f'Restricción (g-({constraint_c:.2f})=0)'),
]
# Añadir solo los que no estén ya (para 'Punto Crítico' y 'Punto Expansión Taylor')
# Esto es para evitar duplicados si plt.plot ya les dio label
final_handles = []
final_labels = []
for h,l in zip(current_handles, current_labels):
    if l not in final_labels:
        final_handles.append(h)
        final_labels.append(l)
for el in legend_elements_fig1:
    if el.get_label() not in final_labels:
        final_handles.append(el)
        final_labels.append(el.get_label())
plt.legend(handles=final_handles, labels=final_labels, loc='best')
plt.grid(True); plt.axhline(0, color='black', lw=0.5); plt.axvline(0, color='black', lw=0.5); plt.axis('equal')
plt.show()


# Superficies 3D
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
try:
    if np.any(np.isfinite(Z_f)):
        ax.plot_surface(X, Y, Z_f, cmap='viridis', alpha=0.6, edgecolor='none') # edgecolor='none' para suavizar
except Exception as e:
    print(f"No se pudo graficar la superficie de f(x,y): {e}")
try:
    if np.any(np.isfinite(Z_taylor)):
        ax.plot_surface(X, Y, Z_taylor, cmap='plasma', alpha=0.8, edgecolor='none')
except Exception as e:
    print(f"No se pudo graficar la superficie de Taylor: {e}")

ax.scatter(x0, y0, f_num(x0, y0), color='magenta', s=100, depthshade=True)
print("Nota: La visualización de f(x,y) sobre g(x,y)=0 en 3D requiere parametrizar la restricción.")
if critical_points:
    for cp_xy, cp_lambda in critical_points:
        try:
            ax.scatter(cp_xy[0], cp_xy[1], f_num(cp_xy[0], cp_xy[1]), color='blue', s=80, depthshade=True)
        except: pass

ax.set_title(f'f(x,y) y Taylor O({min(taylor_order,2)}) cerca de ({x0:.2f}, {y0:.2f})')
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')

try:
    viridis_cmap = matplotlib.colormaps['viridis']
    plasma_cmap = matplotlib.colormaps['plasma']
except (AttributeError, KeyError): 
    viridis_cmap = plt.cm.get_cmap('viridis')
    plasma_cmap = plt.cm.get_cmap('plasma')
    
representative_viridis_color = viridis_cmap(0.5)
representative_plasma_color = plasma_cmap(0.5)

proxy_f = plt.Rectangle((0, 0), 1, 1, fc=representative_viridis_color, alpha=0.6)
proxy_taylor = plt.Rectangle((0, 0), 1, 1, fc=representative_plasma_color, alpha=0.8)


proxy_expansion_point = Line2D([0], [0], marker='o', color='w', markerfacecolor='magenta', markersize=10, linestyle='None')
proxy_critical_points_3d = Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, linestyle='None')
ax.legend([proxy_f, proxy_taylor, proxy_expansion_point, proxy_critical_points_3d],
          ['f(x,y)', f'Taylor O({min(taylor_order,2)})', 'Punto Expansión', 'Puntos Críticos'], loc='best')
plt.show()


# Figura 3: Corte
plt.figure(figsize=(10, 6))
y_slice = y0
slice_width = (x_max_plot - x_min_plot) / 5 if (x_max_plot - x_min_plot) > 1e-6 else 1.0 # Evitar división por cero
x_slice_vals = np.linspace(x0 - slice_width/2, x0 + slice_width/2, 200)
f_slice = f_num(x_slice_vals, y_slice)
taylor_slice = taylor_poly_num(x_slice_vals, y_slice)

plt.plot(x_slice_vals, f_slice, label=f'f(x, {y_slice:.2f}) (Original)', color='blue')
plt.plot(x_slice_vals, taylor_slice, label=f'Taylor(x, {y_slice:.2f}) (Orden {min(taylor_order,2)})', color='orange', linestyle='--')
plt.scatter(x0, f_num(x0,y0), color='magenta', s=100, zorder=5, label=f'Punto Expansión ({x0:.2f},{y_slice:.2f})')
plt.title(f'Comparación en corte y={y_slice:.2f}')
plt.xlabel('x'); plt.ylabel('Valor'); plt.legend(); plt.grid(True)
plt.show()

print("\nSimulación interactiva completada.")
