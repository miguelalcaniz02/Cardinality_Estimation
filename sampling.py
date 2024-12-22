import numpy as np

def generate_zipf_stream(n, alpha, N):
    """
    Genera un flujo de datos siguiendo una distribución de Zipf.
    
    :param n: Número de elementos distintos.
    :param alpha: Parámetro de la distribución de Zipf (α >= 0).
    :param N: Longitud total del flujo de datos.
    :return: Lista de elementos del flujo.
    """
    # Paso 1: Calcular la constante de normalización c_n
    ranks = np.arange(1, n + 1)  # Rango de los elementos (1, 2, ..., n)
    probabilities = 1.0 / np.power(ranks, alpha)  # Probabilidades proporcionales a i^(-alpha)
    c_n = probabilities.sum()  # Normalización
    probabilities /= c_n  # Normalizar para que sumen 1

    # Paso 2: Generar N elementos siguiendo las probabilidades
    elements = [f"x{i}" for i in range(1, n + 1)]  # Elementos distintos x1, x2, ..., xn
    stream = np.random.choice(elements, size=N, p=probabilities)

    return stream
