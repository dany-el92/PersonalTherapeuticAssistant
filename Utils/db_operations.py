from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


class Database:
    """
       Classe per gestire la connessione e le operazioni su un database MongoDB per un chatbot.

       Attributi:
           uri (str): l'URI di connessione a MongoDB.
           db_name (str): il nome del database da utilizzare.
           client (MongoClient): oggetto client di MongoDB.
           db (Database): oggetto del database.
    """

    def __init__(self, uri='mongodb://localhost:27017/', db_name='chatbot_db'):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect_to_db()

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

    def get_all_documents(self, collection_name):

        # Funzione che recupera tutti i documenti da una collezione specificata.

        try:
            collection = self.db[collection_name]
            return list(collection.find({}))
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def get_documents_by_tag(self, collection_name, tag):

        # Funzione che recupera i documenti da una collezione specificata in base a un tag.

        try:
            collection = self.db[collection_name]
            return list(collection.find({"tag": tag}))
        except Exception as e:
            print(f"Error retrieving documents by tag: {e}")
            return []

    def insert_document(self, collection_name, document):

        # Funzione che inserisce un documento in una collezione specificata.

        try:
            collection = self.db[collection_name]
            collection.insert_one(document)
        except Exception as e:
            print(f"Error inserting document: {e}")

    def get_all_patterns(self):

        # Funzione che recupera tutti i documenti dalla collezione 'patterns'.

        return self.get_all_documents('patterns')

    def get_all_responses(self):

        # Funzione che recupera tutti i documenti dalla collezione 'responses'.

        return self.get_all_documents('responses')

    def get_patterns_by_tag(self, tag):

        # Funzione che recupera i documenti dalla collezione 'patterns' in base a un tag.

        return self.get_documents_by_tag('patterns', tag)

    def get_responses_by_tag(self, tag):

        # Funzione che recupera i documenti dalla collezione 'responses' in base a un tag.

        return self.get_documents_by_tag('responses', tag)

    def insert_pattern(self, tag, patterns):

        # Funzione che inserisce un nuovo documento nella collezione 'patterns'.

        document = {"tag": tag, "patterns": patterns}
        self.insert_document('patterns', document)

    def insert_response(self, tag, responses):

        # Funzione che inserisce un nuovo documento nella collezione 'responses'.

        document = {"tag": tag, "responses": responses}
        self.insert_document('responses', document)


# Esempio di utilizzo delle funzioni
if __name__ == "__main__":
    db = Database()

    # Esempio di select
    print(db.get_all_patterns())
    print(db.get_all_responses())
    print(db.get_patterns_by_tag('test_tag'))
    print(db.get_responses_by_tag('test_tag'))

    # Esempio di insert
    # db.insert_pattern('test_tag2', ['Hello', 'Hi'])
    # db.insert_response('test_tag2', ['Hello there!', 'Hi!'])

    # DA CANCELLARE (test_tag e test_tag2 sia in pattern che in response)
