# La constellation : mise en ligne

La page `atoms.html` (servie sur `/atoms`) lit et écrit via la fonction Vercel `api/atoms.js`.
Le navigateur ne parle jamais à Supabase directement.

## 1. Supabase
Dans le SQL Editor du projet, exécuter `supabase/atoms.sql`. La table est verrouillée (RLS sans politique) : seule la clé `service_role` y accède.

## 2. Vercel → Settings → Environment Variables
| Variable | Valeur |
|---|---|
| `SUPABASE_URL` | l'URL du projet (Settings → API) |
| `SUPABASE_SERVICE_ROLE_KEY` | la clé `service_role` (secrète, jamais dans le code) |
| `ATOMS_SECRET` | une longue chaîne aléatoire (sert à hacher les IP et signer les défis) |
| `TURNSTILE_SECRET_KEY` | facultatif : Cloudflare Turnstile en plus |
| `ATOMS_MODERATION` | facultatif : `1` pour que chaque message attende une validation |

## Anti-spam, dans l'ordre
pot de miel · temps minimum de remplissage · preuve de travail (~1 s de calcul) · origine vérifiée ·
texte nettoyé (pas de liens, pas de caractères répétés, liste de mots bloqués) · 2 atomes / 10 min et 6 / jour par IP hachée ·
pas de doublon sur 24 h · 3 signalements = masqué.

## Modérer
Dans Supabase, table `atoms` : passer `status` à `hidden` pour retirer un message, ou de `pending` à `visible` pour le publier.
