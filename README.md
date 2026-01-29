C'est un excellent TP pour apprendre à sécuriser la chaîne de développement (Supply Chain Security). Puisque tu es sous **Debian**, nous allons suivre les instructions spécifiques pour Linux présentes dans le document.

Voici le guide étape par étape pour réaliser ce TP.

### Étape 1 : Installation de Gitleaks sur Debian

Comme indiqué dans le TP, nous allons récupérer le binaire officiel plutôt que d'utiliser Homebrew (macOS).

1. Ouvre ton terminal.
2. Assure-toi d'avoir `curl` et `tar` (généralement installés par défaut, mais au cas où) :
```bash
sudo apt update && sudo apt install curl tar -y

```


3. Exécute les commandes suivantes pour télécharger et installer la dernière version:


```bash
# Récupérer le numéro de la dernière version
VERSION=$(curl -s "https://api.github.com/repos/gitleaks/gitleaks/releases/latest" | grep "tag_name" | sed -E 's/.*"v([^"]+)".*/\1/')

# Télécharger et extraire
curl -sSL "https://github.com/gitleaks/gitleaks/releases/download/v${VERSION}/gitleaks_${VERSION}_linux_x64.tar.gz" | tar -xz

# Déplacer le binaire dans le PATH pour pouvoir l'utiliser partout
sudo mv gitleaks /usr/local/bin/

```


4. Vérifie que l'installation a réussi:


```bash
gitleaks version

```



---

### Étape 2 : Préparation de l'environnement de test

Nous allons créer un dépôt Git et y placer volontairement des secrets pour tester l'outil.

1. Crée le dossier et initialise Git :
```bash
mkdir gitleaks-demo && cd gitleaks-demo
git init

```


2. Crée un fichier `config.js` contenant des faux identifiants AWS et GitHub:


```bash
cat > config.js << 'EOF'
// Configuration de l'application
const config = {
    apiKey: "AKIAIOSFODNN7EXAMPLE",
    secretkey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    dbPassword: "super_secret_password_123",
    githubToken: "ghp_xxxxxxxXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
};
module.exports = config;
EOF

```


3. Valide ce fichier dans l'historique Git (Commit):


```bash
git add .
git commit -m "Add config"

```



---

### Étape 3 : Lancer un scan de détection

Maintenant que le "mal est fait" (les secrets sont committés), nous allons demander à Gitleaks de scanner le répertoire.

1. Lance la commande de détection:


```bash
gitleaks detect --source . -v

```


* `detect` : Scanne le dossier.
* `-v` : Mode verbeux pour voir les détails.



**Résultat attendu :** Tu devrais voir des alertes rouges indiquant "Finding". Gitleaks a identifié `aws-access-key-id`, `aws-secret-access-key`, etc..

---

### Étape 4 : Mettre en place la protection (Pre-commit Hook)

L'objectif est d'empêcher les futurs commits s'ils contiennent des secrets. Nous allons utiliser la méthode manuelle décrite dans le TP, qui est simple et efficace.

1. Crée le fichier du hook dans le dossier caché `.git`:


```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
gitleaks protect --staged -v
EOF

```


*Note : La commande `protect` vérifie ce qui est sur le point d'être committé (`--staged`), contrairement à `detect` qui vérifie l'historique existant.*
2. Rends ce script exécutable:


```bash
chmod +x .git/hooks/pre-commit

```



---

### Étape 5 : Vérifier le blocage

Testons si le système de protection fonctionne en essayant d'ajouter un nouveau secret (une fausse clé Stripe).

1. Ajoute un secret dans un nouveau fichier :
```bash
echo 'STRIPE_KEY="sk..' >> secrets.txt 

```


2. Essaie de committer ce fichier:


```bash
git add secrets.txt
git commit -m "Add stripe key"

```



**Résultat attendu :**
Le commit doit échouer ! Tu devrais voir un message d'erreur : `error: gitleaks has detected sensitive information in your changes.`. Le fichier `secrets.txt` reste en zone de staging ("staged") et n'est pas enregistré dans l'historique.

---

### Étape 6 : Gérer les exceptions (Allowlist)

Parfois, tu as besoin de committer un faux secret (pour des tests) ou Gitleaks fait une erreur (faux positif). Le TP montre comment ignorer une ligne spécifique.

1. Modifie le fichier `secrets.txt` pour ajouter un commentaire d'exemption:


* Ouvre le fichier avec `nano secrets.txt` (ou un autre éditeur).
* Modifie la ligne pour qu'elle ressemble à ceci :
```text
STRIPE_KEY="sk_live_xxxxxxXXXXXXXXXXXXXXX" // gitleaks:allow

```


* Sauvegarde et quitte.


2. Retente le commit :
```bash
git add secrets.txt
git commit -m "Add stripe key with allowlist"

```



Cette fois, le commit devrait passer car tu as explicitement autorisé ce secret.

---

### Résumé

Tu as réussi à :

1. Installer Gitleaks sur Debian.
2. Scanner un historique Git pour trouver des fuites passées.
3. Installer un "garde-fou" (hook) pour empêcher les futures fuites.

**Souhaites-tu que je t'explique comment configurer la partie "GitHub Actions" (Page 9) pour automatiser cela sur un serveur distant ?**