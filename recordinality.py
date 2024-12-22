import hashlib
import math

class Recordinality:
    """
    Implementación del algoritmo Recordinality para estimar la cardinalidad
    en un flujo de datos.
    """
    def __init__(self, k):
        """
        Inicializa el algoritmo Recordinality.
        
        :param k: Tamaño de la muestra (número de k-records iniciales).
        """
        self.k = k  # Tamaño de la muestra
        self.sample = {}  # Conjunto para almacenar elementos hash de la muestra
        self.R = k  # Contador de k-records inicializado en k

    @staticmethod
    def _hash(item):
        """
        Aplica una función hash (SHA-256) y devuelve un valor numérico.
        
        :param item: Elemento a ser hasheado.
        :return: Valor hash entero.
        """
        hash_bytes = hashlib.sha256(str(item).encode('utf-8')).digest()
        return int.from_bytes(hash_bytes[:8], byteorder='big')

    def add(self, item):
        """
        Procesa un elemento del flujo de datos.
        
        :param item: Elemento a agregar al algoritmo Recordinality.
        """
        hash_value = self._hash(item)
        
        # Si la muestra no está llena, agrega el hash directamente
        if len(self.sample) < self.k:
            self.sample[item] = hash_value
            return

        # Encuentra el elemento con el menor valor hash en la muestra
        min_item = min(self.sample, key=self.sample.get)
        min_hash = self.sample[min_item]
        
        # Si el nuevo hash es mayor que el menor hash en la muestra
        if hash_value > min_hash and item not in self.sample:
            # Reemplaza el elemento con menor hash en la muestra
            self.sample.pop(min_item)
            self.sample[item] = hash_value
            self.R += 1  # Incrementa el contador de k-records

    def estimate(self):
        """
        Calcula la estimación de cardinalidad usando el número de k-records (R).
        
        :return: Estimación de la cardinalidad.
        """
        k = self.k
        R = self.R
        return int(k * ((1 + 1 / k) ** (R - k + 1) - 1))
