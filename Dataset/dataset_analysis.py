import json
import pandas as pd
import plotly.graph_objects as go

# Caricamento dei dati da intents_v2.json
with open('./intents_v2.json', 'r') as f:
    data = json.load(f)

pd.set_option('display.max_columns', None)  # per mostrare tutte le colonne

# Creazione di un DataFrame iniziale
df = pd.DataFrame(data['intents'])

# Espansione dei patterns e delle responses in un nuovo DataFrame
expanded_data = {"tag": [], "pattern": [], "response": []}
for idx, row in df.iterrows():
    tag = row['tag']
    patterns = row['patterns']
    responses = row['responses']
    for pattern in patterns:
        # Associa ogni pattern a una singola risposta casualmente
        response = responses[idx % len(responses)]  # Scelgo la risposta in base all'indice
        expanded_data['tag'].append(tag)
        expanded_data['pattern'].append(pattern)
        expanded_data['response'].append(response)

expanded_df = pd.DataFrame.from_dict(expanded_data)

# Visualizzazione delle prime righe del DataFrame
print(expanded_df.head())

# Statistiche aggiuntive e grafici
print("INFO")
expanded_df.info()

# Intenti unici nel dataset
print("Intenti unici nel dataset:")
print(expanded_df['tag'].unique())
print(f"Numero totale di intenti unici nel dataset: {len(expanded_df['tag'].unique())}")

# Grafico 1: Distribuzione degli Intenti
intent_counts = expanded_df['tag'].value_counts()
fig = go.Figure(data=[go.Bar(x=intent_counts.index, y=intent_counts.values)])
fig.update_layout(title='Distribuzione degli Intenti', xaxis_title='Intenti', yaxis_title='Conteggio')
fig.show()

# Lunghezza media dei pattern e delle risposte per ogni intento
expanded_df['pattern_length'] = expanded_df['pattern'].apply(len)
expanded_df['response_length'] = expanded_df['response'].apply(len)

avg_pattern_length = expanded_df.groupby('tag')['pattern_length'].mean()
avg_response_length = expanded_df.groupby('tag')['response_length'].mean()

# Grafico 2: Analisi della Lunghezza di Pattern e Risposte per Intento
fig = go.Figure()
fig.add_trace(go.Bar(x=avg_pattern_length.index, y=avg_pattern_length.values, name='Lunghezza Media dei Pattern'))
fig.add_trace(go.Bar(x=avg_response_length.index, y=avg_response_length.values, name='Lunghezza Media delle Risposte'))
fig.update_layout(title='Analisi della Lunghezza di Pattern e Risposte', xaxis_title='Intenti',
                  yaxis_title='Lunghezza Media')
fig.show()
