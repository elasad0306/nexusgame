"""
test_unit.py — Tests unitaires NexusGame
==========================================
Contexte : Suite de tests unitaires sur l'API GameStore.
Chaque test est isolé — BDD fraîche à chaque appel (fixture function scope).

Lancement :
    pytest tests/test_unit.py -v
    pytest tests/test_unit.py -v --cov=app_gamestore --cov-report=html
"""
from urllib import request, response

import pytest


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Health & endpoints de base
# ════════════════════════════════════════════════════════════════════════════════

class TestHealth:
    def test_health_retourne_200(self, client):
        """
        TODO — Vérifier que GET /health retourne 200 et {"status": "ok"}.
        """
        # À compléter
        request = client.get("/health")
        assert request.status_code == 200

        assert request.json['status'] == "ok"

    def test_health_contient_service(self, client):
        """
        TODO — Vérifier que la réponse contient la clé "service".
        """
        # À compléter
        request = client.get("/health")
        assert "service" in request.json

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Liste des jeux
# ════════════════════════════════════════════════════════════════════════════════

class TestListGames:
    def test_liste_retourne_200(self, client):
        """
        TODO — GET /games retourne 200 et une liste non vide.
        """
        # À compléter
        request = client.get("/games")

        response = request.get_json()

        assert request.status_code == 200

        assert isinstance(response, list)

        assert len(response) > 0

    def test_liste_contient_les_champs_attendus(self, client):
        """
        TODO — Chaque jeu retourné contient au moins : id, title, genre, price, rating.
        """
        # À compléter
        request = client.get("/games")

        responses = request.get_json()

        fields = ["id", "title", "genre", "price", "rating"]
        for response in responses:
            for field in fields:
                assert field in response

    def test_filtre_par_genre(self, client):
        """
        TODO — GET /games?genre=RPG retourne uniquement des jeux RPG.
        Vérifier que tous les éléments ont genre == "RPG".
        """
        # À compléter
        request = client.get("/games?genre=RPG")

        responses = request.get_json()

        for response in responses:
            assert response["genre"] == "RPG"

    def test_tri_par_prix_croissant(self, client):
        """
        TODO — GET /games?sort=price&order=asc retourne les jeux triés par prix croissant.
        """
        # À compléter
        request = client.get("/games?sort=price&order=asc")

        responses = request.get_json()

        last_price = 0
        for response in responses:
            actual_price = response["price"]

            assert actual_price >= last_price

            last_price = actual_price


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Création de jeux
# ════════════════════════════════════════════════════════════════════════════════

class TestCreateGame:
    def test_creation_valide_retourne_201(self, client):
        """
        TODO — POST /games avec titre, genre, prix valides → 201 + id dans la réponse.
        """
        # À compléter
        request = client.post("/games", json={"title": "Asseto Corse", "genre": "Sport", "price": 29.99})

        response = request.get_json()

        assert request.status_code == 201

        assert "id" in response

    def test_creation_sans_titre_retourne_400(self, client):
        """
        TODO — POST /games sans "title" → 400.
        """
        # À compléter
        request = client.post("/games", json={"genre": "Sport", "price": 29.99})

        assert request.status_code == 400


    def test_creation_prix_negatif_retourne_400(self, client):
        """
        TODO — POST /games avec price = -5 → 400.
        """
        # À compléter
        request = client.post("/games", json={"title": "Asseto Corse", "genre": "Sport", "price": -5.00})

        assert request.status_code == 400



    def test_creation_titre_duplique_retourne_409(self, client):
        """
        TODO — Créer le même jeu deux fois → second appel retourne 409.
        """
        # À compléter
        request1 = client.post("/games", json={"title": "Asseto Corse", "genre": "Sport", "price": 29.99})
        request2 = client.post("/games", json={"title": "Asseto Corse", "genre": "Sport", "price": 29.99})


        assert request2.status_code == 409

    @pytest.mark.parametrize("payload,expected_status", [
        # TODO — Ajouter vos cas de validation ici

        ({"title": "Efootball", "genre": "Sport", "price": 29.99}, 201),

        ({"genre": "Sport", "price": 29.99}, 400),

        ({"title": "Efootball","genre": "Sport", "price": -29.99}, 400)
    ])
    def test_validation_parametree(self, client, payload, expected_status):
        """TODO — POST /games avec le payload, vérifier le status code."""
        # À compléter
        request = client.post("/games", json=payload)

        assert request.status_code == expected_status


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Récupération, mise à jour, suppression
# ════════════════════════════════════════════════════════════════════════════════

