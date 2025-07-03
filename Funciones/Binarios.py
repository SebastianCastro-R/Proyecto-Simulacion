# Binarios.py

def decimal_a_binario(n):
    original = n
    pasos = []
    while n > 0:
        residuo = n % 2
        pasos.append(f"{n} ÷ 2 = {n//2}, residuo = {residuo}")
        n = n // 2
    pasos.reverse()
    binario = ''.join(str(int(original) % 2 if original == 0 else paso[-1]) for paso in pasos)
    print("\nProcedimiento (Decimal a Binario):")
    for paso in pasos:
        print(paso)
    return bin(original)[2:]

def binario_a_decimal(b):
    b = b.strip()
    pasos = []
    decimal = 0
    for i, bit in enumerate(reversed(b)):
        valor = int(bit) * (2 ** i)
        pasos.append(f"{bit} × 2^{i} = {valor}")
        decimal += valor
    print("\nProcedimiento (Binario a Decimal):")
    for paso in pasos:
        print(paso)
    return decimal

def sumar_binarios(b1, b2):
    n1, n2 = int(b1, 2), int(b2, 2)
    print(f"\nSuma: {b1} (={n1}) + {b2} (={n2}) = {n1 + n2} -> binario = {bin(n1 + n2)[2:]}")
    return bin(n1 + n2)[2:]

def restar_binarios(b1, b2):
    n1, n2 = int(b1, 2), int(b2, 2)
    print(f"\nResta: {b1} (={n1}) - {b2} (={n2}) = {n1 - n2} -> binario = {bin(n1 - n2)[2:]}")
    return bin(n1 - n2)[2:]

def multiplicar_binarios(b1, b2):
    n1, n2 = int(b1, 2), int(b2, 2)
    print(f"\nMultiplicación: {b1} (={n1}) × {b2} (={n2}) = {n1 * n2} -> binario = {bin(n1 * n2)[2:]}")
    return bin(n1 * n2)[2:]

def dividir_binarios(b1, b2):
    n1, n2 = int(b1, 2), int(b2, 2)
    if n2 == 0:
        return "Error: división por cero"
    print(f"\nDivisión: {b1} (={n1}) ÷ {b2} (={n2}) = {n1 // n2} -> binario = {bin(n1 // n2)[2:]}")
    return bin(n1 // n2)[2:]

