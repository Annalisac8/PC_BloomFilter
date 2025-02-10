from joblib import Parallel, delayed
import hashlib

def calcola_hash(stringa, n, j):
    sha256 = hashlib.sha256()
    # Aggiorna l'oggetto sha256 con la stringa e l'indice j
    sha256.update((stringa + str(j)).encode('utf-8'))
    return int(sha256.hexdigest(), 16) % n

class BloomFilterParallelo:
    def __init__(self, dimensione, numero_hash, numero_thread):
        # Crea un array di bit di dimensione specificata, inizialmente tutti impostati su zero
        self.array_bit = [0] * dimensione
        self.dimensione = dimensione
        self.numero_hash = numero_hash
        self.numero_thread = numero_thread
