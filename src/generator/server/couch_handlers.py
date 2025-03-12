import os

import requests

COUCHDB_URL = os.environ.get("couch_db", "http://admin:password@127.0.0.1:5984")
DATABASE_NAME = "models_results"

def create_couch_entry()->str:
    """Creates a new document in CouchDB and returns its _id."""
    url = f"{COUCHDB_URL}/{DATABASE_NAME}/"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json={})
    if response.status_code == 201:
        return response.json().get("id")
    else:
        raise Exception(f"Error creating document: {response.text}")


def add_couch_data(doc_id: str, new_data: dict)->None:
    """Adds a new dictionary to the existing document in CouchDB."""
    url = f"{COUCHDB_URL}/{DATABASE_NAME}/{doc_id}"

    # Fetch the existing document to get the _rev
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching document: {response.text}")

    doc = response.json()
    doc.update(new_data)

    # Update the document
    response = requests.put(url, json=doc)
    if response.status_code not in [200, 201]:
        raise Exception(f"Error updating document: {response.text}")
