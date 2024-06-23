
# Projet Marty
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Tests](https://img.shields.io/badge/tests-failing-red)
![Licence](https://img.shields.io/badge/license-MIT-green)

## Introduction
Ce projet a pour but de permettre de contrôler le robot [Marty](https://robotical.io/?currency=EUR) via une interface graphique intuitive et une manette de jeu.
![enter image description here](https://www.planeterobots.com/media/2016/08/Marty-robot.jpg)

## Prérequis
Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.7 ou version supérieure
- pip (le gestionnaire de paquets Python)
- Les bibliothèques Python suivantes :
  - martypy
  - inputs
  - PyQt6

## Installation
1. Clonez le dépôt du projet sur votre machine locale :
    ```sh
    git clone https://github.com/QDAVVV/legendary-disco.git
    ```
2. Accédez au répertoire du projet :
    ```sh
    cd legendary-disco
    ```
3. Installez les dépendances nécessaires :
    ```sh
    pip install -r requirements.txt
    ```

## Utilisation
Pour démarrer l'application, exécutez le script `main.py` :
```sh
python main.py
```

## Contrôle de Marty
Les boutons sur le côté droit de l'interface permettent de contrôler les mouvements de Marty.

![Interface de Contrôle](path/to/control_image.png)

Si une manette est branchée, vous pouvez également contrôler Marty via cette dernière.

## Scratch
Le côté gauche de l'interface graphique permet de coder de façon très basique des actions pour Marty.

![Interface de Scratch](path/to/scratch_image.png)

Après avoir choisi les blocs à effectuer, Marty réalisera les actions dans l'ordre en appuyant sur le bouton "Launch".

## Contribution

Pour contribuer à l'interface Scratch :
- Créer Widget -> Créer Item -> Faire BlockManager -> GetWidget
## Licence
Ce projet est sous licence MIT. Pour plus de détails, consultez le fichier [LICENSE](LICENSE).
