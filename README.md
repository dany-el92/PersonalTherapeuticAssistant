<div align="center">
# SupportBot
</div>

# Table of Contents

1. [Introduzione](#introduzione)
2. [Dataset](#dataset)
3. [Guida d'installazione](#guida-installazione)
   - [Installazione di Python](#installazione-python)
   - [Clonazione del repository](#clonazione-del-repository)
   - [Installazione dei Requirements](#installazione-requirements)
5. [Utilizzo](#utilizzo)
   - [Chatbot](#chatbot)
   - [Operazioni CRUD](#operazioni-crud)

# Introduzione

Questo progetto mira a creare un chatbot che interroga un database NoSQL. Il chatbot utilizza un dataset per fornire risposte agli utenti, integrando operazioni CRUD (Create, Read, Update, Delete) sul database. L'obiettivo è sviluppare un sistema efficiente per gestire e rispondere a domande basate sui dati memorizzati.

Il sistema include componenti per la gestione del database, l'interfaccia per l'esecuzione delle operazioni CRUD, l'analisi del dataset e l'interfaccia utente del chatbot.

# Dataset

Il dataset utilizzato include vari file JSON contenenti pattern e risposte. Questi file sono essenziali per il funzionamento del chatbot.

- `tag_responses.json`: contiene le risposte del chatbot.
- `tag_patterns.json`: contiene i pattern delle domande.
- `intents_v2.json`: contiene gli intenti del chatbot.

# Guida d'installazione

Per installare i requisiti necessari per il progetto, seguire i passaggi seguenti.

## Installazione di Python

Verifica di avere Python installato sulla tua macchina. Il progetto è compatibile con Python `3.9`.

Se Python non è installato, fai riferimento alla guida ufficiale [Python Guide](https://www.python.org/downloads/).

## Clonazione del repository

Per clonare questo repository, scarica ed estrai i file del progetto `.zip` usando il pulsante `<Code>` in alto a destra o esegui il seguente comando nel tuo terminale:
```shell git clone <URL>```


# Installazione dei Requirements
Installa i requisiti del progetto utilizzando il seguente comando nel tuo terminale:
```shell pip install -r requirements.txt```

# Utilizzo
## Chatbot
Per avviare il chatbot, eseguire:
```shell python chatbot/main.py```
## Operazioni CRUD
Le operazioni CRUD possono essere eseguite utilizzando il seguente comando nel tuo terminale:
```shell python CRUD/home.py```
