FROM python:3.12-slim-bullseye

WORKDIR /app

# Instalar dependências
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
