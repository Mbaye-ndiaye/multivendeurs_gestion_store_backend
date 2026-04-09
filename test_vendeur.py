#!/usr/bin/env python
import requests
import json

# Test de création d'un vendeur
data = {
    'email': 'testvendeur@example.com',
    'nom': 'Test',
    'prenom': 'Vendeur',
    'telephone': '770000000',
    'nom_de_la_boutique': 'Boutique Test'
}

try:
    response = requests.post('http://127.0.0.1:8000/api/vendeurs/', json=data)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'Erreur: {e}')
