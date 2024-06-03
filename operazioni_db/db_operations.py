from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


class Database:
    """
    Classe per gestire la connessione e le operazioni su un database MongoDB per un chatbot.

    Attributi:
        uri (str): L'URI di connessione a MongoDB.
        db_name (str): Il nome del database da utilizzare.
        client (MongoClient): L'oggetto client di MongoDB.
        db (Database): L'oggetto del database.
    """

    def __init__(self, uri='mongodb://localhost:27017/', db_name='chatbot_db'):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect_to_db()
        self.create_indexes()

    def connect_to_db(self):
        """
        Connette al database MongoDB e imposta l'oggetto del database.
        Gestisce le eccezioni in caso di fallimento della connessione.
        """
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
        except ConnectionFailure as e:
            print(f"Error connecting to database: {e}")
        except OperationFailure as e:
            print(f"Operation failed: {e}")

    def create_indexes(self):
        """
        Crea indici sulle collezioni per migliorare le prestazioni delle query.
        """
        try:
            self.db['patterns'].create_index([('tag', 1), ('patterns', 1)])
            self.db['responses'].create_index([('tag', 1), ('responses', 1)])
        except Exception as e:
            print(f"Error creating indexes: {e}")

    def get_all_documents(self, collection_name):
        """
        Recupera tutti i documenti da una collezione specificata.

        Args:
            collection_name (str): Il nome della collezione da cui recuperare i documenti.

        Returns:
            list: Una lista di documenti dalla collezione.
        """
        try:
            collection = self.db[collection_name]
            return list(collection.find({}))
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def get_documents_by_tag(self, collection_name, tag):
        """
        Recupera i documenti da una collezione specificata in base a un tag.

        Args:
            collection_name (str): Il nome della collezione da cui recuperare i documenti.
            tag (str): Il tag per filtrare i documenti.

        Returns:
            list: Una lista di documenti che corrispondono al tag dalla collezione.
        """
        try:
            collection = self.db[collection_name]
            return list(collection.find({"tag": tag}))
        except Exception as e:
            print(f"Error retrieving documents by tag: {e}")
            return []

    def get_documents_by_tag_covered(self, collection_name, tag):
        """
        Recupera i documenti da una collezione specificata in base a un tag,
        utilizzando una query covered.

        Args:
            collection_name (str): Il nome della collezione da cui recuperare i documenti.
            tag (str): Il tag per filtrare i documenti.

        Returns:
            list: Una lista di documenti che corrispondono al tag dalla collezione.
        """
        try:
            collection = self.db[collection_name]
            if collection_name == "patterns":
                return list(collection.find({"tag": tag}, {"tag": 1, "patterns": 1, "_id": 0}))
            else:
                return list(collection.find({"tag": tag}, {"tag": 1, "responses": 1, "_id": 0}))
        except Exception as e:
            print(f"Error retrieving covered documents by tag: {e}")
            return []

    def insert_document(self, collection_name, document):
        """
        Inserisce un documento in una collezione specificata.

        Args:
            collection_name (str): Il nome della collezione in cui inserire il documento.
            document (dict): Il documento da inserire.
        """
        try:
            collection = self.db[collection_name]
            collection.insert_one(document)
        except Exception as e:
            print(f"Error inserting document: {e}")

    def get_all_patterns(self):
        """
        Recupera tutti i documenti dalla collezione 'patterns'.

        Returns:
            list: Una lista di documenti dalla collezione 'patterns'.
        """
        return self.get_all_documents('patterns')

    def get_all_responses(self):
        """
        Recupera tutti i documenti dalla collezione 'responses'.

        Returns:
            list: Una lista di documenti dalla collezione 'responses'.
        """
        return self.get_all_documents('responses')

    def get_patterns_by_tag(self, tag):
        """
        Recupera i documenti dalla collezione 'patterns' in base a un tag.

        Args:
            tag (str): Il tag per filtrare i documenti.

        Returns:
            list: Una lista di documenti che corrispondono al tag dalla collezione 'patterns'.
        """
        return self.get_documents_by_tag('patterns', tag)

    def get_responses_by_tag(self, tag):
        """
        Recupera i documenti dalla collezione 'responses' in base a un tag.

        Args:
            tag (str): Il tag per filtrare i documenti.

        Returns:
            list: Una lista di documenti che corrispondono al tag dalla collezione 'responses'.
        """
        return self.get_documents_by_tag('responses', tag)

    def insert_pattern(self, tag, patterns):
        """
        Inserisce un nuovo documento nella collezione 'patterns'.

        Args:
            tag (str): Il tag del documento.
            patterns (list): La lista dei pattern associati al tag.
        """
        document = {"tag": tag, "patterns": patterns}
        self.insert_document('patterns', document)

    def insert_response(self, tag, responses):
        """
        Inserisce un nuovo documento nella collezione 'responses'.

        Args:
            tag (str): Il tag del documento.
            responses (list): La lista delle risposte associate al tag.
        """
        document = {"tag": tag, "responses": responses}
        self.insert_document('responses', document)

    def delete_documents_by_tag(self, collection_name, tag):
        """
        Cancella i documenti da una collezione specificata in base a un tag.

        Args:
            collection_name (str): Il nome della collezione da cui cancellare i documenti.
            tag (str): Il tag per filtrare i documenti.
        """
        try:
            collection = self.db[collection_name]
            collection.delete_many({"tag": tag})
        except Exception as e:
            print(f"Error deleting documents by tag: {e}")

    def delete_all_documents(self, collection_name):
        """
        Cancella tutti i documenti da una collezione specificata.

        Args:
            collection_name (str): Il nome della collezione da cui cancellare i documenti.
        """
        try:
            collection = self.db[collection_name]
            collection.delete_many({})
        except Exception as e:
            print(f"Error deleting all documents: {e}")

    def delete_specific_response(self, tag, response):
        """
        Elimina una risposta specifica da un documento con un determinato tag.

        Args:
            tag (str): Il tag del documento.
            response (str): La risposta da eliminare.
        """
        try:
            collection = self.db['responses']
            collection.update_one({"tag": tag}, {"$pull": {"responses": response}})
        except Exception as e:
            print(f"Error deleting specific response: {e}")

    def delete_specific_pattern(self, tag, pattern):
        """
        Elimina un pattern specifico da un documento con un determinato tag.

        Args:
            tag (str): Il tag del documento.
            pattern (str): Il pattern da eliminare.
        """
        try:
            collection = self.db['patterns']
            collection.update_one({"tag": tag}, {"$pull": {"patterns": pattern}})
        except Exception as e:
            print(f"Error deleting specific pattern: {e}")

    def update_document_by_tag(self, collection_name, tag, new_document):
        """
        Aggiorna un documento in una collezione specificata in base a un tag.

        Args:
            collection_name (str): Il nome della collezione in cui aggiornare il documento.
            tag (str): Il tag del documento da aggiornare.
            new_document (dict): Il nuovo documento.
        """
        try:
            collection = self.db[collection_name]
            collection.update_one({"tag": tag}, {"$set": new_document})
        except Exception as e:
            print(f"Error updating document by tag: {e}")

    def update_specific_response(self, tag, response, new_response):
        """
        Aggiorna una risposta specifica da un documento con un determinato tag.

        Args:
            tag (str): Il tag del documento.
            response (str): La risposta da aggiornare.
            new_response (str): La nuova risposta.
        """
        try:
            collection = self.db['responses']
            collection.update_one({"tag": tag, "responses": response}, {"$set": {"responses.$": new_response}})
        except Exception as e:
            print(f"Error updating specific response: {e}")

    def update_specific_pattern(self, tag, pattern, new_pattern):
        """
        Aggiorna un pattern specifico da un documento con un determinato tag.

        Args:
            tag (str): Il tag del documento.
            pattern (str): Il pattern da aggiornare.
            new_pattern (str): Il nuovo pattern.
        """
        try:
            collection = self.db['patterns']
            collection.update_one({"tag": tag, "patterns": pattern}, {"$set": {"patterns.$": new_pattern}})
        except Exception as e:
            print(f"Error updating specific pattern: {e}")



