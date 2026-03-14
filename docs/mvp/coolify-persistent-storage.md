# Persistance des données sur Coolify (serveur alonu)

Objectif : ne perdre aucune donnée entre deux déploiements.

---

## 1. Deux cas selon le type d’application

| Type | Où la persistance se configure | Section Coolify "Storages" |
|------|---------------------------------|----------------------------|
| **Docker Compose** | Dans le fichier `docker-compose.yaml` avec des `volumes:` (ex. `./data/mysql:/var/lib/mysql`) | Souvent vide : les données sont dans le dossier de l’app sur le serveur |
| **Dockerfile / Docker Image / Nixpacks** | Dans l’interface Coolify : **Storages → Add** | C’est ici que tu ajoutes les chemins persistants |

Pour les apps **Docker Compose** (ex. openedx-platform), tant que le compose contient des volumes en `./data/...` et `./env/...`, Coolify conserve tout le répertoire du service entre déploiements — pas besoin d’ajouter des Storages dans la page.

Pour les apps **Dockerfile / Image / Nixpacks**, il faut ajouter manuellement chaque stockage persistant via **Storages → Add**.

---

## 2. Ajouter un Storage (apps Dockerfile / Image / Nixpacks)

1. Ouvre l’application dans Coolify.
2. Va dans l’onglet **Storages**.
3. Clique sur **Add**.
4. Renseigne :
   - **Name** : un libellé (ex. `storage`, `uploads`, `data`).
   - **Destination Path** : le chemin **dans le conteneur** où les données doivent vivre.  
     En Coolify le répertoire de base de l’app est souvent **`/app`**. Exemples :
     - `/app/storage` (Laravel)
     - `/app/public/uploads`
     - `/app/data`
     - `/app/var` (cache, logs, etc.)
5. Choisis **Volume** (stockage géré par Docker) ou **Bind Mount** (dossier sur l’hôte).
6. Sauvegarde.

Coolify ajoute automatiquement l’UUID de la ressource au nom du volume pour éviter les conflits entre projets.

---

## 3. Chemins à persister par type de projet (recommandations)

À utiliser comme **Destination Path** dans Storages (en gardant `/app` comme base si c’est le cas sur ton image).

- **Laravel / PHP**
  - `/app/storage` (logs, cache, sessions, uploads)
  - `/app/bootstrap/cache` (optionnel)
- **Node / Next / Nuxt**
  - `/app/.next/cache` ou équivalent si besoin
  - `/app/public/uploads` ou `/app/uploads` si tu stockes des fichiers
- **API / Backend (général)**
  - `/app/data` ou `/app/storage` selon le code
  - `/app/uploads` si upload de fichiers
- **Open edX (Docker Compose)**
  - Déjà géré par le compose : `./data/mysql`, `./data/redis`, `./data/mongodb`, `./data/lms`, `./data/cms`, `./data/openedx-media`, `./data/meilisearch`, `./data/caddy`. Rien à ajouter dans Storages.

---

## 4. Fiche par projet : exactement quoi faire

Pour chaque projet : ouvre l’app dans Coolify → onglet **Storages** → **Add**, puis ajoute les lignes indiquées (Name + Destination Path, type **Volume** sauf mention contraire).

---

### 1. agro-deal (Dockerfile)

- **Storages → Add**, puis ajouter :

| Name        | Destination Path   |
|------------|---------------------|
| `storage`  | `/app/storage`      |
| `bootstrap-cache` | `/app/bootstrap/cache` |

*(Si ton app est Node/Next et pas Laravel, remplace par `/app/data` ou `/app/.next/cache` selon ton code.)*

---

### 2. alonu-data-deletion (Static)

- **Rien à faire** : app statique, pas de données à persister.

---

### 3. coecept-backend-new (Dockerfile)

- **Storages → Add** :

| Name       | Destination Path |
|-----------|------------------|
| `storage` | `/app/storage`   |
| `bootstrap-cache` | `/app/bootstrap/cache` |

*(Si c’est une API Node/Python, utilise `/app/data` ou `/app/uploads` selon où le code écrit.)*

---

### 4. fedsport-wbsc (Dockerfile)

