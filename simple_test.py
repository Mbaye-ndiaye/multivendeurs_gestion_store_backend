import requests

# Test simple pour voir si le serveur répond
try:
    response = requests.get('http://127.0.0.1:8000/api/login/')
    print(f'GET Login - Status: {response.status_code}')
    print(f'Headers: {response.headers.get("content-type")}')
    
    # Test POST avec données minimales
    data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    response = requests.post('http://127.0.0.1:8000/api/login/', json=data)
    print(f'POST Login - Status: {response.status_code}')
    print(f'Response: {response.text[:500]}')
    
    # Test création vendeur
    vendeur_data = {
        'email': 'testvendeur@example.com',
        'nom': 'Test',
        'prenom': 'Vendeur',
        'telephone': '770000000',
        'nom_de_la_boutique': 'Boutique Test'
    }
    
    response = requests.post('http://127.0.0.1:8000/api/vendeurs/', json=vendeur_data)
    print(f'POST Vendeur - Status: {response.status_code}')
    print(f'Response: {response.text[:500]}')
    
except Exception as e:
    print(f'Erreur: {e}')
