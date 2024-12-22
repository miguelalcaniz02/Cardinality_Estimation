from hyperloglog import HyperLogLog
from recordinality import Recordinality
import numpy as np
import math
import string
import random

def hll_runs(data, b, runs):
    """
    Ejecuta el estimador HyperLogLog múltiples veces y calcula la media de las estimaciones.
    :param data: Flujo de datos a procesar.
    :param b: Parámetro de bits de la clase HyperLogLog.
    :param runs: Número de ejecuciones para promediar.
    :return: Media de las estimaciones.
    """
    estimates = []
    for _ in range(runs):
        hll = HyperLogLog(b=b)
        two_letters = ''.join(random.choices(string.ascii_lowercase, k=2))
        for item in data:
            item += two_letters
            hll.add(item)
        estimates.append(hll.estimate())
    avg_var_exvar = []
    avg_var_exvar.append(int(sum(estimates) / runs))
    avg_var_exvar.append(np.std(estimates))

    #Calculate the expected SE
    if b <= 4:
       avg_var_exvar.append(1.106/((2**b)**0.5))
    if b == 5:
       avg_var_exvar.append(1.07/((2**b)**0.5))
    if b == 6:
       avg_var_exvar.append(1.054/((2**b)**0.5))
    if b == 7:
       avg_var_exvar.append(1.046/((2**b)**0.5))
    if b > 7:
       avg_var_exvar.append(1.03896/(2**(b/2)))
    return avg_var_exvar

def rec_runs(data, k, runs):
    """
    Ejecuta el estimador Recordinality múltiples veces y calcula la media de las estimaciones.
    :param data: Flujo de datos a procesar.
    :param k: Parámetro de la clase Recordinality.
    :param runs: Número de ejecuciones para promediar.
    :return: Media de las estimaciones.
    """
    estimates = []
    for _ in range(runs):
        recordinality = Recordinality(k=k)
        two_letters = ''.join(random.choices(string.ascii_lowercase, k=2))
        for item in data:
            item += two_letters
            recordinality.add(item)
        estimates.append(recordinality.estimate())
    avg_var = []
    avg_var.append(sum(estimates) / runs)
    avg_var.append(np.std(estimates))
    return avg_var


# Leer el dataset
with open("datasets/iliad.txt", "r", encoding="utf-8") as file:
    content = file.read()  # Lee todo el contenido del archivo
data = content.split()

print("0 %")

cardinality = len(set(data)) #Cardinal real
n = cardinality
runs = 50 #Numero de ejecuciones

# Vectores de expected variance i avg

# Parameters
k_values = [2 ** i for i in range(2, 9+1)]  # k = 2^2, 2^3, ..., 2^9


#ESTIMADORES HHL
# Calcular la media de los estimadores para cada b
estimators_hll = []
var_hll = []
expected_var_hll = []
for b in range(2, 9 + 1):
    #print(f"Calculando para b = {b} ...")
    hll = hll_runs(data, b, runs)
    estimators_hll.append(hll[0])
    var_hll.append(hll[1])
    expected_var_hll.append(hll[2])
    #print(f"Media de la estimación para b={b}: {avg_estimate}")
    print(f"{int((b-2)*100/14)+2} %")

error_hll = []
for b in range(2, 9 + 1):
    #print(f"Calculando para b = {b} ...")
    error = abs(n-estimators_hll[b-2])/n
    error_hll.append(error)

#ESTIMADORES REC
estimators_rec = []
var_rec = []
for k in range(2, 9 + 1):
    #print(f"Calculando para k = {k} ...")
    rec = rec_runs(data, 2**k, runs)
    estimators_rec.append(rec[0])
    var_rec.append(rec[1])
    #print(f"Media de la estimación para b={k}: {avg_estimate}")
    print(f"{int((k+5)*100/14)} %")

error_rec = []
for k in range(2, 9 + 1):
    #print(f"Calculando para k = {k} ...")
    error = abs(n-estimators_rec[k-2])/n
    error_rec.append(error)

print(estimators_hll)
formatted_error_hll = [f"{value:.3f}" for value in error_hll]
print(formatted_error_hll)

print(estimators_rec)
formatted_error_rec = [f"{value:.3f}" for value in error_rec]
print(formatted_error_rec)

print(n)

print(f"{runs} runs")
print("k | hll_avg | hll_error | hll_var | hll_ex_var | rec_avg | rec_error | rec_variance")
for k in range(2, 9 + 1):
    print(f"{2**k} & {int(estimators_hll[k-2])} & {formatted_error_hll[k-2]} & {int(var_hll[k-2])} & {int(n*expected_var_hll[k-2])} & {int(estimators_rec[k-2])} & {formatted_error_rec[k-2]} & {int(var_rec[k-2])}\\\\")

