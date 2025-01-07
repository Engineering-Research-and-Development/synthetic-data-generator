FROM python:3.12-alpine

WORKDIR src/model_registry

COPY requirements.txt /app/model_registry/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/model_registry/requirements.txt

COPY . /app/model_registry


CMD ["fastapi", "run", "/app/model_registry/server/controller.py", "--port", "80"]