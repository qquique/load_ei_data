FROM python:slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off

ENV POETRY_VERSION=1.1.13
RUN apt-get update \
    && apt install -y curl netcat
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY . .
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

ENTRYPOINT ["/app/entrypoint.sh"]
