# Gestion de flotte automobile de la mairie de Port-Bouët

Ce document explique en détail les étapes nécessaires pour configurer et lancer votre projet Django.

---

## Prérequis

1. **Python 3.x.x**
   - Assurez-vous que Python 3 est installé sur votre machine. Vous pouvez vérifier la version installée avec la commande :
     ```bash
     python3 --version
     ```

2. **pip**
   - pip est généralement installé avec Python. Vérifiez sa présence avec :
     ```bash
     pip --version
     ```

3. **Git** (optionnel mais recommandé)
   - Si vous travaillez avec un dépôt Git, assurez-vous que Git est installé.

---

## Configuration de l'Environnement

### 1. Création d'un Environnement Virtuel
Un environnement virtuel vous permet de gérer les dépendances de votre projet sans interférer avec les autres projets.

- Créez un environnement virtuel :
  ```bash
  python3 -m venv env
  ```

- Activez l'environnement virtuel :
  - **Sous Linux/macOS :**
    ```bash
    source env/bin/activate
    ```
  - **Sous Windows :**
    ```bash
    .\env\Scripts\activate
    ```

- Vous saurez que l'environnement est activé car le nom de celui-ci apparaît dans votre terminal.

### 2. Installation des Dépendances
- Assurez-vous que le fichier `requirements.txt` est présent à la racine de votre projet.
- Installez les dépendances :
  ```bash
  pip install -r requirements.txt
  ```

---

## Architecture du Projet

```
ges_auto
|
|-- ges_auto
|-- pages
|-- static
    |-- assets
         |-- //
|-- templates
    |-- bases
        |-- base.html
    |-- //
```

---

## Configuration de la Base de Données

1. Appliquez les migrations initiales pour configurer la base de données :
   ```bash
   python manage.py migrate
   ```

2. Créez un superutilisateur pour accéder à l'interface d'administration :
   ```bash
   python manage.py createsuperuser
   ```
   - Fournissez un nom d'utilisateur, une adresse email, et un mot de passe lorsque vous y êtes invité.

---

## Lancement du Serveur de Développement

1. Exécutez le serveur Django :
   ```bash
   python manage.py runserver
   ```

2. Accédez au serveur local via votre navigateur web à l'adresse suivante :
   ```
   http://127.0.0.1:8000/
   ```

---

## Commandes Utiles

- **Collecter les fichiers statiques (pour la production) :**
  ```bash
  python manage.py collectstatic
  ```

- **Effectuer des tests unitaires :**
  ```bash
  python manage.py test
  ```

---

## Notes Complémentaires

- **Fichier `.env` :** Si votre projet utilise des variables d'environnement, créez un fichier `.env` et ajoutez-y les informations nécessaires.
- **Extensions recommandées pour VS Code :**
  - Python
  - Django
  - .env

---

Votre projet Django est maintenant configuré et prêt à être utilisé !