# Esempio di utilizzo delle funzioni
if __name__ == "__main__":
    # Creazione dell'istanza del database, che crea automaticamente gli indici
    db = Database()

    # Esempio di select
    # print(db.get_all_patterns())
    # print(db.get_all_responses())
    # print(db.get_patterns_by_tag('goodbye'))
    # print(db.get_responses_by_tag('goodbye'))
    #
    # # Esempio di covered query
    # print(db.get_documents_by_tag_covered('patterns', 'greeting'))
    #
    # # Esempio di insert
    # db.insert_pattern('test_tag2', ['Hello', 'Hi'])
    # db.insert_response('test_tag2', ['Hello there!', 'Hi!'])

    # DA CANCELLARE patter e response con test_tag e test_tag2

    # Esempio di delete
    # db.delete_documents_by_tag('patterns', 'test_tag2')
    # db.delete_documents_by_tag('responses', 'test_tag2')

    # Esempio di delete all
    # db.delete_all_documents('patterns')
    # db.delete_all_documents('responses')

    # Esempio di delete specific
    # db.delete_specific_response('test_tag2', 'Hi!')
    # db.delete_specific_pattern('test_tag2', 'Hello')

    # Esempio di update
    # db.update_document_by_tag('patterns', 'test_tag2', {'tag': 'test_tag2', 'patterns': ['Hello', 'Hi!']})
    # db.update_document_by_tag('responses', 'test_tag2', {'tag': 'test_tag2', 'responses': ['Hello there!', 'Hi!']})

    # Esempio di update specific
    # db.update_specific_response('test_tag2', 'Hi!', 'Hi :)')
    # db.update_specific_pattern('test_tag2', 'Hello', 'Hello there')



