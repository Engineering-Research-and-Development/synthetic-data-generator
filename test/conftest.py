import glob
import json
import os
import requests
import pytest
from dataclasses import dataclass
from typing import Iterable


DEFAULT_TIMEOUT = 2.0


def first_reachable(urls: Iterable[str]) -> str:
    for url in urls:
        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            if response.ok:
                return url
        except requests.RequestException:
            continue
    raise RuntimeError(f"No available endpoints with: {list(urls)}")


def candidates(env_name: str, fallback: str) -> list[str]:
    env_value = os.environ.get(env_name)

    urls = []
    if env_value:
        urls.append(env_value)

    if fallback.startswith("http://127.0.0.1"):
        urls.append(fallback)
        urls.append(fallback.replace("127.0.0.1", "host.docker.internal"))

    return urls


@dataclass(frozen=True, slots=True)
class ServiceConfig:
    middleware: str
    generator: str
    couch: str


def resolve_services() -> ServiceConfig:
    return ServiceConfig(
        middleware=first_reachable(candidates("MIDDLEWARE", "http://127.0.0.1:8001")),
        generator=first_reachable(candidates("GENERATOR", "http://127.0.0.1:8010")),
        couch=first_reachable(candidates("COUCH", "http://127.0.0.1:5984")),
    )


SERVICE_CONFIG = resolve_services()


@pytest.fixture(scope="session")
def get_services() -> ServiceConfig:
    return SERVICE_CONFIG


def load_jsons(resources_path):
    json_files = glob.glob(os.path.join(resources_path, "*.json"))

    jsons = []
    for json_file in json_files:
        with open(json_file) as f:
            jsons.append((json_file, json.load(f)))

    return jsons
