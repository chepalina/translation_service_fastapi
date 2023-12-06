INSERT INTO words (word_id, word, language, last_updated) VALUES (1, 'apple', 'English', '2023-12-06');
INSERT INTO words (word_id, word, language, last_updated) VALUES (2, 'manzana', 'Spanish', '2023-12-06');


INSERT INTO definitions (definition_id, word_id, language, definition) VALUES (1, 1, 'English', 'A fruit that is red, green, or yellow in color.');
INSERT INTO definitions (definition_id, word_id, language, definition) VALUES (2, 2, 'Spanish', 'Una fruta de color rojo, verde o amarillo.');

INSERT INTO synonyms (synonym_id, word_id, language, synonym) VALUES (1, 1, 'English', 'pome');
INSERT INTO synonyms (synonym_id, word_id, language, synonym) VALUES (2, 2, 'Spanish', 'poma');


INSERT INTO translations (translation_id, word_id, language, translation) VALUES (1, 1, 'Spanish', 'manzana');
INSERT INTO translations (translation_id, word_id, language, translation) VALUES (2, 2, 'English', 'apple');


INSERT INTO examples (example_id, word_id, language, example) VALUES (1, 1, 'English', 'An apple a day keeps the doctor away.');
INSERT INTO examples (example_id, word_id, language, example) VALUES (2, 2, 'Spanish', 'Una manzana al día es salud para la vida.');
