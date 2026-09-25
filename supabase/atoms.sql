-- La constellation : un atome par personne, un court message.
-- À exécuter une fois dans Supabase (SQL Editor). Rien n'est accessible en public :
-- seule la fonction /api/atoms (clé service_role, côté serveur) lit et écrit.

create table if not exists public.atoms (
  id          bigint generated always as identity primary key,
  created_at  timestamptz not null default now(),
  name        text        not null check (char_length(name) between 1 and 24),
  country     text                 check (country is null or country ~ '^[A-Z]{2}$'),
  message     text        not null check (char_length(message) between 3 and 140),
  shape       smallint    not null check (shape between 0 and 5),
  color       smallint    not null check (color between 0 and 7),
  lang        text                 check (lang is null or char_length(lang) <= 5),
  ip_hash     text        not null,
  reports     integer     not null default 0,
  status      text        not null default 'visible' check (status in ('visible', 'pending', 'hidden'))
);

create index if not exists atoms_visible_idx on public.atoms (id desc) where status = 'visible';
create index if not exists atoms_ip_idx on public.atoms (ip_hash, created_at desc);

-- Signalements : une personne (IP hachée) ne signale un atome qu'une fois
create table if not exists public.atom_reports (
  atom_id    bigint not null references public.atoms (id) on delete cascade,
  ip_hash    text   not null,
  created_at timestamptz not null default now(),
  primary key (atom_id, ip_hash)
);

-- Verrouillé : pas de politique = aucun accès pour anon / authenticated
alter table public.atoms enable row level security;
alter table public.atom_reports enable row level security;

-- Signaler : compte les signalements distincts, masque l'atome à partir de 3
create or replace function public.report_atom(aid bigint, ip text)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into atom_reports (atom_id, ip_hash) values (aid, ip) on conflict do nothing;
  update atoms
     set reports = (select count(*) from atom_reports where atom_id = aid),
         status  = case when (select count(*) from atom_reports where atom_id = aid) >= 3 then 'hidden' else status end
   where id = aid;
end;
$$;
revoke all on function public.report_atom(bigint, text) from public, anon, authenticated;
