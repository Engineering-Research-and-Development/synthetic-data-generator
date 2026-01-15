FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /home
COPY . .

RUN uv init
RUN uv add -r ./requirements.txt

CMD [".venv/bin/pytest", "."]