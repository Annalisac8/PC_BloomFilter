"""
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

    def inizializza(self, elementi):
        # Crea una lista vuota per contenere i risultati
        risultato = []
        with Parallel(n_jobs=self.numero_thread) as parallelo:  # Riutilizza lo stesso pool di thread
            # Itera per il numero di volte specificato nella proprietà numero_hash
            for j in range(self.numero_hash):
                risultato.extend(  # Parallelizza applicando l'hash a più elementi della lista di elementi
                                   # con delayed si aspetta che calcola_hash venga applicato a ogni elemento della lista prima di passare all'hash successivo
                    parallelo(delayed(calcola_hash)(elementi[i], self.dimensione, j)
                              for i in range(len(elementi)))
                )

        # Itera per ogni elemento nella lista risultato
        for i in range(len(risultato)):
            # Imposta l'elemento corrispondente nell'array_bit a 1
            self.array_bit[risultato[i]] = 1

    def verifica(self, elementi):
        for i in range(self.numero_hash):
            if self.array_bit[calcola_hash(elementi, self.dimensione, i)] == 0:
                return False
        return True

    def verifica_parallela(self, elementi):
        risultato = []
        risultato.extend(Parallel(n_jobs=self.numero_thread)(delayed(self.verifica)(elementi[i])
                                                             for i in range(len(elementi))))
        # Parallelizza applicando contemporaneamente la stessa funzione di verifica della stringa a più elementi
        return risultato

"""

import hashlib
import numpy as np
from joblib import Parallel, delayed

# Funzione per calcolare numero_hash di hash di un singolo elemento
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
        risultati = Parallel(n_jobs=self.numero_thread, backend="loky")( #loky permette di eseguire il calcolo su più core
            delayed(calcola_hash_multiplo)(el, self.dimensione, self.numero_hash) for el in elementi
        )

        # Aggiorno il filtro di Bloom
        for hash_list in risultati:
            np.put(self.array_bit, hash_list, 1)  # Modifica diretta su array NumPy

    def verifica(self, elemento):
        """Verifica se un elemento potrebbe essere nel filtro"""
        return all(self.array_bit[calcola_hash(elemento, self.dimensione, j)] for j in range(self.numero_hash))

    def verifica_parallela(self, elementi):
        """Parallelizza la verifica di più elementi nel filtro"""
        return Parallel(n_jobs=self.numero_thread, backend="loky")( #applica la funzione verifica ad ogni elemento della lista elementi in parallelo
            delayed(self.verifica)(e) for e in elementi
        )
