# Projet de Scraping et Filtrage d'Articles

Ce projet comprend deux scripts principaux pour récupérer des articles et les filtrer selon leur catégorie ou tags.

## Scripts

### `scrap.py`
Récupère des articles depuis un site web et les insère dans une base de données MongoDB connectée via MongoDB Atlas. Il extrait des informations comme le titre, la catégorie, les tags, l'auteur, et les images.

### `by_category.py`
Permet de filtrer les articles par catégorie ou tag. Il interroge la base de données MongoDB et affiche les articles correspondants.

## Prérequis

- Python 3.x
- Bibliothèques : `requests`, `beautifulsoup4`, `pymongo`

Installez les dépendances avec :

```bash
pip install requests beautifulsoup4 pymongo

python scrap.py

python by_category.py
