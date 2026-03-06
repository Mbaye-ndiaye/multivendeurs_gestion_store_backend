# Récapitulatif : configuration envoi d’emails

## Comparaison des deux projets

### backend_easymarket_multivendor

| Élément | Valeur |
|--------|--------|
| **Fichier** | `backend/settings.py` |
| **EMAIL_BACKEND** | `django.core.mail.backends.smtp.EmailBackend` |
| **EMAIL_HOST** | `smtp.gmail.com` |
| **EMAIL_USE_TLS** | `True` |
| **EMAIL_PORT** | `587` |
| **EMAIL_HOST_USER** | `noreply.easymarket@gmail.com` (fixe en settings) |
| **EMAIL_HOST_PASSWORD** | `os.environ.get('EMAIL_HOST_PASSWORD')` |
| **EMAIL_USE_SSL** | `False` |
| **EMAIL_TIMEOUT** | `20` |
| **EMAIL_SSL_KEYFILE** | `None` |
| **EMAIL_SSL_CERTFILE** | `None` |
| **APP_NAME** | `env["APP_NAME"]` (depuis .env) |
| **Envoi** | `api/notifications.py` → `Notif.send_email(APP_NAMES, subject, to, template_src, context_dict)` avec `EmailMultiAlternatives`, HTML + texte, `from_email = f'{APP_NAMES} <{settings.EMAIL_HOST_USER}>'` |

### gestion_stock_backend (avant alignement)

| Élément | Valeur |
|--------|--------|
| **EMAIL_HOST_USER** | `noreply.babacarndiay546@gmail.com` (fixe) |
| **APP_NAME** | Absent des settings (défaut dans `notifications.py`) |
| **EMAIL_SSL_KEYFILE / CERTFILE** | Absents |
| **Envoi** | 2 modules : `email_utils.send_vendeur_credentials()` (plain text, `send_mail`) et `notifications.send_email()` (HTML, `EmailMultiAlternatives`) |
| **USE_CONSOLE_EMAIL** | Présent (mode console si True) |

## Différences principales

1. **APP_NAME** : easymarket le lit depuis `env["APP_NAME"]` ; gestion_stock n’avait pas de variable dédiée en settings.
2. **EMAIL_HOST_USER** : easymarket utilise une adresse dédiée (noreply.easymarket) ; gestion_stock une autre adresse en dur.
3. **SSL** : easymarket définit explicitement `EMAIL_SSL_KEYFILE` et `EMAIL_SSL_CERTFILE` à `None`.
4. **Envoi** : easymarket centralise tout dans `Notif.send_email` (template HTML) ; gestion_stock avait en plus un envoi en texte seul dans `email_utils`.

## Configuration appliquée (alignée sur backend_easymarket_multivendor)

- **APP_NAME** : lu depuis `env` avec valeur par défaut si absent.
- **EMAIL_*** : même schéma que easymarket (SMTP Gmail, TLS, port 587, timeout 20, SSL key/cert à `None`).
- **EMAIL_HOST_USER** : depuis `os.environ.get('EMAIL_HOST_USER', '...')` pour pouvoir le définir dans `.env` comme le mot de passe.
- **email_utils** : même format d’expéditeur que easymarket : `f'{APP_NAME} <{settings.EMAIL_HOST_USER}>'`.

Voir `backend/settings.py` et `api/email_utils.py` pour le détail.
