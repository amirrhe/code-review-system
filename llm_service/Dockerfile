FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry


RUN poetry install

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
