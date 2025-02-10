import hashlib
import time

# Funzione per calcolare hash
def calcola_hash(string, n, j):
    sha256 = hashlib.sha256()
    sha256.update((string + str(j)).encode('utf-8'))
    return int(sha256.hexdigest(), 16) % n

# Classe FiltroBloom
class BloomFilter:
    def __init__(self, dimensione, numero_hash):
        self.array_bit = [0] * dimensione  # Array di bit inizializzato a 0
        self.dimensione = dimensione  # Dimensione totale dell'array
        self.numero_hash = numero_hash  # Numero di funzioni hash simulate

    def inizializza(self, elementi):
        """ Inserisce gli elementi nel filtro di Bloom """
        for j in range(self.numero_hash): # itera per il numero di volte specificato in numero hash
            for i in range(len(elementi)): # utilizza la funzione calcolo hash per ogni elemento e aggionra il filtro
                self.array_bit[calcola_hash(elementi[i], self.dimensione, j)] = 1

    def verifica(self, elemento):
        """ Verifica se un elemento potrebbe essere presente nel filtro """
        for i in range(self.numero_hash):
            if self.array_bit[calcola_hash(elemento, self.dimensione, i)] == 0:
                return False  # Se uno dei bit è 0, l'elemento sicuramente non è presente
        return True  # Potrebbe essere presente (ma esistono falsi positivi)



