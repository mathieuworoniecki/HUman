-- Dix premiers atomes, pour que la constellation ne s'ouvre pas vide.
-- À exécuter une fois après atoms.sql. Pour les retirer plus tard :
--   delete from public.atoms where ip_hash = 'seed';
insert into public.atoms (name, country, message, shape, color, lang, ip_hash, created_at) values
  ('Léa', 'FR', 'Je crois qu''on est des calculs qui ont appris à s''émerveiller.', 2, 1, 'fr', 'seed', now() - interval '9 days 29 hours'),
  ('Kenji', 'JP', '人は予測するだけじゃない。忘れることもできる。', 4, 6, 'ja', 'seed', now() - interval '8 days 26 hours'),
  ('Amara', 'NG', 'Hunger came before words. So did love.', 3, 4, 'en', 'seed', now() - interval '7 days 23 hours'),
  ('Mateo', 'AR', '¿Y si el alma fuera el error de redondeo?', 5, 5, 'es', 'seed', now() - interval '6 days 20 hours'),
  ('Sofia', 'IT', 'The universe isn''t math. Math is how we fall in love with it.', 1, 0, 'en', 'seed', now() - interval '5 days 17 hours'),
  ('Omar', 'MA', 'We are the cosmos asking itself a question.', 0, 3, 'en', 'seed', now() - interval '4 days 14 hours'),
  ('Priya', 'IN', '20 watts and still dreaming.', 2, 7, 'en', 'seed', now() - interval '3 days 11 hours'),
  ('Jonas', 'DE', 'An AI never had to survive a winter.', 1, 2, 'en', 'seed', now() - interval '2 days 8 hours'),
  ('Ana', 'BR', 'Somos poeira de estrelas com medo do escuro.', 4, 1, 'pt', 'seed', now() - interval '1 days 5 hours'),
  ('Noah', 'CA', 'If I''m calculable, I still want to be surprised.', 5, 6, 'en', 'seed', now() - interval '0 days 2 hours');
