<div align="center">

# SupportBot :speech_balloon: 

 [Amendola Daniela](https://github.com/dany-el92), [Costante Luigina](https://github.com/Luigina2001)
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

Questo progetto ha l'obiettivo di sviluppare un chatbot destinato a fornire supporto alle persone affette da ansia e depressione tramite conversazioni di assistenza per la salute mentale. A differenza dei classici chatbot basati su modelli di apprendimento, esso funziona tramite regole predefinite. Il suo funzionamento è stato implementato interamente attraverso interrogazioni a un database NoSQL contenente conversazioni.

# Dataset

Il dataset utilizzato include tre file JSON contenenti pattern e risposte, essenziali per il funzionamento del chatbot:

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
```shell 
https://github.com/dany-el92/PersonalTherapeuticAssistant.git
```


# Installazione dei Requirements
Installa i requisiti del progetto utilizzando il seguente comando nel tuo terminale:
```shell
pip install -r requirements.txt
```

# Utilizzo
<b>Chatbot</b>
Per avviare il chatbot, eseguire:
```shell 
python chatbot/main.py
```
<b>Operazioni CRUD</b>
Le operazioni CRUD possono essere eseguite utilizzando il seguente comando nel tuo terminale:
```shell 
python CRUD/home.py
```
