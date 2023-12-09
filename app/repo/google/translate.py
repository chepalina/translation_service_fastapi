import asyncio
from dataclasses import dataclass
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By

from app.domain.entities import WordEntity


@dataclass
class GoogleTranslateWordRepo:
    """Google Translate scrapper."""

    operation: str = "translate"
    translation_class: str = "HwtZe"
    example_class: str = "me82ge"
    synonym_class: str = "FpAlrf"
    sleep: int = 3

    async def get(self, word: str, sl: str, tl: str) -> Optional["WordEntity"]:

        # here is a bug with auto sl
        link = self._get_link(word, sl, tl)
        driver = webdriver.Chrome()
        word_entity = WordEntity(word=word, language=sl)

        try:
            # blocking operation need to be launched on its own thread
            driver.get(link)

            # wait for page loading
            await asyncio.sleep(3)

            word_entity.definitions = self._get_definitions(driver)
            word_entity.synonyms = self._get_synonyms(driver)
            word_entity.translations = self._get_translations(driver)
            word_entity.examples = self._get_examples(driver)

        except TimeoutException:
            return None
        except WebDriverException:
            return None
        finally:
            driver.close()

        return word_entity

    def _get_link(self, word: str, sl: str, tl: str) -> str:
        return f"https://translate.google.com/?sl={sl}&tl={tl}&text={word}&op={self.operation}"

    def _get_definitions(self, driver) -> list[str]:

        try:
            translation = driver.find_element(By.CLASS_NAME, self.translation_class)
        except NoSuchElementException:
            return []

        return [translation.text]

    def _get_translations(self, driver) -> list[str]:

        try:
            translations = driver.find_elements(By.CLASS_NAME, self.translation_class)
        except NoSuchElementException:
            return []

        return list({t.text for t in translations})[1:]

    def _get_examples(self, driver) -> list[str]:
        try:
            examples = driver.find_elements(By.CLASS_NAME, self.example_class)
        except NoSuchElementException:
            return []

        return list({e.text for e in examples})

    def _get_synonyms(self, driver) -> list[str]:
        try:
            synonyms = driver.find_elements(By.CLASS_NAME, self.synonym_class)
        except NoSuchElementException:
            return []

        return list({s.text for s in synonyms})


# from asyncio import run
#
# async def main():
#     g = GoogleTranslateWordRepo()
#
#     word = await g.get("challenge", "en", "fr")
#     print(word)
#
# run(main())
