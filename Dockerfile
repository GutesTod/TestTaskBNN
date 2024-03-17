FROM python:3.12-slim

WORKDIR .

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml .

RUN python -m pip install --no-cache-dir poetry==1.7.0 \
    && poetry config virtualenvs.create false \
    && poetry install --without test \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY . .