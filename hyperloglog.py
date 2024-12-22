import hashlib
import math

class HyperLogLog:
    def __init__(self, b):
        """
        Inicializa HyperLogLog.
        
        :param b: Número de bits utilizados para los registros (m = 2^b subregistros).
        """
        self.b = b
        self.m = 1 << b  # Número de subregistros (2^b)
        self.registers = [0] * self.m  # Inicializa los registros con ceros
        self.alpha = self._compute_alpha(self.m)  # Factor de corrección

    @staticmethod
    def _compute_alpha(m):
        """
        Calcula el factor de corrección alpha_m.
        """
        if m == 16:
            return 0.673
        elif m == 32:
            return 0.697
        elif m == 64:
            return 0.709
        else:
            return 0.7213 / (1 + 1.079 / m)
    
    @staticmethod
    def _hash(item):
        """
        Genera un hash del elemento usando hashlib (SHA-256).
        
        :param item: Elemento a ser hasheado.
        :return: Valor hash como un número entero.
        """
        # Convierte el item a string, lo codifica y aplica SHA-256
        hash_bytes = hashlib.sha256(str(item).encode('utf-8')).digest()
        # Convierte los primeros 8 bytes del hash en un entero
        return int.from_bytes(hash_bytes[:8], byteorder='big')

    @staticmethod
    def _count_leading_zeros(binary_str):
        """
        Cuenta la cantidad de ceros consecutivos al inicio de un string binario.
        """
        count = 0
        for char in binary_str:
            if char == '0':
                count += 1
            else:
                break
        return count

    def add(self, item):
        """
        Agrega un elemento al estimador HyperLogLog.
        
        :param item: Elemento a ser añadido.
        """
        # Genera un hash entero usando hashlib
        hash_value = self._hash(item)
        binary_hash = bin(hash_value)[2:].zfill(64)  # Representación binaria de 64 bits

        # Usa los primeros 'b' bits para determinar el registro
        index = int(binary_hash[:self.b], 2)

        # Cuenta los ceros consecutivos en el resto de los bits (excluyendo los 'b' bits iniciales)
        remaining_bits = binary_hash[self.b:]
        leading_zeros = self._count_leading_zeros(remaining_bits)

        # Actualiza el registro: mantiene el máximo número de ceros observados
        self.registers[index] = max(self.registers[index], leading_zeros + 1)

    def estimate(self):
        """
        Estima la cardinalidad (número de elementos distintos).
        """
        # Calcula la suma inversa de 2^(-Rj) para cada registro
        Z = sum(2 ** (-R) for R in self.registers)

        # Estimación básica
        E = self.alpha * self.m * self.m / Z

        # Corrección para pequeñas cardinalidades (sesgo)
        if E <= 2.5 * self.m:
            V = self.registers.count(0)  # Número de registros con valor 0
            if V > 0:
                E = self.m * math.log(self.m / V)  # Corrección de sesgo

        # Corrección para grandes cardinalidades
        elif E > (1 << 32) / 30.0:  # 2^32 / 30
            E = -(1 << 32) * math.log(1 - E / (1 << 32))

        return int(E)
    