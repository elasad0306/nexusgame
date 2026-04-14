"""
pages/add_game_modal.py — Page Object : modal d'ajout de jeu
==============================================================
Encapsule les interactions avec le formulaire d'ajout de jeu.
"""
from playwright.sync_api import Page, expect



class AddGameModal:

    def __init__(self, page: Page):
        self.page = page

        # TODO — Définir les locators du formulaire.
        #
        self.modal = page.locator("[data-testid=add-game-modal]")
        self.input_title = page.locator("[data-testid=input-title]")
        self.input_genre = page.locator("[data-testid=input-genre]")
        self.input_price = page.locator("[data-testid=input-price]")
        self.submit_btn = page.locator("[data-testid=btn-submit]")
        self.cancel_btn = page.locator("[data-testid=btn-cancel]")

    def fill_and_submit(self, title: str, genre: str, price: float):
        """
        TODO — Remplir le formulaire et soumettre.
        1. Remplir input_title avec title
        2. Remplir input_genre avec genre
        3. Remplir input_price avec str(price)
        4. Cliquer sur submit_btn
        """
        expect(self.modal).to_be_visible()

        self.input_title.fill(title)
        self.input_genre.select_option(genre)
        self.input_price.fill(str(price))

        self.submit_btn.click()
    def cancel(self):
        """TODO — Cliquer sur le bouton Annuler."""
        self.cancel_btn.click()

    def is_visible(self) -> bool:
        """TODO — Retourner True si le modal est visible."""
        return self.modal.is_visible()