FROM python:3.12-alpine

WORKDIR /model_registry

COPY ./server .

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "8001"]