class TestGameCRUD:
    def test_get_jeu_existant(self, client):
        """
        TODO — Créer un jeu, récupérer son id, GET /games/{id} → 200.
        """
        # À compléter
        game = {
            "title": "Uncharted 4",
            "genre": "Aventure",
            "price": 49.99
        }
        create_request = client.post("/games", json=game)

        id = create_request.get_json()["id"]

        get_request = client.get(f"/games/{id}")

        assert get_request.status_code == 200


    def test_get_jeu_inexistant_retourne_404(self, client):
        """
        TODO — GET /games/99999 → 404.
        """
        # À compléter
        request = client.get("/games/99999")

        assert request.status_code == 404

    def test_update_prix(self, client):
        """
        TODO — Créer un jeu, PUT /games/{id} avec nouveau prix, vérifier la mise à jour.
        """
        # À compléter
        game = {
            "title": "Uncharted 4",
            "genre": "Aventure",
            "price": 49.99
        }
        create_request = client.post("/games", json=game)
        id = create_request.get_json()["id"]

        update_request = client.put(f"/games/{id}", json={"price": 9.99})

        data_update = update_request.get_json()

        assert data_update["price"] == 9.99

    def test_delete_jeu(self, client):
        """
        TODO — Créer un jeu, DELETE /games/{id} → 204, puis GET → 404.
        """
        # À compléter
        game = {
            "title": "Uncharted 4",
            "genre": "Aventure",
            "price": 49.99
        }
        #Requete pour créer le jeu
        create_request = client.post("/games", json=game)
        id = create_request.get_json()["id"]

        #Requette de suppression
        delete_request = client.delete(f"/games/{id}")
        assert delete_request.status_code == 204
        #Requette pour  vérifier si le jeux n'existe plus
        get_request = client.get(f"/games/{id}")
        assert get_request.status_code == 404



# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Choix libres (à justifier dans le README)
# ════════════════════════════════════════════════════════════════════════════════

class TestChoixLibres:
    """
    Ajoutez ici les tests que vous jugez critiques.
    Documentez vos choix dans le README.
    """
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

    
# ════════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Endpoint /games/featured (NGS-108)
# ════════════════════════════════════════════════════════════════════════════════

class TestFeatured:
    """
    Tests sur l'endpoint GET /games/featured.
    Consultez la documentation de l'endpoint dans app_gamestore.py.
    Si un test échoue alors que votre assertion est correcte,
    documentez ce que vous observez dans le README.
    """

    def test_featured_retourne_200(self, client):
        """TODO — GET /games/featured retourne 200."""
        request = client.get("/games/featured")

        assert request.status_code == 200

    def test_featured_retourne_liste(self, client):
        """TODO — La réponse contient une clé 'featured' qui est une liste."""
        request = client.get("/games/featured")

        response = request.get_json()

        assert "featured" in response

        assert isinstance(response["featured"], list)



    def test_featured_max_5_par_defaut(self, client):
        """TODO — Sans paramètre, au maximum 5 jeux sont retournés."""
        request = client.get("/games/featured")

        response = request.get_json()

        assert len(response["featured"]) == 5

    def test_featured_limit_param(self, client):
        """TODO — ?limit=3 retourne au maximum 3 jeux."""
        request = client.get("/games/featured?limit=3")

        response = request.get_json()

        assert len(response["featured"]) == 3


    def test_featured_tries_par_rating_decroissant(self, client):
        """TODO — Les jeux sont triés par rating décroissant."""
        request = client.get("/games/featured")

        responses = request.get_json()

        bad_rating = 5
        for game in responses['featured']:
            current_rating = game["rating"]

            assert current_rating <= bad_rating

            bad_rating = current_rating

    def test_featured_sans_jeux_gratuits(self, client):
        """TODO — Les jeux gratuits ne doivent pas apparaître dans featured."""
        request = client.get("/games/featured")

        responses = request.get_json()
        for game in responses["featured"]:
            assert game["price"] > 0


    def test_featured_sans_jeux_hors_stock(self, client):
        """TODO — Les jeux hors stock ne doivent pas apparaître dans featured."""
        request = client.get("/games/featured")

        responses = request.get_json()
        for game in responses["featured"]:
            assert game["stock"] > 0
