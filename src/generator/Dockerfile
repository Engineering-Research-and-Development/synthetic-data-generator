FROM python:3.11-slim-bullseye
LABEL authors="fabcassano"

WORKDIR /home

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt


CMD ["uvicorn", "orion_catcher.main:orion_catcher", "--host", "0.0.0.0", "--port", "8010"]
