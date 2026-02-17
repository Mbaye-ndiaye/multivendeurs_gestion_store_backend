# Guide : Tester les Endpoints Vendeurs dans Postman

## 📋 Table des matières
1. [Prérequis](#prérequis)
2. [Obtenir un Token d'Authentification](#obtenir-un-token-dauthentification)
3. [Configuration Postman](#configuration-postman)
4. [Endpoints Disponibles](#endpoints-disponibles)
5. [Exemples de Requêtes](#exemples-de-requêtes)

---

## 🔧 Prérequis

1. **Serveur Django en cours d'exécution** :
   ```bash
   python manage.py runserver
   ```
   Le serveur sera accessible sur `http://127.0.0.1:8000`

2. **Un compte superAdmin créé** :
   ```bash
   python manage.py createsuperuser
   ```

3. **Postman installé** : [Télécharger Postman](https://www.postman.com/downloads/)

---

## 🔑 Obtenir un Token d'Authentification

### Méthode 1 : Via le Shell Django (Recommandé)

1. Ouvrir le shell Django :
   ```bash
   python manage.py shell
   ```

2. Exécuter ce code :
   ```python
   from rest_framework.authtoken.models import Token
   from api.models import User
   
   # Récupérer votre utilisateur superAdmin
   user = User.objects.get(email='votre_email@example.com')
   
   # Créer ou récupérer le token
   token, created = Token.objects.get_or_create(user=user)
   
   print(f"Token: {token.key}")
   print(f"Utilisateur: {user.email}")
   print(f"Type: {user.user_type}")
   ```

3. **Copier le token** affiché (ex: `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`)

### Méthode 2 : Créer un Endpoint pour obtenir le Token (Optionnel)

Si vous voulez créer un endpoint pour obtenir le token, ajoutez ceci dans `api/views.py` :

```python
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'user_type': user.user_type
        })
```

Puis ajoutez dans `api/urls.py` :
```python
path('auth/login/', views.CustomAuthToken.as_view(), name='api-auth-login'),
```

---

## ⚙️ Configuration Postman

### 1. Créer une Collection

1. Ouvrir Postman
2. Cliquer sur **"New"** → **"Collection"**
3. Nommer la collection : **"Gestion Stock API"**

### 2. Configurer les Variables d'Environnement

1. Cliquer sur **"Environments"** (icône œil en haut à droite)
2. Créer un nouvel environnement : **"Local Development"**
3. Ajouter ces variables :
   - `base_url` : `http://127.0.0.1:8000`
   - `token` : `VOTRE_TOKEN_ICI` (à remplacer après avoir obtenu le token)

### 3. Configurer l'Authentification Globale

1. Dans votre collection, aller dans **"Authorization"**
2. Type : **"Bearer Token"**
3. Token : `{{token}}` (utilise la variable d'environnement)

---

## 📍 Endpoints Disponibles

### Base URL
```
http://127.0.0.1:8000/api/vendeurs/
```

### Endpoints

| Méthode | URL | Description | Permissions |
|---------|-----|-------------|-------------|
| `GET` | `/api/vendeurs/` | Liste tous les vendeurs | Authentifié |
| `POST` | `/api/vendeurs/` | Crée un vendeur | Admin/SuperAdmin |
| `GET` | `/api/vendeurs/<id>/` | Détails d'un vendeur | Authentifié |
| `PUT` | `/api/vendeurs/<id>/` | Modifie un vendeur | Authentifié |
| `DELETE` | `/api/vendeurs/<id>/` | Supprime un vendeur | Admin/SuperAdmin |

---

## 📝 Exemples de Requêtes

### 1. GET - Lister tous les vendeurs

**Configuration Postman :**
- **Méthode** : `GET`
- **URL** : `{{base_url}}/api/vendeurs/`
- **Headers** :
  ```
  Authorization: Token {{token}}
  Content-Type: application/json
  ```

**Réponse attendue (200 OK) :**
```json
[
  {
    "id": 1,
    "nom": "Doe",
    "prenom": "John",
    "email": "john@example.com",
    "telephone": "+221771234567",
    "adresse": "123 Rue Example",
    "pays": "Sénégal",
    "nom_de_la_boutique": "Boutique John",
    "domaine": "Électronique",
    "devise": "XOF",
    "is_active": true,
    "created_at": "2026-02-16T20:00:00Z"
  }
]
```

---

### 2. POST - Créer un vendeur

**Configuration Postman :**
- **Méthode** : `POST`
- **URL** : `{{base_url}}/api/vendeurs/`
- **Headers** :
  ```
  Authorization: Token {{token}}
  Content-Type: application/json
  ```
- **Body** (raw JSON) :
  ```json
  {
    "nom": "Dupont",
    "prenom": "Marie",
    "email": "marie.dupont@example.com",
    "telephone": "+221775432109",
    "adresse": "456 Avenue Test",
    "pays": "Sénégal",
    "nom_de_la_boutique": "Boutique Marie",
    "domaine": "Mode",
    "devise": "XOF"
  }
  ```

**Réponse attendue (201 Created) :**
```json
{
  "id": 2,
  "nom": "Dupont",
  "prenom": "Marie",
  "email": "marie.dupont@example.com",
  "telephone": "+221775432109",
  "adresse": "456 Avenue Test",
  "pays": "Sénégal",
  "nom_de_la_boutique": "Boutique Marie",
  "domaine": "Mode",
  "devise": "XOF",
  "is_active": true,
  "created_at": "2026-02-16T21:00:00Z",
  "message": "Vendeur créé avec succès",
  "password_generated": "Abc123!@#"
}
```

**⚠️ Note** : Le mot de passe généré est retourné dans la réponse (à retirer en production).

**Erreur possible (403 Forbidden) :**
```json
{
  "message": "Vous n'êtes pas autorisé à ajouter un vendeur"
}
```
→ Vérifiez que votre utilisateur a `user_type == 'admin'` ou `'superadmin'`

---

### 3. GET - Détails d'un vendeur

**Configuration Postman :**
- **Méthode** : `GET`
- **URL** : `{{base_url}}/api/vendeurs/1/` (remplacer `1` par l'ID du vendeur)
- **Headers** :
  ```
  Authorization: Token {{token}}
  Content-Type: application/json
  ```

**Réponse attendue (200 OK) :**
```json
{
  "id": 1,
  "nom": "Doe",
  "prenom": "John",
  "email": "john@example.com",
  "telephone": "+221771234567",
  "adresse": "123 Rue Example",
  "pays": "Sénégal",
  "nom_de_la_boutique": "Boutique John",
  "domaine": "Électronique",
  "devise": "XOF",
  "is_active": true,
  "created_at": "2026-02-16T20:00:00Z"
}
```

**Erreur possible (404 Not Found) :**
```json
{
  "detail": "Not found."
}
```

---

### 4. PUT - Modifier un vendeur

**Configuration Postman :**
- **Méthode** : `PUT`
- **URL** : `{{base_url}}/api/vendeurs/1/`
- **Headers** :
  ```
  Authorization: Token {{token}}
  Content-Type: application/json
  ```
- **Body** (raw JSON) :
  ```json
  {
    "nom": "Doe",
    "prenom": "John",
    "email": "john.updated@example.com",
    "telephone": "+221771234567",
    "adresse": "789 Nouvelle Adresse",
    "pays": "Sénégal",
    "nom_de_la_boutique": "Boutique John Updated",
    "domaine": "Informatique",
    "devise": "XOF"
  }
  ```

**Réponse attendue (200 OK) :**
```json
{
  "id": 1,
  "nom": "Doe",
  "prenom": "John",
  "email": "john.updated@example.com",
  "telephone": "+221771234567",
  "adresse": "789 Nouvelle Adresse",
  "pays": "Sénégal",
  "nom_de_la_boutique": "Boutique John Updated",
  "domaine": "Informatique",
  "devise": "XOF",
  "is_active": true,
  "created_at": "2026-02-16T20:00:00Z"
}
```

---

### 5. DELETE - Supprimer un vendeur

**Configuration Postman :**
- **Méthode** : `DELETE`
- **URL** : `{{base_url}}/api/vendeurs/1/`
- **Headers** :
  ```
  Authorization: Token {{token}}
  Content-Type: application/json
  ```

**Réponse attendue (204 No Content)** : Pas de contenu dans la réponse

**Erreur possible (403 Forbidden) :**
```json
{
  "message": "Vous n'êtes pas autorisé à supprimer un vendeur"
}
```
→ Vérifiez que votre utilisateur a `user_type == 'admin'` ou `'superadmin'`

---

## 🔍 Vérification des Erreurs

### Erreur 401 Unauthorized
```
{
  "detail": "Authentication credentials were not provided."
}
```
**Solution** : Vérifiez que le header `Authorization: Token <votre_token>` est présent.

### Erreur 400 Bad Request
```json
{
  "email": ["This field is required."],
  "telephone": ["This field is required."]
}
```
**Solution** : Vérifiez que tous les champs requis sont présents dans le body JSON.

### Erreur 403 Forbidden
```json
{
  "message": "Vous n'êtes pas autorisé à ajouter un vendeur"
}
```
**Solution** : Vérifiez que votre utilisateur a `user_type == 'admin'` ou `'superadmin'`.

---

## 📋 Checklist de Test

- [ ] Obtenir un token d'authentification
- [ ] Configurer les variables d'environnement dans Postman
- [ ] Tester GET `/api/vendeurs/` (liste)
- [ ] Tester POST `/api/vendeurs/` (création - nécessite admin/superadmin)
- [ ] Tester GET `/api/vendeurs/<id>/` (détails)
- [ ] Tester PUT `/api/vendeurs/<id>/` (modification)
- [ ] Tester DELETE `/api/vendeurs/<id>/` (suppression - nécessite admin/superadmin)

---

## 💡 Astuces

1. **Sauvegarder les requêtes** : Créez une collection Postman pour réutiliser les requêtes
2. **Tests automatiques** : Utilisez l'onglet "Tests" dans Postman pour automatiser les vérifications
3. **Variables dynamiques** : Utilisez `{{base_url}}` et `{{token}}` pour faciliter les changements
4. **Export/Import** : Exportez votre collection pour la partager avec votre équipe

---

## 🐛 Dépannage

### Le token ne fonctionne pas
1. Vérifiez que le token est correctement copié
2. Vérifiez que le header est au format : `Authorization: Token <token>` (avec un espace)
3. Régénérez un nouveau token si nécessaire

### Erreur CORS
Si vous testez depuis un frontend, ajoutez dans `settings.py` :
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React
    "http://127.0.0.1:8000",
]
```

---

**Bon test ! 🚀**
