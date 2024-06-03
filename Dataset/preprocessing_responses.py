import json
import pandas as pd


def carica_da_json(file_path):
    """Carica i dati da un file JSON."""
    with open(file_path, 'r') as f:
        return json.load(f)


def ottieni_tags_e_patterns(tag_responses):
    """Estrae i tags e i responses dai dati."""
    tags = [entry["tag"] for entry in tag_responses]
    responses = [response for entry in tag_responses for response in entry["responses"]]
    tot_responses = len(responses)
    return tags, responses, tot_responses


def controlla_valori_nulli(df):
    """Controlla la presenza di valori nulli nel DataFrame."""
    valori_nulli_colonne = df.isnull().any()
    valori_nulli_righe = df.isnull().any(axis=1)
    return valori_nulli_colonne, valori_nulli_righe


# Caricamento dei dati dal file JSON contenente i pattern dei tag
file_path = './tag_responses.json'
tag_responses = carica_da_json(file_path)

print("---------------------------------------------------------------------------------------------------------")

# Estrazione dei tags e dei patterns
tags, responses, tot_patterns = ottieni_tags_e_patterns(tag_responses)

print("Tags:")
print(tags)
print("\nResponses:")
print(responses)
print("\nNumero totale di patterns:", tot_patterns)

print("---------------------------------------------------------------------------------------------------------")

# Creazione di un DataFrame pandas dai dati
df = pd.DataFrame(tag_responses)

# Controllo la presenza di valori nulli
valori_nulli_colonne, valori_nulli_righe = controlla_valori_nulli(df)

print("\nValori nulli nelle colonne:")
print(valori_nulli_colonne)
print("\nValori nulli nelle righe:")
print(valori_nulli_righe)

print("---------------------------------------------------------------------------------------------------------")

print("INFO")
df.info()

print("---------------------------------------------------------------------------------------------------------")

statistiche = df.describe(include='all')
print(f"STATISTICHE:\n{statistiche}")