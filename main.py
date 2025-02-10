# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import string
import random
from sequential_BloomFilter import BloomFilter  # Importa la classe
from parallel_BloomFilter import BloomFilterParallelo  # Importa la classe


# Funzione per generare parole casuali
def genera_parola_casuale(lunghezza):
    return ''.join(random.choices(string.ascii_lowercase, k=lunghezza))


    # Funzione per generare email casuali
def genera_email_casuale():
    domini = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com", "icloud.com"]
    nome = ''.join(random.choices(string.ascii_lowercase, k=7))
    return nome + "@" + random.choice(domini)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Parametri del test
    dimensione_filtro = 10000  # Numero di bit nel filtro
    numero_hash = 100  # Numero di funzioni hash
    numero_thread = 4  # Numero di thread per la versione parallela
    numero_elementi = 100000  # Numero di email da inserire

    # Generazione delle email
    random.seed(42)  # Per ripetibilità dei risultati
    email_inserite = [genera_email_casuale() for _ in range(numero_elementi)]
    email_da_verificare = email_inserite[:2500] + [genera_email_casuale() for _ in range(2500)]

    """Test del Filtro di Bloom sequenziale"""
    filtro_seq = BloomFilter(dimensione_filtro, numero_hash)

    print("Esecuzione sequenziale:")
    tempo_inizio = time.time()
    filtro_seq.inizializza(email_inserite)
    tempo_fine = time.time()
    print(f"Tempo inserimento: {tempo_fine - tempo_inizio:.5f} sec")

    tempo_inizio = time.time()
    for email in email_da_verificare:
        filtro_seq.verifica(email)
    tempo_fine = time.time()
    print(f"Tempo verifica: {tempo_fine - tempo_inizio:.5f} sec")

    """Test del Filtro di Bloom parallelo"""
    filtro_par = BloomFilterParallelo(dimensione_filtro, numero_hash, numero_thread)

    print("\nEsecuzione parallela:")
    tempo_inizio = time.time()
    filtro_par.inizializza(email_inserite)
    tempo_fine = time.time()
    print(f"Tempo inserimento: {tempo_fine - tempo_inizio:.5f} sec")

    tempo_inizio = time.time()
    filtro_par.verifica_parallela(email_da_verificare)
    tempo_fine = time.time()
    print(f"Tempo verifica: {tempo_fine - tempo_inizio:.5f} sec")


"""
    # Test di inserimento
    tempo_inizio = time.time()
    filtro.inizializza(email_inserite)
    tempo_fine = time.time()
    print("Tempo di esecuzione per l'inserimento delle email:", tempo_fine - tempo_inizio, "secondi")

    # Test di verifica con debug
    print("\n🔍 **Verifica Email**")
    email_presenti = 0
    falsi_positivi = 0

    for email in email_da_verificare:
        risultato = filtro.verifica(email)
        print(f"Email: {email} -> {'PRESENTE' if risultato else 'NON PRESENTE'}")

        if email in email_inserite and risultato:
            email_presenti += 1  # Corretta identificazione
        elif email not in email_inserite and risultato:
            falsi_positivi += 1  # Il filtro ha sbagliato

    print("\n📊 **Risultati Finali**")
    print(f"Email correttamente trovate nel filtro: {email_presenti}/{len(email_da_verificare)}")
    print(f"Falsi positivi: {falsi_positivi}/{len(email_da_verificare)}")
"""


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
