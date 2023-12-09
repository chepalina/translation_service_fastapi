import asyncio
from dataclasses import dataclass
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By

from app.domain.entities import (DefinitionEntity, ExampleEntity,
                                 SynonymEntity, TranslationEntity, WordEntity)


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

            word_entity.definitions = self._get_definitions(driver, tl)
            word_entity.synonyms = self._get_synonyms(driver, tl)
            word_entity.translations = self._get_translations(driver, tl)
            word_entity.examples = self._get_examples(driver, tl)

        except TimeoutException:
            return None
        except WebDriverException:
            return None
        finally:
            driver.close()

        return word_entity

    def _get_link(self, word: str, sl: str, tl: str) -> str:
        return f"https://translate.google.com/?sl={sl}&tl={tl}&text={word}&op={self.operation}"

    def _get_definitions(
        self, driver: "webdriver.Chrome", tl: str
    ) -> list[DefinitionEntity]:

        try:
            translation = driver.find_element(By.CLASS_NAME, self.translation_class)
        except NoSuchElementException:
            return []

        return [DefinitionEntity(definition=translation.text, language=tl)]

    def _get_translations(
        self, driver: "webdriver.Chrome", tl: str
    ) -> list["TranslationEntity"]:

        try:
            translations = driver.find_elements(By.CLASS_NAME, self.translation_class)
        except NoSuchElementException:
            return []

        return [
            TranslationEntity(translation=t, language=tl)
            for t in self._clean(translations)
        ][1:]

    def _get_examples(self, driver: "webdriver.Chrome", tl: str) -> list[ExampleEntity]:
        try:
            examples = driver.find_elements(By.CLASS_NAME, self.example_class)
        except NoSuchElementException:
            return []

        return [ExampleEntity(example=e, language=tl) for e in self._clean(examples)]

    def _get_synonyms(self, driver: "webdriver.Chrome", tl: str) -> list[SynonymEntity]:
        try:
            synonyms = driver.find_elements(By.CLASS_NAME, self.synonym_class)
        except NoSuchElementException:
            return []

        return [SynonymEntity(synonym=s, language=tl) for s in self._clean(synonyms)]

    def _clean(self, results: list) -> set:
        return {r.text for r in results if r.text}


# from asyncio import run
#
# async def main():
#     g = GoogleTranslateWordRepo()
#
#     word = await g.get("challenge", "en", "fr")
#     print(word)
#
# run(main())
