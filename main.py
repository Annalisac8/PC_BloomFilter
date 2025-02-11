# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import string
import random
import pandas as pd
from sequential_BloomFilter import BloomFilter
from parallel_BloomFilter import BloomFilterParallelo

def genera_parola_casuale(lunghezza):
    return ''.join(random.choices(string.ascii_lowercase, k=lunghezza))

def genera_email_casuale():
    domini = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com", "icloud.com"]
    nome = ''.join(random.choices(string.ascii_lowercase, k=7))
    return nome + "@" + random.choice(domini)

if __name__ == '__main__':
    dimensione_filtro = 10000
    numero_hash = 100
    numero_thread = 4
    numero_elementi = 10000

    random.seed(42)
    email_inserite = [genera_email_casuale() for _ in range(numero_elementi)]
    #prendo le prime [:x] email da email inserite e genero altre (y) casuali per un tot di x+y email da verificare
    email_da_verificare = email_inserite[:1000] + [genera_email_casuale() for _ in range(1000)] #2500

    """ Test del Filtro di Bloom sequenziale """
    filtro_seq = BloomFilter(dimensione_filtro, numero_hash)
    print("Esecuzione sequenziale:")
    tempo_inizio = time.time()
    filtro_seq.inizializza(email_inserite)
    tempo_fine = time.time()
    print(f"Tempo inserimento: {tempo_fine - tempo_inizio:.5f} sec")

    risultati_seq = []
    tempo_inizio = time.time()
    for email in email_da_verificare:
        risultati_seq.append(filtro_seq.verifica(email))
    tempo_fine = time.time()
    print(f"Tempo verifica: {tempo_fine - tempo_inizio:.5f} sec")

    """ Test del Filtro di Bloom parallelo """
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
