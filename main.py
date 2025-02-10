# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import random
import string
import random
from sequential_BloomFilter import BloomFilter  # Importa la classe


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
    """Test del Filtro di Bloom con indirizzi email"""

    # Creazione degli insiemi di test
    numero_elementi = 10  # Numero di email da inserire
    email_inserite = []
    email_da_verificare = []

    random.seed(42)  # Per ottenere sempre gli stessi risultati

    for i in range(numero_elementi):
        email_inserite.append(genera_email_casuale())  # Genera email casuali

    # Genero alcune email già inserite e alcune nuove
    email_da_verificare = email_inserite[:5] + [genera_email_casuale() for _ in range(5)]

    # Creazione del filtro di Bloom
    filtro = BloomFilter(5000, 20)  # 5000 bit, 20 funzioni hash

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

    # Test di inserimento
    tempo_inizio = time.time()
    filtro.inizializza(email_inserite)
    tempo_fine = time.time()
    print("Tempo di esecuzione per l'inserimento degli elementi:", tempo_fine - tempo_inizio, "secondi")

    # Test di verifica
    tempo_inizio = time.time()
    for parola in email_da_verificare:
        filtro.verifica(parola)
    tempo_fine = time.time()
    print("Tempo di esecuzione per la verifica degli elementi:", tempo_fine - tempo_inizio, "secondi")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
