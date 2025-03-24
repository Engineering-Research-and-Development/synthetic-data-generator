import os
from loguru import logger
import requests

COUCHDB_URL = os.environ.get("couch_db", "http://admin:password@127.0.0.1:5984")
DATABASE_NAME = "models_results"


def is_couch_online():
    response = requests.get(COUCHDB_URL)
    if response.status_code == 200 and response.json():
        return True
    else:
        return False


def check_couch_model_registry():
    """
    This function checks if the couch model registry db is present, otherwise it creates it if absent
    :return:
    """
    response = requests.get(f"{COUCHDB_URL}/_all_dbs")
    if response.status_code != 200:
        logger.error(
            "Could not connect to couch db for server init!\n "
            f"Got the following response:\n"
            f" {response.status_code}:{response.content}  "
        )
    if DATABASE_NAME not in response.json():
        response = requests.put(url=f"{COUCHDB_URL}/{DATABASE_NAME}")
        if response.status_code != 201:
            logger.error(
                "Could not create the couch db model registry\n"
                f"{response.status_code}:{response.content}"
            )
        # Checking if the db has been created
        response = requests.get(f"{COUCHDB_URL}/_all_dbs")
        if response.status_code != 200:
            raise logger.error("Could not reach couch db")
        if DATABASE_NAME not in response.json():
            logger.error(
                "Model registry has been created but couch db is not returning it in the available"
                f"databases.\n{response.status_code}:{response.json()}"
            )


def create_couch_entry() -> None:
    """Creates a new document in CouchDB and returns its _id."""
    url = f"{COUCHDB_URL}/{DATABASE_NAME}/"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json={})
    if response.status_code == 201:
        return response.json().get("id")
    else:
        logger.error(f"Error creating document: {response.text}")


def add_couch_data(doc_id: str, new_data: dict) -> None:
    """Adds a new dictionary to the existing document in CouchDB."""
    url = f"{COUCHDB_URL}/{DATABASE_NAME}/{doc_id}"

    # Fetch the existing document to get the _rev
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Error fetching document: {response.text}")

    doc = response.json()
    doc.update(new_data)
    response = requests.put(url, json=doc)
    if response.status_code not in [200, 201]:
        logger.error(f"Error updating document: {response.text}")
