FROM python:3.11-slim-bullseye
LABEL authors="fabcassano"

WORKDIR /home

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt


CMD ["uvicorn", "generator.app:generator", "--host", "0.0.0.0", "--port", "8010"]
