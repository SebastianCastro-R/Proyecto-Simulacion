# Pruebas

## Método de Taylor

### Encontrar el polinomio

#### Prueba 1

f(x) = ```x*exp(-x)```
Grado del polinomio: ```3```
X~0~ = ```0```
Valor a aproximar X~1~ = ```0.25```

#### Resultado esperado:

Polinomio: \[
\frac{x^3}{2} - x^2 + x
\]

Aproximación: \[p(0.25)= 0.1953125\]
Valor Real: \[f(0.25)= 0.194700\]
Error absoluto: \[0.0006123\]
Cota Máxima: \[0.0006510\]

#### Prueba 2

f(x) = ```x*exp(x-1)```
Grado del polinomio: ```3```
X~0~ = ```1```
Valor a aproximar X~1~ = ```0.9```

Polinomio: \[
2x + \frac{2(x-1)^3}{3} + \frac{3(x-1)^2}{2} - 1
\]

Aproximación: \[p(0.9)= 0.7843\]
Valor Real: \[f(0.9)= 0.814354\]
Error absoluto \[0.030054\]
Cota Máxima \[0.00002083\]

### Encontrar el grado del polinomio

#### Prueba 1

f(x) = ```ln(x)```
Grado del polinomio: Puedes poner cualquiera, por ejemplo 1, no afectara
X~0~ = ```exp(1)```
X~1~ = ```3```

Error/Presición = ```0.0001```

#### Resultado esperado:

Grado del polinomio: \[3\]

#### Prueba 2

f(x) = ```sin(x)```
Grado del polinomio: Puedes poner cualquiera, por ejemplo 5, no afectara
X~0~ = ```pi/6```
X~1~ = ```28*pi/180```

Error/Presición = ```0.00001```

#### Resultado esperado:

Grado del polinomio: \[2\]

## Operaciones Binarias

Para esta función la escritura es muy sencilla, solo debes tener en cuenta:

- Decimales: Solo se admiten naturales, es decir sin .
- El Segundo campo para escribir solo se utiliza en los casos de sumar, restar, multiplicar y dividir binarios.

Ejemplo: 

| Operación      | Campo 1 | Campo 2 | Resultado |
| -------------- | ------- | ------- | --------- |
| Suma           | `1010`  | `1100`  | `10110`   |
| Resta          | `1100`  | `1010`  | `0010`    |
| Multiplicación | `101`   | `11`    | `1111`    |
| División       | `1100`  | `10`    | `110`     |

## Método de Bisección

