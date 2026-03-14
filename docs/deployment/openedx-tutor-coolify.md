# Documentation Complete: Open edX avec Tutor sur Serveur Coolify

## Objectif
Deployer Open edX (fork perso) avec Tutor sur un serveur Ubuntu ou Coolify est deja installe, en separant proprement l'environnement Open edX.

## Prerequis
- Serveur Linux (Ubuntu 22.04/24.04 recommande)
- Ressources conseillees: 8 vCPU, 16 Go RAM, 120 Go SSD minimum
- DNS configure:
  - `lms.votre-domaine.tld`
  - `studio.votre-domaine.tld`
- Acces sudo/root

## 1. Preparation systeme
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release python3-pip git
```

Installer Docker (si non present):
```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Installer Tutor:
```bash
sudo pip3 install --break-system-packages --ignore-installed "tutor[full]"
```

## 2. Creer un environnement dedie Open edX
```bash
sudo mkdir -p /opt/tutor
sudo chown -R $USER:$USER /opt/tutor
echo 'export TUTOR_ROOT=/opt/tutor' >> ~/.bashrc
export TUTOR_ROOT=/opt/tutor
```

## 3. Cloner le fork Open edX
```bash
mkdir -p /opt/tutor/src
git clone https://github.com/kof70/openedx-platform.git /opt/tutor/src/openedx
```

## 4. Configurer Tutor
### Cas A (recommande): Tutor gere son proxy Caddy (SSL natif Tutor)
```bash
tutor config save \
  --set LMS_HOST=lms.votre-domaine.tld \
  --set CMS_HOST=studio.votre-domaine.tld \
  --set MOUNT_EDX_PLATFORM=/opt/tutor/src/openedx
```

### Cas B (avance): Coolify/Traefik gere le SSL en frontal
Si tu veux absolument faire terminer TLS par Coolify:
```bash
tutor config save \
  --set LMS_HOST=lms.votre-domaine.tld \
  --set CMS_HOST=studio.votre-domaine.tld \
  --set WEB_PROXY=false \
  --set ENABLE_HTTPS=false \
  --set CADDY_HTTP_PORT=81 \
  --set CADDY_HTTPS_PORT=444 \
  --set MOUNT_EDX_PLATFORM=/opt/tutor/src/openedx
```
Puis configurer Traefik pour router `lms.*` et `studio.*` vers le port Tutor choisi.

## 5. Lancer Open edX
```bash
tutor local launch -I
```
Cette commande telecharge les images, initialise les services et les bases.

## 6. Creer l'utilisateur admin
```bash
tutor local do createuser --staff --superuser kof70 djakpakoffi7029@gmail.com
```
Note securite: n'utilise pas `--password` en clair en prod. Definis le mot de passe interactivement.

## 7. URLs d'acces
- LMS: `https://lms.votre-domaine.tld`
- Studio: `https://studio.votre-domaine.tld`

## 8. Workflow de developpement (live)
Ton code est monte depuis `/opt/tutor/src/openedx` via `MOUNT_EDX_PLATFORM`.

1. Modifier le code dans `/opt/tutor/src/openedx`
2. Appliquer les changements:
```bash
tutor local restart lms cms
```
3. Si changement front/assets:
```bash
tutor local do lms ./manage.py lms collectstatic --noinput
tutor local do cms ./manage.py cms collectstatic --noinput
```

## 9. Que faire apres chaque `git pull` ?
### Reponse courte
Non, tu ne relances pas `tutor local launch -I` a chaque fois.

### Procedure apres pull
```bash
cd /opt/tutor/src/openedx
git pull origin master
```
Puis selon type de changement:

- Code Python/Django seulement:
```bash
tutor local restart lms cms
```

- Migrations Django detectees:
```bash
tutor local do lms ./manage.py lms migrate
tutor local do cms ./manage.py cms migrate
tutor local restart lms cms
```

- Frontend/assets modifies:
```bash
tutor local do lms ./manage.py lms collectstatic --noinput
tutor local do cms ./manage.py cms collectstatic --noinput
tutor local restart lms cms
```

- Si changement majeur Tutor/config:
```bash
tutor config save
tutor local launch -I
```

## 10. Commandes utiles
```bash
# Stopper la plateforme
tutor local stop

# Demarrer la plateforme
tutor local start -d

# Etat des services
tutor local status

# Logs LMS
tutor local logs --tail=200 -f lms

# Shell Django LMS
tutor local run lms ./manage.py lms shell
```

## 11. Sauvegarde minimale recommandee
- Sauvegarder regulierement:
  - `/opt/tutor` (config + env)
  - volumes Docker de MySQL/Mongo
- Avant mise a jour importante:
  - snapshot VM
  - backup DB

## 12. Points d'attention
- Open edX est lourd: surveiller CPU/RAM/disque.
- Eviter de melanger trop d'apps lourdes sur le meme host Coolify.
- Privilegier un serveur dedie Open edX des que possible.
