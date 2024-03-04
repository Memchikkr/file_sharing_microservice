FROM python:3.11

WORKDIR /app/
ENV PYTHONPATH=/app
RUN pip install poetry
COPY . .
RUN poetry config virtualenvs.create false && poetry install && poetry lock
