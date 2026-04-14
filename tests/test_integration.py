"""
test_integration.py — Tests d'intégration NexusGame
=====================================================
Tests de bout en bout sur l'API GameStore avec un serveur réel.
Ces tests valident le comportement complet, pas seulement la logique unitaire.

Lancement :
    pytest tests/test_integration.py -v -m integration
    pytest tests/test_integration.py -v --html=reports/integration.html
"""
import subprocess

import pytest
import requests
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ════════════════════════════════════════════════════════════════════════════════
# FIXTURE — Serveur GameStore en processus réel
# ════════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="module")
def api_url():
    """
    TODO — Démarrer l'API GameStore en sous-processus réel,
    attendre qu'elle soit prête, puis la stopper après les tests.

    Indice : subprocess.Popen · time.sleep · proc.terminate()
    """
    # À compléter
    # Note : tant que la fixture n'est pas implémentée,
    # l'API doit tourner manuellement avant de lancer ces tests.
    proc = subprocess.Popen([sys.executable, "app_gamestore.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    yield "http://localhost:5000"
    proc.terminate()


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Scénarios de bout en bout
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestScenariosCatalogueComplet:
    """
    Scénarios E2E sur le catalogue de jeux.
    Ces tests utilisent requests (HTTP réel) — pas le client Flask.
    """

    def test_catalogue_initial_non_vide(self, api_url):
        """
        TODO — GET /games retourne 200 et une liste non vide.
        Utiliser requests.get(), pas client.get().
        """
        # À compléter
        response = requests.get(f"{api_url}/games")
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) > 0

    def test_cycle_complet_creation_lecture_suppression(self, api_url):
        """
        TODO — Scénario complet :
        1. POST /games → créer un jeu, récupérer son id
        2. GET /games/{id} → vérifier qu'il existe
        3. DELETE /games/{id} → supprimer
        4. GET /games/{id} → vérifier 404

        """
        # À compléter
        game = {
            "title": "Football Manager 2026",
            "genre": "Sport",
            "price": 59.99
        }
        create_response = requests.post(f"{api_url}/games", json=game)
        assert create_response.status_code == 201

        game_id = create_response.json()["id"]

        get_game = requests.get(f"{api_url}/games/{game_id}")
        assert get_game.status_code == 200
        assert get_game.json()["title"] == "Football Manager 2026"

        delete_game = requests.delete(f"{api_url}/games/{game_id}")
        assert delete_game.status_code == 204

        get_final_game = requests.get(f"{api_url}/games/{game_id}")
        assert get_final_game.status_code == 404

    def test_mise_a_jour_stock(self, api_url):
        """
        TODO — Créer un jeu avec stock=10, PUT pour passer à stock=0,
        vérifier que la valeur est bien persistée en base.
        """
        game = {
            "title": "Asseto Corsa",
            "genre": "Sport",
            "price": 59.99,
            "stock": 10
        }
        create_response = requests.post(f"{api_url}/games", json=game)
        assert create_response.status_code == 201

        game_id = create_response.json()["id"]

        update_response = requests.put(f"{api_url}/games/{game_id}", json={"stock": 0})
        assert update_response.status_code == 200

        get_game = requests.get(f"{api_url}/games/{game_id}")
        assert get_game.json()["stock"] == 0


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Tests de robustesse
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestRobustesse:
    """
    Ces tests valident le comportement de l'API sous des conditions inhabituelles.
    """

    def test_requetes_concurrentes(self, api_url):
        """
        TODO — Envoyer 10 requêtes GET /games en parallèle avec threading.
        Vérifier que toutes retournent 200.

        Indice :
            import threading
            results = []
            def call(): results.append(requests.get(f"{api_url}/games").status_code)
            threads = [threading.Thread(target=call) for _ in range(10)]
            ...
        """
        import threading

        results = []

        def call():
            results.append(requests.get(f"{api_url}/games").status_code)
        threads = [threading.Thread(target=call) for _ in range(10)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        for status in results:
            assert status == 200

    def test_payload_json_malforme(self, api_url):
        """
        TODO — POST /games avec un body non-JSON (texte brut).
        L'API doit retourner 400 sans crasher.
        """
        # À compléter

        fake_data = "Ceci est faux donnée"

        response = requests.post(f"{api_url}/games", data=fake_data)

        assert response.status_code == 400


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Choix libres (à justifier dans le README)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestChoixLibresIntegration:
    """
    Ajoutez ici les scénarios d'intégration que VOUS jugez critiques.

    Pensez aux questions suivantes :
    - Quels enchaînements d'appels représentent un vrai usage de l'API ?
    - Qu'est-ce qui ne peut être testé qu'avec un serveur réel (pas un client Flask) ?
    - Y a-t-il des conditions de bord qui ne se voient qu'en intégration ?

    Documentez vos choix dans le README.
    """
    pass