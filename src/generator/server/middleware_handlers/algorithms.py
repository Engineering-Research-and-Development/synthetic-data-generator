import requests
from loguru import logger

from ai_lib.browse_algorithms import browse_algorithms
from server.middleware_handlers.connection import (
    middleware,
    ALGORITHM_SHORT_TO_LONG,
    ALGORITHM_LONG_TO_SHORT,
    ALGORITHM_LONG_NAME_TO_ID,
)


def sync_available_algorithms():
    """
    Syncs the available algorithms from the middleware to the local server.
    """
    response = requests.get(f"{middleware}algorithms/")

    for remote_algo in response.json().get("algorithms", []):
        if remote_algo.get("name") not in ALGORITHM_SHORT_TO_LONG.keys():
            requests.delete(url=f"{middleware}algorithms/{remote_algo.get('id')}")

    for algorithm in browse_algorithms():
        long_name = algorithm["algorithm"]["name"]
        algorithm["algorithm"]["name"] = ALGORITHM_LONG_TO_SHORT[long_name]
        response = requests.post(url=f"{middleware}algorithms/", json=algorithm)

        if not response.status_code == 201:
            logger.error(f"Error syncing algorithm: {response.text}")
        else:
            algo_id = response.json().get("id")
            ALGORITHM_LONG_NAME_TO_ID[long_name] = algo_id

    logger.info("Algorithm sync completed")
