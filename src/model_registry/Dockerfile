FROM python:3.12-alpine

WORKDIR /model_registry

COPY requirements.txt model_registry/requirements.txt
# Needed for install pyscopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir --upgrade -r model_registry/requirements.txt

COPY . /model_registry

ENV PYTHONPATH="${PYTHONPATH}:/model_registry"

CMD ["fastapi", "run", "model_registry/server/controller.py:app", "--port", "8001"]