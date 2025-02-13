FROM python:3.12-alpine

WORKDIR /model_registry

COPY . .

RUN pip install --upgrade -r ./requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "8001"]