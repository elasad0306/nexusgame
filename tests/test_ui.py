"""
test_ui.py — Tests UI Playwright NexusGame
===========================================
Contexte : Tests de l'interface utilisateur GameStore avec Playwright.
Pattern Page Object Model (POM) obligatoire — les sélecteurs ne doivent
pas être écrits directement dans les tests.

Lancement :
    pytest tests/test_ui.py -v --headed          # avec navigateur visible
    pytest tests/test_ui.py -v                   # headless (CI)
    pytest tests/test_ui.py -v --html=reports/ui.html

Prérequis :
    playwright install chromium
    # L'API GameStore doit tourner sur http://localhost:5000
"""
import pytest
import time
from playwright.sync_api import Page, expect

from tests.pages.home_page import HomePage
from tests.pages.add_game_modal import AddGameModal

BASE_URL = "http://localhost:5000"


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Tests basiques (sans POM)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.ui
class TestPageBasique:
    """
    Tests directs avec l'objet Page de Playwright.
    Pas de POM ici — comparer avec la section 2 pour voir la différence.
    """

    def test_page_se_charge(self, page: Page):
        """
        TODO — Vérifier que la page principale charge correctement.
        1. Naviguer vers BASE_URL
        2. Vérifier le titre : page.title() == "GameStore"
        3. Vérifier que [data-testid=game-list] est visible
        """
        page.goto(BASE_URL)
        assert page.title() == "GameStore"

        expect(page.locator('[data-testid=game-list]')).to_be_visible()

    def test_compteur_jeux_positif(self, page: Page):
        """
        TODO — Vérifier que le compteur de jeux affiche un nombre > 0.
        [data-testid=game-count] doit contenir un nombre extrait du texte.
        """
        page.goto(BASE_URL)
        counter_games = page.locator('[data-testid=game-count]')

        expect(counter_games).to_be_visible()

        content = counter_games.inner_text()
        number_only = content.split()[0]
        count = int(number_only)

        assert count > 0

    def test_annuler_ferme_le_modal(self, page: Page):
        """
        TODO — Ouvrir le formulaire d'ajout, cliquer Annuler,
        vérifier que [data-testid=add-game-modal] n'est plus visible.
        """
        page.goto(BASE_URL)

        page.get_by_role("button", name="Ajouter un jeu").click()

        modal = page.locator("[data-testid=add-game-modal]")
        expect(modal).to_be_visible()

        modal.get_by_role("button", name="Annuler").click()

        expect(modal).to_be_hidden()


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Tests avec Page Object Model
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.ui
class TestAvecPOM:
    """
    Mêmes scénarios qu'en section 1, mais via les classes POM.
    Comparer la lisibilité et la maintenabilité.
    """

    def test_page_charge_via_pom(self, page: Page):
        """
        TODO — Instancier HomePage, naviguer, vérifier game_list visible.
        """
        home = HomePage(page)
        home.navigate()

        expect(home.game_list).to_be_visible()

    def test_ajouter_jeu_via_pom(self, page: Page):
        """
        TODO — Via HomePage + AddGameModal :
        1. Naviguer
        2. Ouvrir le formulaire
        3. Remplir et soumettre
        4. Vérifier que le titre apparaît dans game_list
        """
        home = HomePage(page)
        home.navigate()

        modal = home.open_add_form()

        test_title = "Zelda: Tears of the Kingdom"
        modal.fill_form(title=test_title, genre="RPG", price="69.99")
        modal.submit()

        expect(home.search(test_title)).to_be_visible()

    def test_recherche_filtre_resultats(self, page: Page):
        """
        TODO — Rechercher "Zelda", vérifier que la première carte contient "Zelda".
        """
        home = HomePage(page)
        home.navigate()

        home.search("Zelda")

        first_card = home.game_cards.first
        expect(first_card).to_contain_text("Zelda")

    def test_filtre_genre_rpg(self, page: Page):
        """
        TODO — Filtrer par "RPG", vérifier que toutes les cartes visibles
        ont [data-testid=game-genre] contenant "RPG".
        """
        home = HomePage(page)
        home.navigate()

        home.filter_genre("RPG")
        genres = home.game_genres.all()
        for genre_badge in genres:
            expect(genre_badge).to_have_text("RPG")


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Choix libres (à justifier dans le README)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.ui
class TestChoixLibresUI:
    """
    Ajoutez ici les parcours utilisateur que vous jugez critiques.
    Documentez vos choix dans le README.
    """

    def test_combinaison_filtre_et_recherche(self, page: Page):
        """Vérifie que le filtrage par genre et la recherche se cumulent."""
        home = HomePage(page)
        home.navigate()

        home.filter_genre("RPG")
        home.search("Zelda")

        for card in home.game_cards.all():
            expect(card).to_contain_text("RPG")
            expect(card).to_contain_text("Zelda")
