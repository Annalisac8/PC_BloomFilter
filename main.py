# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import string
import random
import pandas as pd
from sequential_BloomFilter import BloomFilter
from parallel_BloomFilter import BloomFilterParallelo
import numpy as np

def genera_parola_casuale(lunghezza):
    return ''.join(random.choices(string.ascii_lowercase, k=lunghezza))

def genera_email_casuale():
    domini = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com", "icloud.com"]
    nome = ''.join(random.choices(string.ascii_lowercase, k=7))
    return nome + "@" + random.choice(domini)

if __name__ == '__main__':
    # Parametri
    dimensione_filtro = 1000000
    numero_hash = 50
    numero_elementi = 1000000
    num_test = 1  # Numero di iterazioni per media
    threads_list = [2, 4, 8, 16]  # Lista dei thread da testare

    random.seed(42)
    email_inserite = [genera_email_casuale() for _ in range(numero_elementi)]
    email_da_verificare = email_inserite[:50000] + [genera_email_casuale() for _ in range(50000)]
    numero_email_ver = len(email_da_verificare)

    # ----------------------------- #
    #    Tempo Sequenziale (1 VOLTA)
    # ----------------------------- #
    tempi_inserimento_seq = []
    tempi_verifica_seq = []

    for _ in range(num_test):
        filtro_seq = BloomFilter(dimensione_filtro, numero_hash)

        inizio = time.time()
        filtro_seq.inizializza(email_inserite)  # Se l'inizializzazione è attiva
        fine = time.time()
        tempi_inserimento_seq.append(fine - inizio)

        inizio = time.time()
        risultati_seq = [filtro_seq.verifica(email) for email in email_da_verificare]
        fine = time.time()
        tempi_verifica_seq.append(fine - inizio)

    # Media del tempo sequenziale
    media_ins_seq = np.mean(tempi_inserimento_seq)
    media_ver_seq = np.mean(tempi_verifica_seq)

    # ----------------------------- #
    #    Tempo Parallelo (PER OGNI THREAD)
    # ----------------------------- #
    risultati_parallelo = {}

    for num_thread in threads_list:
        tempi_inserimento_par = []
        tempi_verifica_par = []

        for _ in range(num_test):
            filtro_par = BloomFilterParallelo(dimensione_filtro, numero_hash, num_thread)

            inizio = time.time()
            filtro_par.inizializza(email_inserite)
            fine = time.time()
            tempi_inserimento_par.append(fine - inizio)

            inizio = time.time()
            risultati_par = filtro_par.verifica_parallela(email_da_verificare)
            fine = time.time()
            tempi_verifica_par.append(fine - inizio)

        # Salvo le medie per ogni numero di thread
        risultati_parallelo[num_thread] = {
            "media_ins_par": np.mean(tempi_inserimento_par),
            "media_ver_par": np.mean(tempi_verifica_par)
        }

    # ----------------------------- #
    #    STAMPA I RISULTATI
    # ----------------------------- #
    print("media tempi inizializzazione")
    print(f"{numero_elementi}x{numero_hash} | {media_ins_seq:.4f} |", end=" ")

    for num_thread in threads_list:
        print(f"{risultati_parallelo[num_thread]['media_ins_par']:.4f} |", end=" ")

    print()  # Nuova riga

    print("media tempi verifica")
    print(f"{numero_elementi}x{numero_hash}x{numero_email_ver} | {media_ver_seq:.4f} |", end=" ")

    for num_thread in threads_list:
        print(f"{risultati_parallelo[num_thread]['media_ver_par']:.4f} |", end=" ")

    print()  # Nuova riga

    """
    dimensione_filtro = 1000000
    numero_hash = 75
    numero_thread = 2
    numero_elementi = 1000000

    random.seed(42)
    email_inserite = [genera_email_casuale() for _ in range(numero_elementi)]
    #prendo le prime [:x] email da email inserite e genero altre (y) casuali per un tot di x+y email da verificare
    email_da_verificare = email_inserite[:500] + [genera_email_casuale() for _ in range(500)] #2500

    # Test del Filtro di Bloom sequenziale
    filtro_seq = BloomFilter(dimensione_filtro, numero_hash)
    print("Esecuzione sequenziale:")
    tempo_inizio = time.time()
    #filtro_seq.inizializza(email_inserite)
    tempo_fine = time.time()
    print(f"Tempo inserimento: {tempo_fine - tempo_inizio:.5f} sec")

    risultati_seq = []
    tempo_inizio = time.time()
    #for email in email_da_verificare:
        #risultati_seq.append(filtro_seq.verifica(email))
    tempo_fine = time.time()
    print(f"Tempo verifica: {tempo_fine - tempo_inizio:.5f} sec")

     #Test del Filtro di Bloom parallelo 
    filtro_par = BloomFilterParallelo(dimensione_filtro, numero_hash, numero_thread)
    print("\nEsecuzione parallela:")
    tempo_inizio = time.time()
    filtro_par.inizializza(email_inserite)
    tempo_fine = time.time()
    print(f"Tempo inserimento: {tempo_fine - tempo_inizio:.5f} sec")

    tempo_inizio = time.time()
    risultati_par = filtro_par.verifica_parallela(email_da_verificare)
    tempo_fine = time.time()
    print(f"Tempo verifica: {tempo_fine - tempo_inizio:.5f} sec")
    """

"""
    #per visualizzare risultati sequenziale 
    email_presenti_seq = sum(1 for i, email in enumerate(email_da_verificare) if risultati_seq[i] and email in email_inserite)
    falsi_positivi_seq = sum(1 for i, email in enumerate(email_da_verificare) if risultati_seq[i] and email not in email_inserite)

    print("\n📊 **Risultati Sequenziale**")
    print(f"Email correttamente trovate: {email_presenti_seq}/{len(email_da_verificare)}")
    print(f"Falsi positivi: {falsi_positivi_seq}/{len(email_da_verificare)}")

    df_seq = pd.DataFrame({
        "Email": email_da_verificare,
        "Risultato Filtro": ["Presente" if res else "Non Presente" for res in risultati_seq],
        "Effettivamente Presente": ["✅" if email in email_inserite else "❌" for email in email_da_verificare]
    })
    print("\n📌 **Tabella Risultati Sequenziale**")
    print(df_seq.head(10))  # Mostra solo le prime 10 righe per leggibilità
"""

"""
    #per visualizzare risultati parallelo
    email_presenti_par = sum(1 for i, email in enumerate(email_da_verificare) if risultati_par[i] and email in email_inserite)
    falsi_positivi_par = sum(1 for i, email in enumerate(email_da_verificare) if risultati_par[i] and email not in email_inserite)

    print("\n📊 **Risultati Parallelo**")
    print(f"Email correttamente trovate: {email_presenti_par}/{len(email_da_verificare)}")
    print(f"Falsi positivi: {falsi_positivi_par}/{len(email_da_verificare)}")

    df_par = pd.DataFrame({
        "Email": email_da_verificare,
        "Risultato Filtro": ["Presente" if res else "Non Presente" for res in risultati_par],
        "Effettivamente Presente": ["✅" if email in email_inserite else "❌" for email in email_da_verificare]
    })
    print("\n📌 **Tabella Risultati Parallelo**")
    print(df_par.head(10))  # Mostra solo le prime 10 righe per leggibilità
"""

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
