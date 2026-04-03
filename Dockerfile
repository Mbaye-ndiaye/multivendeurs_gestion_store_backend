FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /app

WORKDIR /app

COPY . /app/


# RUN python -m venv /env
# ENV PATH="/env/bin:$PATH"
COPY entrypoint.sh /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh


# AJOUTER LE FICHIER SHELL

COPY requirements.txt .

# Mettre à jour pip + installer dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le reste du projet
COPY . .

# Copier entrypoint
COPY entrypoint.sh /app/entrypoint.sh

# Optionnel (Linux)
# RUN chmod +x /app/entrypoint.sh