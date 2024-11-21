# **Introduction : Automatisation mesures LMG641 en Python / Stage**
Le programme a été réalisé intégralement en Python qui permet une connexion à l'outil Zes Zimmer Precision Power Analyzer LMG641 pour contrôler et automatiser les mesures faites par la machine sur un appareil électronique branché.
Le programme a été testé et fonctionne sous [Windows] ainsi que [Linux]

[Windows]: https://www.microsoft.com/fr-fr/windows?r=1 "Windows"
[Linux]: https://www.linux.org/ "Linux"
[noms de variables valides]: var "var"

### **Informations**
Ce projet fait suite à une période de stage effectuée du 23/09/2024 au 10/01/2025. Il peut donc présenter quelques failles ou problèmes d'optimisations.
Il est important d'installer deux librairies utilisés dans le programme afin que celui-ci fonctionne :

- sudo apt install xlsxwriter
- sudo apt install matplotlib

# **Configuration & Mesures**

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

# **Fonctionnalités**
Le programme présente divers paramètres qui sont modifiables. Il est possible d'afficher les arguments via la commande `-help` dans un terminal. Cependant il est intéressant d'en connaître les détails :

- val --> Permet de définir les valeurs qu'on souhaite mesure via le LMG641. Par défaut si l'on ne rempli rien, le programme mesurera la tension, le courant ainsi que la puissance de l'appareil brancher au LMG641. Les valeurs mesurables sont affichés par le LMG641 dans la catégorie MEASUREMENT en appuyant sur "DEFAULT". A savoir qu'il est très important de saisir des [noms de variables valides] afin d'éviter tout problème de mesure. 
Cependant si vous souhaitez mesurer d'autres valeurs, il est possible d'utiliser l'arg val de façon suivante :
    - `python3 powerlog641.py "durnorm utrms itrms iac idc udc uac"` --> Le programme mesurera donc la période, la tension, le courant, le courant alternatif, la tension alternatif etc. . .


- lf (LOGFILE) --> Permet de définir un nom au fichier que l'on va créer. Utile en cas de mesure importante que l'on veut pouvoir retrouver plus facilement. Par défaut, le dossier crée ainsi que les fichiers possèdent comme nom la date et l'heure du jour.
    - `python3 powerlog641.py -lf Mesure1` --> Le dossier crée ainsi que les fichiers se nommeront "Mesure1"

- host (HOST) --> Permet d'effectuer la connexion a UN seul LMG641 via l'IP de celui-ci. En cas d'utilisation de plusieurs LMG641 avec des IP différentes, cette commande permet de sélectionner celui auquel il faut se connecter.
    - `python3 powerlog641.py -host 169.254.6.217` --> Le programme récupérera les données acquises par le LMG641 possédant l'adresse IP 169.254.6.217

- d (DUREE) --> Permet de contrôler le nombre de cycles de mesures en définissant une durée d'execution du programme en nombres de cycles qui dépendent de la période que l'on fixe au LMG641. Si l'on ne spécifie pas cet argument, le programme effectue par défaut 100 cycles et s'arrête une fois les 100 cycles effectués
    - `python3 powerlog641.py -d 0` --> Le programme se lance sans limite de cycle jusqu'à arrêt manuel
    - `python3 powerlog641.py -d 500` --> Le programme se lance et effectue 500 cycles de mesures puis se termine automatiquement

- v (VERBOSE) --> Permet d'afficher dans la console les valeurs que l'on mesure à chaque cycle. Par défaut, rien n'est affiché dans la console si la commande n'est pas activée.
    - `python3 powerlog641.py -v 1` --> Affiche les valeurs mesurés à chaque cycles

- i (INTERVAL) --> Permet de contrôler la période du LMG641. Celle-ci peut varier de 10ms à 60s et contrôle ainsi la fréquence à laquelle le programme va acquérir les données mesurées par le LMG641. Par défaut, l'interval est fixé au minimum (10ms) qui effectue une acquisition toute les 10ms pour assurer la meilleure efficacité du programme. La valeure à définir dans le programme doit être en secondes
    - `python3 powerlog641.py -i 0.01` --> Une acquisition chaque 10ms
    - `python3 powerlog641.py -i 1.0` --> Une acquisition chaque 1s

- p (PLOT) --> Permet de régler la taille de la fenêtre graphique afin d'observer un champ plus ou moins vaste de données. A savoir que les données qui dépassent ce champs ne sont plus observables ensuite. Ainsi cela signifie que si la fenêtre est fixée à 100, elle permet d'observer les données acquises les 100 derniers cycles et non au delà. A savoir qu'à la fin du programme, une capture est faites des données dépendant alors intégralement de la taille de la fenêtre. Par défaut la valeure est fixée à 100 cycles observables afin d'éviter des graphes trop écrasés.
    - `python3 powerlog641.py -d 1000 -p 100` --> Lance une acquisition de 1000 cycles et observe alors à chaque fois les données sur 100 cycles. Les 100 derniers cycles (données de 900 à 1000 cycles) sont capturés via un screenshot et sauvegardés dans le dossier

- a (AUTO AUTO) --> Permet de calibrer les intervales de mesures Courant/Tension du LMG641. Cette fonction est utile si l'on souhaite effectuer des mesures en sélectionnant le capteur souhaitée pour réguler la précision. A savoir que pour fonctionner, le calibrage doit être fait avec des valeurs précises définit par le LMG641 en Courant et Tension auquel cas il ne sera pas pris en compte par le LMG641 et fonctionnera en mode auto :
Tension (en V) : 3.0, 6.0, 12.5, 25.0, 60.0, 130.0, 250.0, 400.0, 600.0, 1000.0
Courant (en A) : 0.005, 0.01, 0.02, 0.04, 0.08, 0.150, 0.300, 0.600, 1.2, 2.5, 5.0, 10.0, 20.0, 32.0
Par défaut, la machine utilise un calibrage automatique, c'est à dire que les valeurs s'adaptent à l'appreil que l'on branche afin de pouvoir directement mesurer la consommation de celui-ci 
    - `python3 powerlog641.py -a 10.0 250.0` --> L'appareil est calibré pour 10A ainsi que 250V et ne détectera aucune valeurs n'avoisinant pas ces valeurs. Exemple la consommation d'une radio 5V aux alentours de 100mA affichera des valeurs à 0 sur le programme
    - `python3 powerlog641.py` ou `python3 powerlog641.py -a 0.0 0.0` --> Utilise le calibrage automatique qui s'adaptera directement à l'appareil branché.

# **Résolution des problèmes**

## **Contributeurs**

Jan de Cuveland --> Le code développé se base sur son travail ayant mis a disposition un socket déjà fait permettant le lien entre l'ordinateur et le LMG641