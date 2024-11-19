# Python automatisation mesures LMG641 / Stage
Le programme a été réalisé intégralement en Python qui permet une connexion à l'outil Zes Zimmer Precision Power Analyzer LMG641 pour contrôler et automatiser les mesures faites par la machine sur un appareil électronique branché.
Le programme a été testé et fonctionne sous [Windows] ainsi que [Linux]

### Informations
Ce projet fait suite à une période de stage effectuée du 23/09/2024 au 10/01/2025. Il peut donc présenter quelques failles ou problèmes d'optimisations.

# Configuration & Mesures

Afin d'utiliser correctement le programme, il est d'abord nécessaire de correctement prendre en main l'outil de mesure LMG641. La connexion entre l'ordinateur et le LMG641 nécessite qu'ils soient tout deux reliés au même réseau et se fait grâce à l'adresse IP de la machine.

**Voici donc les étapes à vérifier :**
- Ordinateur branché au réseau
- LMG641 branché au réseau 
    - Sur la machine dans la partie setup appuyer sur le bouton "INSTRUMENT"
    - Vérifier que l'IP Address est bien disponible et récupérer celle-ci (exemple 169.254.6.217)

**Lancer une mesure classique :**
- Entrer la commande suivante lance une mesure classique avec __l'host par défaut 169.254.6.217__ : `python3 powerlog641.py`
    - En cas d'IP différente à celle par défaut : `python3 powerlog641.py -host XXX.XXX.X.XXX`

## Contributeurs

Jan de Cuveland --> Le code développé se base sur son travail ayant mis a disposition un socket déjà fait permettant le lien entre l'ordinateur et le LMG641