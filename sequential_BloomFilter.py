import hashlib

# Funzione per calcolare hash
def calcola_hash(string, n, j):
    sha256 = hashlib.sha256()
    sha256.update((string + str(j)).encode('utf-8'))
    return int(sha256.hexdigest(), 16) % n

# Classe FiltroBloom
class FiltroBloom:
    def __init__(self, dimensione, numero_hash):
        self.array_bit = [0] * dimensione  # Array di bit inizializzato a 0
        self.dimensione = dimensione  # Dimensione totale dell'array
        self.numero_hash = numero_hash  # Numero di funzioni hash simulate