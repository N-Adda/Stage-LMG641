# Python automatisation mesures LMG641 / Stage
Le programme a été réalisé intégralement en Python qui permet une connexion à l'outil Zes Zimmer Precision Power Analyzer LMG641 pour contrôler et automatiser les mesures faites par la machine sur un appareil électronique branché.
Le programme a été testé et fonctionne sous [Windows] ainsi que [Linux]

[Windows]: https://www.microsoft.com/fr-fr/windows?r=1 "Windows"
[Linux]: https://www.linux.org/ "Linux"

### Informations
Ce projet fait suite à une période de stage effectuée du 23/09/2024 au 10/01/2025. Il peut donc présenter quelques failles ou problèmes d'optimisations.

# Configuration & Mesures

Afin d'utiliser correctement le programme, il est d'abord nécessaire de correctement prendre en main l'outil de mesure LMG641. La connexion entre l'ordinateur et le LMG641 nécessite qu'ils soient tout deux reliés au même réseau et se fait grâce à l'adresse IP de la machine.

**Voici donc les étapes à vérifier :**
- Ordinateur branché au réseau
- LMG641 branché au réseau 
    - Sur la machine dans la partie setup appuyer sur le bouton "INSTRUMENT"
    - Vérifier que l'IP Address de l'host est bien disponible et récupérer celle-ci (exemple 169.254.6.217)

**Lancer une mesure classique :**
- Entrer la commande suivante lance une mesure classique avec __l'host par défaut 169.254.6.217__ : `python3 powerlog641.py`
    - En cas d'IP différente à celle par défaut : `python3 powerlog641.py -host XXX.XXX.X.XXX`
    
La console devrait alors afficher le nombres de cycles de mesures et une fenêtre graphique devrait s'ouvrir durant la mesure donnant un aperçu visuel de celle-ci, avec la possibilité de déplacer le curseur de la souris pour y afficher les valeurs en abscisses et ordonnées. La fenêtre graphique se fermera lorsque le programme aura fini ses cycles de mesures et sera remplacé par un dossier crée automatiquement dans l'espace de travail contenant deux fichiers :
    - Un fichier Excel répétoriant les valeurs numériques mesurées au travers des cycles
    - Un fichier PNG affichant une capture visuelle des derniers graphes à la fin des cycles.

## Contributeurs

Jan de Cuveland --> Le code développé se base sur son travail ayant mis a disposition un socket déjà fait permettant le lien entre l'ordinateur et le LMG641