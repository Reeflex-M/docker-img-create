C'est parti ! Comme pour Gitleaks, je vais te guider pas à pas pour réaliser ce TP sur **OpenSSF Scorecard** directement sur ta machine **Debian**.

Ce TP est divisé en deux parties : l'installation/utilisation de l'outil en ligne de commande (CLI), puis l'amélioration d'un projet pour augmenter son score.

### Étape 1 : Installation sur Debian

Nous allons récupérer la dernière version binaire comme indiqué à la page 4 du document.

1. Ouvre ton terminal.
2. Exécute ce bloc de commandes pour télécharger et installer l'outil :
```bash
# 1. Récupérer le numéro de la dernière version
VERSION=$(curl -s "https://api.github.com/repos/ossf/scorecard/releases/latest" | grep "tag_name" | sed -e 's/.*"v\([^"]\+\)".*/\1/')

# 2. Télécharger et extraire
# Note : Le nom du fichier extrait dépend souvent de l'architecture, on va lister après extraction.
curl -sSL "https://github.com/ossf/scorecard/releases/download/v${VERSION}/scorecard_${VERSION}_linux_amd64.tar.gz" | tar -xz

# 3. Déplacer le binaire (le nom du fichier extrait est généralement 'scorecard-linux-amd64')
sudo mv scorecard-linux-amd64 /usr/local/bin/scorecard

# 4. Vérifier l'installation
scorecard version

```



### Étape 2 : Analyser un projet existant

Avant de créer le nôtre, regardons comment Scorecard note un projet populaire (ex: Node.js), comme suggéré page 5.

Note : Sans token GitHub, tu risques d'être limité par l'API (Rate Limiting). Si la commande échoue, il faudra créer un Personal Access Token sur GitHub et faire `export GITHUB_AUTH_TOKEN=ton_token`.

1. Lance l'analyse :
```bash
scorecard --repo=github.com/nodejs/node

```


2. Observe le résultat. Tu verras une note globale (ex: 7.8/10) et le détail par catégorie (Binary-Artifacts, Code-Review, etc.).



---

### Étape 3 : Créer un projet "mauvais élève"

Nous allons créer un dépôt minimaliste qui aura forcément un mauvais score, pour pouvoir l'améliorer ensuite.

1. **Sur ton compte GitHub (via le navigateur) :**
* Crée un nouveau repository public nommé `scorecard-demo`.
* Ne l'initialise pas (pas de README, pas de licence pour l'instant).


2. **Sur ton terminal Debian :**
```bash
# Créer le dossier local
mkdir scorecard-demo && cd scorecard-demo

# Ajouter un contenu minimal
echo "# Scorecard Demo" > README.md
echo "node_modules/" > .gitignore
npm init -y  # Crée un package.json par défaut (nécessite npm, sinon crée le fichier manuellement)

# Initialiser Git et lier à GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
# Remplace USERNAME par ton pseudo GitHub ci-dessous
git remote add origin https://github.com/USERNAME/scorecard-demo.git
git push -u origin main

```


3. **Analyser ce nouveau projet :**
```bash
# Remplace USERNAME par ton pseudo
scorecard --repo=github.com/USERNAME/scorecard-demo

```



**Résultat attendu :** Un score très bas (2 ou 3/10).



---

### Étape 4 : Améliorer le score (Quick Wins)

Nous allons gagner des points faciles en ajoutant des fichiers standards de sécurité.

#### A. Ajouter une politique de sécurité (Security Policy)

Cela permet de gagner 10/10 sur le critère "Security-Policy".

1. Crée le fichier `SECURITY.md` :
```bash
cat > SECURITY.md << 'EOF'
# Security Policy

## Supported Versions
| Version | Supported |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability
Please report security vulnerabilities to: security@example.com
We will respond within 48 hours.
EOF

```


2. Commit et Push :
```bash
git add SECURITY.md
git commit -m "Add security policy"
git push

```



#### B. Ajouter une Licence

Cela permet de gagner 10/10 sur le critère "License".

1. Télécharge une licence MIT :
```bash
curl -sSL https://opensource.org/license/mit > LICENSE

```


2. Commit et Push :
```bash
git add LICENSE
git commit -m "Add MIT license"
git push

```



---

### Étape 5 : Automatisation avec GitHub Actions

Pour que le score soit calculé automatiquement et affiché, nous allons configurer un Workflow.

1. Crée le dossier des workflows :
```bash
mkdir -p .github/workflows

```


2. Crée le fichier `.github/workflows/scorecard.yml`.


Copie-colle le contenu suivant (basé sur la page 12 ) :


```yaml
name: OpenSSF Scorecard
on:
  push:
    branches: [main]
  schedule:
    - cron: '30 6 * * 1' # Lundi matin

permissions: read-all

jobs:
  analysis:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      id-token: write
      contents: read
      actions: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Run Scorecard
        uses: ossf/scorecard-action@v2
        with:
          results_file: results.sarif
          results_format: sarif
          publish_results: true

      - name: Upload results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif

```


3. Envoie le workflow sur GitHub :
```bash
git add .github/workflows/scorecard.yml
git commit -m "Add Scorecard workflow"
git push

```



---

### Étape 6 : Le Badge de fierté

Une fois que l'action aura tourné (tu peux vérifier dans l'onglet "Actions" de ton repo GitHub), tu pourras ajouter le badge.

1. Modifie ton `README.md` pour ajouter le badge:


```markdown
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/USERNAME/scorecard-demo/badge)](https://securityscorecards.dev/viewer/?uri=github.com/USERNAME/scorecard-demo)

```


*(N'oublie pas de remplacer `USERNAME` par ton pseudo)*.
2. Une dernière fois : `git add`, `git commit`, `git push`.

Dis-moi quand tu as réussi l'installation (Étape 1), et nous pourrons analyser tes résultats ensemble !