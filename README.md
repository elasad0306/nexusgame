# NexusGame — Suite de Tests

> Projet final 2TES3 — Tests Avancés & Automatisation

## Présentation du projet

<!-- Décrivez le contexte du projet et l'API GameStore. -->

---

## Structure du repo

```
NexusGame/
├── app_gamestore.py
├── requirements.txt
├── tests/
│   ├── conftest.py
│   ├── test_unit.py
│   ├── test_integration.py
│   ├── test_ui.py
│   ├── gamestore_collection.json
│   ├── locust_gamestore.py
│   └── pages/
│       ├── home_page.py
│       └── add_game_modal.py
└── .github/
    └── workflows/
        └── tests.yml
```

---

## Lancer les tests

```bash
# Installation
pip install -r requirements.txt
playwright install chromium
npm install -g newman newman-reporter-htmlextra
pip install locust

# Démarrer l'API
python app_gamestore.py

# Tests unitaires
pytest tests/test_unit.py -v --cov=app_gamestore --cov-report=html

# Tests d'intégration
pytest tests/test_integration.py -v -m integration

# Tests UI
pytest tests/test_ui.py -v --headed

# Collection Newman
newman run tests/gamestore_collection.json --env-var "base_url=http://localhost:5000" --reporters cli,htmlextra

# Tests de charge
locust -f tests/locust_gamestore.py --host=http://localhost:5000 --headless -u 20 -r 2 --run-time 30s
```

---

## Mes choix techniques

### Pyramide de tests adoptée

<!-- Quelle pyramide avez-vous choisie et pourquoi ? -->
La pyramide de tests adoptée c'est une pyramide de test classique. 

Avec beaucoup de test unitaires effectué, on effectué des test sur les trois niveaux : unitaires (15+ tests isolés), intégration (E2E avec serveur réel) et UI (3 parcours critiques). 

Cette structure permet une détection rapide des bugs au niveau des fonctions, puis validation des flux complets en conditions réelles.

### Pipeline CI vs local

<!-- Qu'est-ce qui tourne en CI, qu'est-ce qui reste en local, et pourquoi ? -->
Ce qui tourne en local ce sont les tests d'integrations et tests unitaires, elles permettent de valider le code plus rapidement.
Par contre en CI, refait les test intégrations, tests unitaires, de l'interface (UI),  et Newman, elle vérifie avant de push le code en production

### Mes choix libres

<!-- Pour chaque test libre : ce qu'il teste et pourquoi vous l'avez choisi. -->

#### Pour test ui : Test pour vérifier la persistance du filtre : 
J'ai implémenté ce test ui pour vérifier l'interaction entre la barre de recherche et le menu de déroulant pour selectionner le genre comme exemple ici : 

Chercher  : **Zelda**

Filtre : **RPG**


Je l'ai choisi parce que souvent quand on rajoute une nouvelle fonctionnalité recherche, ça écrase par erreur les filtres existants du coup avec ce test, on confirme qu'il n'y a pas d'erreur. 

Le teste : 
```bash
    def test_combinaison_filtre_et_recherche(self, page: Page):
        """Vérifie que le filtrage par genre et la recherche se cumulent."""
        home = HomePage(page)
        home.navigate()

        home.filter_genre("RPG")
        home.search("Zelda")

        for card in home.game_cards.all():
            expect(card).to_contain_text("RPG")
            expect(card).to_contain_text("Zelda")

```
#### Test de recherche par titre et genre de jeux :

J'ai implémenté ce test pour vérifier la précision de l'api à rechercher un jeu en particulier selon deux critères majeures : 
    
    - Titre 
    - Genre 
Elle est critique en prod parce que la recherche constitue un moteur principal des ventes si l'utilisateur recherche un jeu avec les critères bien précis comme le titre et le genre et que l'api d'autre données alors l'utilisateur quittera la boutique. D'où la nécessité d'implémenter ce genre de test

```bash
def test_search_by_title_genre(self, client):
        """
        Rechercher un jeu par son nom et genre
        """
        create_request = client.post("/games", json={"title": "Uncharted 4", "genre": "Aventure", "price": 49.99})

        title = create_request.get_json()["title"]
        genre = create_request.get_json()["genre"]

        search_request = client.get(f"/games/search?title={title}&genre={genre}")

        response = search_request.get_json()

        result = response["results"][0]

        assert search_request.status_code == 200

        assert result["title"] == title
        assert result["genre"]== genre
```


---

## Investigation de l'API

#### Route de `suppression` :
La route de suppression retournait un **200** après la suppression alors que par convention elle doit retourner un **204**. 

Et dans la documentation docstring aussi la route devait retourner un **204**
Dans mes tests, j'ai suivi la convention ce qui faisait échoué mes tests de suppression. 
Pour le résoudre, j'ai modifié le code de retour de la route par **204**.

#### Route `featured`

#### Problèmes identifiés
- L'ordre de tri est incorrect dans la requête par rapport à la documentation qui demande un tri decroissant 
  - Remplacer `ASC` par `DESC`.

- Absence de `LIMIT` dans la requête SQL :
  - La requête de base :
    ```bash
    SELECT * FROM games ORDER BY rating ASC;
    ```
  - Problème : récupère tous les jeux de la base de données, ce qui est trop lourd et impacte les performances de l'API.

Version de la requête sql modifié : 
```bash
SELECT * FROM games WHERE stock > 0 AND price > 0 ORDER BY rating DESC LIMIT ?
```

<!-- Ce que vous avez observé en testant l'API.
     Comportements inattendus, hypothèses, ce que vos tests révèlent. -->

## Test de performance avec Locust
## Résumé
On peut observer ici que la route ```Post/games``` est plus lent par rapport aux autres routes
Et les deux autres route avec ```Get``` présentent de bonnes performances avec des temps faibles et stables.

| Méthode | Endpoint           | Médiane | 95e percentile (P95) |
|--------|-------------------|--------|---------------------|
| GET    | ```/games/featured``` | 12 ms  | 17 ms               |
| GET    | ```/games/stats```     | 12 ms  | 20 ms               |
| POST   | ```/games```            | 35 ms  | 53 ms               |


---

## Pipeline CI/CD
Lien : https://github.com/elasad0306/nexusgame/actions
<!-- État de votre pipeline sur GitHub Actions. -->

---

## Ce que j'ai appris

<!-- Optionnel. -->
