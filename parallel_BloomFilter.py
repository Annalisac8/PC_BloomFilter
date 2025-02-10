from joblib import Parallel, delayed
import hashlib

def calcola_hash(stringa, n, j):
    sha256 = hashlib.sha256()
    sha256.update((stringa + str(j)).encode('utf-8'))  # Aggiorna con la stringa e l'indice j
    return int(sha256.hexdigest(), 16) % n

class BloomFilterParallelo:
    def __init__(self, dimensione, numero_hash, numero_thread):
        # Crea un array di bit di dimensione specificata, inizialmente tutti impostati su zero
        self.array_bit = [0] * dimensione
        self.dimensione = dimensione
        self.numero_hash = numero_hash
        self.numero_thread = numero_thread

    def inizializza(self, elemento):
        risultato = []  # lista  per contenere i risultati
        with Parallel(n_jobs=self.numero_thread) as parallelo:  # Riutilizza lo stesso pool di thread
            for j in range(self.numero_hash): # Itero per il numero di volte specificato in numero_hash
                # Parallelizza applicando l'hash a più elementi della lista di email
                # delayed: aspetta che calcola_hash venga fatto su ogni elemento della lista prima di passare all'hash successivo
                risultato.extend(parallelo(delayed(calcola_hash)(elemento[i], self.dimensione, j) for i in range(len(elemento))))

        # Itero per ogni elemento in risultato
        for i in range(len(risultato)):
            # Imposto l'elemento corrispondente in array_bit a 1
            self.array_bit[risultato[i]] = 1
    def verifica(self, elemento): # Funzione per verificare
        for i in range(self.numero_hash):
            if self.array_bit[calcola_hash(elemento, self.dimensione, i)] == 0:
                return False # Se uno dei bit è 0, l'elemento sicuramente non è presente
        return True # Potrebbe essere presente (ma esistono falsi positivi)

    def verifica_parallela(self, elementi): #funzione per la verifica parallela
        risultato = []
        # Applico contemporaneamente la stessa funzione di verifica a più elementi
        risultato.extend(Parallel(n_jobs=self.numero_thread)(delayed(self.verifica)(elementi[i]) for i in range(len(elementi))))
        return risultato