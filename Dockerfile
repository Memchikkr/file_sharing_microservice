FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app
RUN pip install poetry
COPY .env src poetry.lock pyproject.toml /app/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
