FROM python:3.12-alpine

WORKDIR /model_registry

COPY . .
# Needed for install pyscopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/model_registry/"


CMD ["fastapi", "run", "server/controller.py", "--port", "8001"]