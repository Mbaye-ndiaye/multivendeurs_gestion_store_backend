# Configuration de l'envoi d'emails - Gestio-Stock

## Variables à ajouter dans votre fichier `.env`

Pour activer l'envoi d'emails (notamment le mot de passe aux vendeurs créés), ajoutez les variables suivantes dans votre fichier `.env` à la racine du projet backend :

```env
# Configuration Email (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply.gestio-stock@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_application

# Optionnel : nom de l'application affiché dans les emails
APP_NAME=Gestio-Stock
```

## Configuration Gmail

1. **Activer la validation en 2 étapes** sur votre compte Google
2. **Créer un mot de passe d'application** :
   - Aller sur [Google Account Security](https://myaccount.google.com/security)
   - Sélectionner "Validation en 2 étapes" → "Mots de passe des applications"
   - Générer un mot de passe pour "Mail"
   - Utiliser ce mot de passe dans `EMAIL_HOST_PASSWORD`

3. Ne jamais mettre le mot de passe réel de votre compte Gmail dans `.env`

## Alternative : Mailtrap (si Gmail ne fonctionne pas)

**Si l'erreur 535 persiste avec Gmail**, utilisez Mailtrap (gratuit, sans mot de passe d'application) :

1. Créez un compte sur [mailtrap.io](https://mailtrap.io)
2. Allez dans **Email Testing** → **Inboxes** → choisissez une inbox
3. Cliquez sur **SMTP Settings** et copiez les identifiants
4. Dans votre `.env` :

```env
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=votre_username_mailtrap
EMAIL_HOST_PASSWORD=votre_password_mailtrap
```

Les emails apparaîtront dans votre inbox Mailtrap (pas chez le destinataire réel). Idéal pour tester.

## Tester la configuration

```bash
python manage.py test_email kheud@gmail.com
```

Cette commande affiche la config actuelle et tente d'envoyer un email.

## Vérification

Une fois configuré, créez un vendeur via le dashboard SuperAdmin. Le vendeur recevra un email avec :
- Son adresse email de connexion
- Son mot de passe généré automatiquement
