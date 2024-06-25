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
   - [Creazione del DB](#creazione-DB)
   - [Chatbot](#chatbot)
   - [Operazioni CRUD](#operazioni-crud)

# Introduzione

La salute mentale è un aspetto cruciale del nostro benessere complessivo, influenzando ogni ambito della nostra vita, dalle relazioni interpersonali alla produttività lavorativa. Negli ultimi anni, l'importanza di prendersi cura della propria salute mentale è stata finalmente riconosciuta a livello globale. Sempre più persone hanno iniziato a parlare apertamente dei propri problemi e delle proprie esperienze, contribuendo a rompere lo stigma che circonda questo tema delicato. Questo cambiamento culturale ha portato a una maggiore consapevolezza e accettazione, incoraggiando molti a cercare aiuto e supporto.

In questo contesto, parlare con qualcuno può fare una grande differenza. La comunicazione aperta e onesta è spesso il primo passo verso la guarigione e il benessere emotivo. Tuttavia, non sempre è facile trovare una persona con cui confidarsi, o avere accesso a un professionista della salute mentale.

Per rispondere a questa necessità, abbiamo realizzato Personal Therapeutic Assistant, un assistente virtuale con cui puoi parlare tramite chat. Questo chatbot è progettato per offrire supporto e un ascolto empatico, aiutandoti ad esplorare ed affrontare i tuoi problemi in un ambiente sicuro e riservato. Che tu stia attraversando un momento difficile, abbia bisogno di sfogarti o cerchi semplicemente qualcuno con cui parlare, Personal Therapeutic Assistant è qui per aiutarti. 

# Dataset

Il dataset utilizzato proviene dalla piattaforma Kaggle e comprende conversazioni di base, domande frequenti relative alla salute mentale, dialoghi di terapia classica e consigli generali destinati a persone affette da ansia e depressione. Il dataset è organizzato intorno al concetto di intenti, i quali rappresentano le motivazioni che si nascondono dietro i messaggi inviati dagli utenti al nostro sistema. Per ogni intento, il dataset include pattern di messaggi e risposte appropriate. Nello specifico, i pattern sono esempi di messaggi che riflettono un fine specifico dell'utente, mentre le risposte sono le repliche fornite dal chatbot. Questa struttura permette al sistema di identificare gli intenti degli utenti e rispondere adeguatamente.

Per ottimizzare la gestione e l'utilizzo dei dati, abbiamo diviso il contenuto originale in due file separati: 
- `tag_responses.json`: contiene le risposte del chatbot.
- `tag_patterns.json`: contiene i pattern delle domande.

# Guida d'installazione

Per installare i requisiti necessari per il progetto, seguire i passaggi seguenti.

<b>Installazione di Python</b>

Verifica di avere Python installato sulla tua macchina. Il progetto è compatibile con Python `3.9`.

Se Python non è installato, fai riferimento alla guida ufficiale [Python Guide](https://www.python.org/downloads/).

<b>Clonazione del repository</b>

Per clonare questo repository, scarica ed estrai i file del progetto `.zip` usando il pulsante `<Code>` in alto a destra o esegui il seguente comando nel tuo terminale:
```shell 
git clone https://github.com/dany-el92/PersonalTherapeuticAssistant.git
```


# Installazione dei Requirements
Installa i requisiti del progetto utilizzando il seguente comando nel tuo terminale:
```shell
pip install -r requirements.txt
```

# Utilizzo

## Creazione del Database

1. **Installazione di MongoDB:**
   - Scarica e installa MongoDB dal [sito ufficiale](https://www.mongodb.com/try/download/community).
   - (Opzionale) Installa MongoDB Compass per una gestione grafica del database.

2. **Avvio di MongoDB:**
   - Avvia MongoDB utilizzando il comando appropriato per il tuo sistema operativo.

3. **Creazione del Database:**
   - Esegui il notebook `operazionidb/creazioneDB.ipynb` per creare e configurare il database.

## Chatbot

Per avviare il chatbot, esegui il seguente comando nel terminale:

```shell
python chatbot/main.py
```

## Operazioni CRUD

Le operazioni CRUD possono essere eseguite utilizzando il seguente comando nel tuo terminale:
```shell 
python CRUD/home.py
```
