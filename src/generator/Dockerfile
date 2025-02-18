FROM python:3.11-slim-bullseye
LABEL authors="emiliocimino"

WORKDIR /home

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt


CMD ["fastapi", "run", "generator/app.py", "--port", "8010"]