# API de Création de Comptes Vendeurs

## Overview

Cette API permet de créer des comptes vendeurs avec génération automatique de mot de passe et envoi des identifiants par email, similaire à l'implémentation d'easymarket_multivendor.

## Endpoint

### POST /api/vendeurs/

Crée un nouveau compte vendeur avec mot de passe généré automatiquement.

#### Corps de la requête (JSON)

```json
{
    "email": "vendeur@example.com",
    "nom": "Nom du vendeur",
    "prenom": "Prénom du vendeur", 
    "telephone": "770000000",
    "nom_de_la_boutique": "Nom de la boutique"
}
```

#### Champs obligatoires

- `email`: Email unique du vendeur
- `nom`: Nom du vendeur
- `prenom`: Prénom du vendeur
- `telephone`: Numéro de téléphone
- `nom_de_la_boutique`: Nom de la boutique

#### Champs optionnels

- `adresse`: Adresse du vendeur
- `pays`: Pays du vendeur
- `couleur`: Couleur thème de la boutique
- `domaine`: Domaine personnalisé
- `devise`: Devise (XOF, EUR, USD) - défaut: XOF

#### Réponse réussie (201 Created)

```json
{
    "id": 89,
    "user_type": "VENDEUR",
    "slug": "5589f303-3415-11f1-854e-3868938b97e5",
    "nom": "Test",
    "prenom": "Vendeur",
    "email": "testvendeur@example.com",
    "telephone": "770000000",
    "nom_de_la_boutique": "Boutique Test",
    "is_active": true,
    "created_at": "2026-04-09T13:07:00Z"
}
```

## Fonctionnalités

### Génération automatique du mot de passe

- Le mot de passe est généré automatiquement avec 8 caractères minimum
- Inclut: majuscules, minuscules, chiffres, caractères spéciaux
- Le mot de passe est hashé avant sauvegarde

### Envoi d'email

- Un email est automatiquement envoyé au vendeur avec ses identifiants
- Sujet: "Vos identifiants - Espace vendeur"
- Contient: email et mot de passe généré
- Message recommande de changer le mot de passe à la première connexion

### Configuration email

L'envoi d'email nécessite la configuration des variables suivantes dans `.env`:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=votre_email@gmail.com
```

## Exemple d'utilisation

### Python avec requests

```python
import requests

data = {
    'email': 'nouveau.vendeur@example.com',
    'nom': 'Doe',
    'prenom': 'John',
    'telephone': '770123456',
    'nom_de_la_boutique': 'Super Boutique'
}

response = requests.post('http://127.0.0.1:8000/api/vendeurs/', json=data)

if response.status_code == 201:
    vendeur = response.json()
    print(f"Vendeur créé: {vendeur['email']}")
    print(f"ID: {vendeur['id']}")
    print(f"Boutique: {vendeur['nom_de_la_boutique']}")
else:
    print(f"Erreur: {response.status_code}")
    print(f"Détails: {response.text}")
```

### cURL

```bash
curl -X POST http://127.0.0.1:8000/api/vendeurs/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "vendeur@example.com",
    "nom": "Doe", 
    "prenom": "John",
    "telephone": "770123456",
    "nom_de_la_boutique": "Ma Boutique"
  }'
```

## Gestion des erreurs

### 400 Bad Request

```json
{
    "email": ["Cet email est déjà utilisé."],
    "telephone": ["Ce format de numéro n'est pas valide."]
}
```

### 500 Internal Server Error

Erreur serveur (généralement liée à la configuration email).

## Tests

Pour tester l'API:

```bash
# Démarrer le serveur
python manage.py runserver

# Tester avec le script fourni
python simple_test.py
```

## Notes importantes

1. **Configuration email**: L'envoi d'email nécessite une configuration SMTP valide
2. **Unicité**: L'email doit être unique dans le système
3. **Sécurité**: Les mots de passe sont hashés avec Django PBKDF2
4. **Permissions**: L'endpoint est public (pas d'authentification requise)
5. **Logging**: Les erreurs d'envoi d'email sont loguées mais ne bloquent pas la création

## Architecture

Les fichiers modifiés/ajoutés:

- `api/serializers.py`: `VendeurRegisterSerializer`
- `api/views.py`: `VendeurRegisterAPIListView`  
- `api/urls.py`: Route `/api/vendeurs/`
- `api/email_utils.py`: `send_vendeur_credentials()`

Cette implémentation est basée sur le système easymarket_multivendor avec adaptation pour le projet gestion_stock_backend.