- **Storages → Add** :

| Name       | Destination Path |
|-----------|------------------|
| `storage` | `/app/storage`   |
| `bootstrap-cache` | `/app/bootstrap/cache` |

*(Adapter en `/app/data` ou `/app/uploads` si ce n’est pas Laravel.)*

---

### 5. iadessbackend (Dockerfile)

- **Storages → Add** :

| Name       | Destination Path |
|-----------|------------------|
| `storage` | `/app/storage`   |
| `bootstrap-cache` | `/app/bootstrap/cache` |

---

### 6. togo-fedsport-network (Dockerfile)

- **Storages → Add** :

| Name       | Destination Path |
|-----------|------------------|
| `storage` | `/app/storage`   |
| `bootstrap-cache` | `/app/bootstrap/cache` |

*(Ou `/app/data`, `/app/uploads` selon le stack.)*

---

### 7. coecept-frontend (Dockerfile)

- En général un front seul n’écrit pas de données côté conteneur.  
- **Si** tu as des uploads ou un cache persistant : **Storages → Add** → Name : `uploads` ou `data`, Destination : `/app/public/uploads` ou `/app/data`.  
- Sinon : **Rien à faire**.

---

### 8. administration-territoriale (Dockerfile)

- **Storages → Add** :

| Name       | Destination Path |
|-----------|------------------|
| `storage` | `/app/storage`   |
| `bootstrap-cache` | `/app/bootstrap/cache` |

---

### 9. iades frontend (Dockerfile)

- Comme frontend : **Rien à faire** sauf si tu as un dossier d’uploads → alors **Add** : Name `uploads`, Destination `/app/public/uploads` ou `/app/uploads`.

---

### 10. delivery-tracking (Dockerfile)

- **Storages → Add** :

| Name       | Destination Path |
|-----------|------------------|
| `storage` | `/app/storage`   |
| `bootstrap-cache` | `/app/bootstrap/cache` |

*(Ou `/app/data`, `/app/uploads` selon le framework.)*

---

### 11. alonu-backend (Dockerfile)

- **Storages → Add** :

| Name       | Destination Path |
|-----------|------------------|
| `storage` | `/app/storage`   |
| `bootstrap-cache` | `/app/bootstrap/cache` |

---

### 12. archivage-ministere (Dockerfile)

- **Storages → Add** :

| Name       | Destination Path |
|-----------|------------------|
| `storage` | `/app/storage`   |
| `data`    | `/app/data`      |
| `bootstrap-cache` | `/app/bootstrap/cache` |

*(Réduire à `storage` + `data` si pas Laravel.)*

---

### 13. alonu-frontend (Dockerfile)

- Frontend : **Rien à faire** sauf uploads → **Add** : Name `uploads`, Destination `/app/public/uploads`.

---

### 14. openedx-platform-mvp (Nixpacks)

- **Si** c’est l’app **Docker Compose** (plusieurs services : lms, cms, mysql, redis, etc.) : la persistance est déjà dans le `docker-compose.yaml` (`./data/...`, `./env/...`). **Rien à ajouter** dans Storages.
- **Si** c’est une **seule** image (un conteneur) : **Storages → Add** selon où l’app écrit, par ex. `data` → `/app/data`, `media` → `/app/media`.

---

### 15. archivage (Dockerfile)

- **Storages → Add** :

| Name       | Destination Path |
|-----------|------------------|
| `storage` | `/app/storage`   |
| `data`    | `/app/data`      |
| `bootstrap-cache` | `/app/bootstrap/cache` |

---

## 5. Résumé

- **Storages dans Coolify** = persistance pour les apps **non-Compose** (Dockerfile / Image / Nixpacks). Tu les crées à la main dans **Storages → Add** avec le bon **Destination Path** (souvent sous `/app/...`).
- **Docker Compose** = persistance via les `volumes:` du compose ; pas besoin de remplir la section Storages pour ces chemins.
- L’API Coolify utilisée ici ne permet pas de créer des Storages automatiquement ; l’ajout se fait dans l’interface Coolify.

Une fois un Storage ajouté pour chaque chemin critique de chaque projet, les redéploiements ne feront plus perdre ces données.
