# HUman

*Et si nous étions le plus gros LLM jamais observé ?*

Une expérience plein écran à l'encre de Chine qui déroule la réflexion de Mathieu, sans scroll. On tape une question à une IA, des milliers de lettres explosent et écrivent le titre, puis on traverse l'espace des mots où une phrase se construit, mot par mot, par tirage au sort. Les mots deviennent les étoiles d'une nuit au bord de la mer, où le regard du bonhomme révèle les calculs du paysage, puis on plonge dans une fleur, une graine, une cellule, l'ADN et un atome, où l'électron apparaît tirage après tirage jusqu'à dessiner la forme que le calcul prévoit. Ce nuage explose en étoiles, qui forment une galaxie, puis un réseau cosmique. Ce réseau devient des neurones, puis un visage. Un feu d'artifice remonte toute l'histoire en accéléré jusqu'à un atome vivant : ses électrons partent en courant, allument un neurone, traversent les couches d'une IA et reviennent à l'atome en peignant l'ensō, un seul circuit où passe le même courant.

Ouvrir `index.html` dans un navigateur. Aucune dépendance, aucun build.

Dix langues : français, anglais, chinois, hindi, espagnol, arabe, bengali, portugais, russe et japonais. L'expérience prend automatiquement la langue du navigateur (l'anglais sinon). Le sélecteur en haut permet d'en changer, et `index.html#lang=ja` force une langue.

- Lecture automatique, environ 2 min 40, puis un écran de fin : des questions pour prolonger la réflexion et des lectures pour aller plus loin
- Un clic sur le film : pause ou lecture
- La barre des chapitres, en bas, se glisse pour avancer ou reculer
- Molette ou glisser : avancer et reculer dans le temps
- Flèches : chapitre suivant ou précédent, espace : pause
- Bouton « Activer le son » : un son calculé (Web Audio) où la vague joue ses trois ondes, les graines chantent leur angle, l'ADN se lit à voix haute et les neurones claquent
- La souris déforme la matière sans arrêter le film : les graines s'écartent, l'électron la suit, la mer ondule, les neurones s'allument
- Sous la souris, une loupe montre le calcul caché de ce qu'on survole : l'angle d'une graine, l'onde d'une vague, le vecteur d'un mot, la probabilité de l'électron, la somme d'un neurone
- Les phrases s'écrivent en particules en haut à gauche, se fixent à l'encre, puis se transforment en la phrase suivante
- « Revoir » relance le film, comme une IA qui régénère : à chaque tour, une nouvelle question est tapée

## Traductions

Les textes vivent dans `i18n/*.json`. `fr.json` est la référence, et `i18n/GUIDE.md` donne les règles de traduction (longueurs, phrase de la démo IA, formats de nombres). Après une modification, `python3 i18n/build.py` vérifie les fichiers et les injecte dans `index.html`.
