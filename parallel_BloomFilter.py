import hashlib
import numpy as np
from joblib import Parallel, delayed

# Funzione per calcolare un certo numero (numero_hash) di hash di un singolo elemento
def calcola_hash_multiplo(elemento, dimensione, numero_hash):
    return [calcola_hash(elemento, dimensione, j) for j in range(numero_hash)] #restituisce posizioni da impostare a 1 nel filtro

# Funzione hash
def calcola_hash(stringa, n, j):
    sha256 = hashlib.sha256()
    sha256.update((stringa + str(j)).encode('utf-8'))
    return int(sha256.hexdigest(), 16) % n

class BloomFilterParallelo:
    def __init__(self, dimensione, numero_hash, numero_thread):
        self.array_bit = np.zeros(dimensione, dtype=np.uint8)  # Usa NumPy per accesso veloce
        self.dimensione = dimensione
        self.numero_hash = numero_hash
        self.numero_thread = numero_thread

    def inizializza(self, elementi):
        """Parallelizza il calcolo degli hash e aggiorna il filtro in batch"""
        # così evito di aggiornare array_bit uno alla volta durante la parallelizzazione poichè sarebbe meno efficente
        risultati = Parallel(n_jobs=self.numero_thread, backend="loky")( #loky permette di eseguire il calcolo su più core
            delayed(calcola_hash_multiplo)(el, self.dimensione, self.numero_hash) for el in elementi
        )

        # Aggiorno il filtro di Bloom
        for hash_list in risultati:
            # Modifica diretta su array NumPy (overhead della parallelizzazione > aggiornamento diretto con np.put())
            np.put(self.array_bit, hash_list, 1)

    def verifica(self, elemento):
        """Verifica se un elemento potrebbe essere nel filtro"""
        return all(self.array_bit[calcola_hash(elemento, self.dimensione, j)] for j in range(self.numero_hash))

    def verifica_parallela(self, elementi):
        """Parallelizza la verifica di più elementi nel filtro"""
        return Parallel(n_jobs=self.numero_thread, backend="loky")( #applica la funzione verifica ad ogni elemento della lista elementi in parallelo
            delayed(self.verifica)(e) for e in elementi
        )
