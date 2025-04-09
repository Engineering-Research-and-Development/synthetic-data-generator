import os

middleware = os.environ.get("MIDDLEWARE", "http://127.0.0.1:8001")
generator = os.environ.get("GENERATOR", "http://127.0.0.1:8010")
couch = os.environ.get("COUCH", "http://127.0.0.1:5984")