#### Prueba 1
f(x) = ```exp(-x)-x```
Extremos: $\`[a,b]$
a: ```0```         b: ```1```
Criterio Error: ```0.0001```

#### Resultado esperado:

Raiz: \[\sqrt{x}=\]
Tabla:
![Prueba1](Images/Ejemplos1.png "Prueba1")

#### Prueba 2

f(x) = ```x**2-5```
Extremos: $\`[2,3]$
Criterio Error: ```0.0001```

#### Resultado esperado:

Raiz: \[\sqrt{5}=2.2360679775\]
Tabla:
![Prueba2](Images/Ejemplos2.png "Prueba2")

#### Prueba 3

f(x) = ```x**3 + 4*x**2 - 10```
Extremos: $\`[1,2]$
Criterio Error: ```0.0001```

#### Resultado esperado:

Raiz: \[\sqrt{x}=\]

Tabla:
![Prueba3](Images/Ejemplos3.png "Prueba3")

# Método de Newton-Raphson

## 📌 Parámetros de entrada

- **Función:** `f(x) = sin(x) - 2/(x^2 + 1)`
- **Intervalo:** `a = -1`, `b = 10`
- **Cantidad de puntos para graficar:** `50`
- **Error máximo permitido:** `0.001`
- **Número máximo de iteraciones:** `20`
- **Valor inicial para Newton-Raphson:** `x₀ = 0`

---

## 📈 Iteraciones

| Iteración |    xₙ     |   f'(xₙ)    |     f(xₙ)     | Error Absoluto | Error Relativo (%) |
|-----------|-----------|-------------|----------------|----------------|---------------------|
| 0         | 0.000000  | 1.000000     | -2.0000000000  | --             | --                  |
| 1         | 2.000000  | -0.0961468   | 0.509297       | 2.000000       | 100.0000            |
| 2         | 7.297079  | 0.538478     | 0.812028       | 5.297079       | 72.5918             |
| 3         | 5.789071  | 0.899829     | -0.532200      | 1.508008       | 26.0492             |
| 4         | 6.380517  | 1.009940     | 0.0492293      | 0.591445       | 9.2696              |
| 5         | 6.331772  | 1.013820     | -0.000104229   | 0.048745       | 0.7698              |
| 6         | 6.331875  | 1.013810     | -2.93189e-10   | 0.000103       | 0.0016              |

---

## ✅ Resultado Final

- **Raíz aproximada:** `6.331875`
- **f(6.331875):** `-2.931889 × 10⁻¹⁰`
- **Error absoluto final:** `≈ 0.000103`
- **Error relativo porcentual:** `≈ 0.0016%`
- **Iteraciones realizadas:** `6`



## Método de Lagrange

# Método de Mínimos Cuadrados

## 📌 Datos de entrada

- **Cantidad de puntos:** `6`
- **Modelo a ajustar:** `y = a/x + b/sqrt(x)`

### Tabla de datos

| `xᵢ` | 0.1 | 0.2 | 0.4 | 0.5 | 1.0 | 2.0 |
|------|-----|-----|-----|-----|-----|-----|
| `yᵢ` | 2.1 | 1.1 | 7.0 | 6.0 | 5.0 | 6.0 |

---

## 🔁 Transformación del modelo

Transformamos el modelo no lineal en uno lineal en los parámetros:

\[
yᵢ = a \cdot z₁ᵢ + b \cdot z₂ᵢ, \quad \text{donde:}
\]
- \( z₁ᵢ = \frac{1}{xᵢ} \)
- \( z₂ᵢ = \frac{1}{\sqrt{xᵢ}} \)

Aplicamos mínimos cuadrados clásicos con:

\[
\vec{β} = (Z^T Z)^{-1} Z^T \vec{Y}, \quad \text{con } β = \begin{bmatrix} a \\ b \end{bmatrix}
\]

---

## ✅ Modelo ajustado

- **Función ajustada:**

\[
y = \frac{-2.15712464104885}{x} + \frac{7.03694505106239}{\sqrt{x}}
\]

- **Error cuadrático medio (ECM):**

\[
\text{ECM} = 3.833572
\]

---

## 📌 Observación

Este modelo logra un buen ajuste para la tendencia no lineal de los datos observados, combinando términos racionales con raíces cuadradas.

---


## Diferencias Divididas

## Método de Diferencias Finitas

### 🧪 Prueba 1

**Ecuación diferencial:**
```
y' + 2*y + cos(x)
```

**Parámetros:**
- Extremo izquierdo `a = 0`
- Extremo derecho `b = π/2`
- Paso `h = π/8`
- Condición inicial `y(0) = -0.3`
- Condición final `y(π/2) = -0.1`

#### ✔ Resultado esperado:
```
--- Solución Aproximada ---
y(0.0000) ≈ -0.300000
y(0.3927) ≈ -0.232322
y(0.7854) ≈ -0.196560
y(1.1781) ≈ -0.170006
y(1.5708) ≈ -0.100000
```

📊 Se grafica la curva aproximada de la solución con 5 nodos (incluyendo los extremos), donde se observa un comportamiento creciente.

---

### 🧪 Prueba 2

**Ecuación diferencial:**
```
y' + y - exp(x)
```

**Parámetros:**
- Extremo izquierdo `a = 0`
- Extremo derecho `b = 1`
- Paso `h = 0.25`
- Condición inicial `y(0) = 1`
- Condición final `y(1) = 2`

#### ✔ Resultado esperado:
```
--- Solución Aproximada ---
y(0.0000) ≈ 1.000000
y(0.2500) ≈ 1.150357
y(0.5000) ≈ 1.370928
y(0.7500) ≈ 1.671986
y(1.0000) ≈ 2.000000
```

📊 Se genera una curva suavemente creciente que aproxima la solución esperada de forma precisa con 5 nodos.

---
