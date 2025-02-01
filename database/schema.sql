-- SCHEMA version 2.0

-- /////// FASE 0 (bis) ///////
-- compte d'usuari
CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  fallback_email TEXT UNIQUE NOT NULL,  -- per si l'usuari queda orfe de logins, que tingui alguna referència
  profile_pic TEXT,
  date_joined INTEGER DEFAULT (strftime('%s', 'now')),
  username TEXT UNIQUE
);

-- proveïdor d'oauth (inicialment, només google)
CREATE TABLE IF NOT EXISTS login_provider (
  provider TEXT PRIMARY KEY
);

-- detalls d'inici de sessió
CREATE TABLE IF NOT EXISTS login_details (
  sub TEXT,
  provider TEXT,
  user_id INTEGER NOT NULL,
  email TEXT NOT NULL,
  PRIMARY KEY (sub, provider),
  FOREIGN KEY (provider)
    REFERENCES login_provider (provider)
      ON DELETE RESTRICT  -- no deixis eliminar proveïdors que faig servir
      ON UPDATE CASCADE,  -- si canvio el nom (improbable) actualitzo
  FOREIGN KEY (user_id)
    REFERENCES user (id)
      ON DELETE CASCADE  -- si esborro usuari, elimina
      ON UPDATE CASCADE  -- si actualitzo id d'usuari (improbable), actualitza
);

-- //////// FASE 1 ////////
-- DIACRÍPTICS
-- autor (també per els catagrames, a futurs)
CREATE TABLE IF NOT EXISTS autor (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);
-- pista d'encreuats críptics (també per encreuats, a futurs)
CREATE TABLE IF NOT EXISTS cryptic_clue (
  clue_id TEXT PRIMARY KEY,
  word TEXT NOT NULL,
  clue TEXT,
  solution TEXT,
  date_created INTEGER DEFAULT (strftime('%s', 'now')),
  autor_id INTEGER DEFAULT 0,
  FOREIGN KEY (autor_id)
    REFERENCES autor (id)
      ON DELETE SET NULL  -- si l'autor desapareix, conservo la pista sense autor
      ON UPDATE CASCADE   -- si l'autor canvia d'id (improbable), actualitzo
);
-- tipus d'anàlisi (i.e: és de la pista o és de la solució?)
CREATE TABLE IF NOT EXISTS cryptic_clue_analysis_type (
  type TEXT PRIMARY KEY  -- "clue" vs "solution"
);
-- anàlisis d'una pista (taula pont: pista + tipus d'anàlisi)
CREATE TABLE IF NOT EXISTS cryptic_clue_analysis (
  clue_id TEXT,
  analysis_type TEXT,
  PRIMARY KEY (clue_id, analysis_type),
  FOREIGN KEY (clue_id)
    REFERENCES cryptic_clue (clue_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY (analysis_type)
    REFERENCES cryptic_clue_analysis_type (type)
      ON DELETE RESTRICT  -- (no permitas eliminar tipos de analisis si se usan)
      ON UPDATE CASCADE  -- si le cambio el nombre, actualiza
);
-- tipus de blocs de l'anàlisi
CREATE TABLE IF NOT EXISTS analysis_block_type (
  type TEXT PRIMARY KEY,  -- "def", "ind", "mat"...
  name TEXT NOT NULL  -- "definició", "indicador", "material"...
);
-- blocs de l'anàlisi
CREATE TABLE IF NOT EXISTS analysis_block (
  id INTEGER PRIMARY KEY,
  clue_id TEXT NOT NULL,
  analysis_type TEXT NOT NULL,
  block_type TEXT NOT NULL,
  block_start INTEGER NOT NULL,
  block_end INTEGER NOT NULL,
  FOREIGN KEY (clue_id, analysis_type)
    REFERENCES cryptic_clue_analysis (clue_id, analysis_type)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY (block_type)
    REFERENCES analysis_block_type (type)
      ON DELETE RESTRICT  -- (prohibit eliminar tipus de bloc si es fan servir)
      ON UPDATE CASCADE  -- actualitza si li canvio el nom al bloc
);

-- /////// FASE 2 ///////
-- arxiu de diacríptics (quin dia es publica cada pista)
CREATE TABLE IF NOT EXISTS diacriptic_arxiu (
  id INTEGER PRIMARY KEY,
  date_published TEXT NOT NULL,  -- ISO8601 (YYYY-MM-DD), sqlite sap convertir i fer +DD i tal
  num TEXT,  -- assigned on (first) publication
  clue_id TEXT NOT NULL,  -- no el poso UNIQUE per si algun dia he de reciclar pistes antigues
  FOREIGN KEY (clue_id)
    REFERENCES cryptic_clue (clue_id)
      ON DELETE RESTRICT  -- prohibit eliminar pistes que ja estiguin publicades a l'arxiu
      ON UPDATE CASCADE  -- actualitza la referència si li canvio l'id a la pista
);
-- tipus d'etiqueta per poder marcar les pistes críptiques
-- (p.ex. per marcar les que estan pausades que l'arxiu no les pot agafar automàtic, etc)
CREATE TABLE IF NOT EXISTS cryptic_clue_tag_type (
  type TEXT PRIMARY KEY,
  description TEXT NOT NULL
);
-- etiquetes aplicades a les pistes
CREATE TABLE IF NOT EXISTS cryptic_clue_tag (
  clue_id TEXT,
  tag_id TEXT,
  PRIMARY KEY (clue_id, tag_id),
  FOREIGN KEY (clue_id)
    REFERENCES cryptic_clue (clue_id)
      ON DELETE CASCADE  -- si esborro la pista, esborro les seves etiquetes
      ON UPDATE CASCADE,  -- si actualitzo l'id, actualitza la referència
  FOREIGN KEY (tag_id)
    REFERENCES cryptic_clue_tag_type (type)
      ON DELETE RESTRICT  -- no deixis eliminar etiquetes que es fan servir
      ON UPDATE CASCADE  -- si actualitzo l'id de l'etiqueta, actualitza la referència
);

-- /////// FASE 3 ///////
CREATE TABLE IF NOT EXISTS diacriptic_solve (
  clue_id TEXT,
  user_id INTEGER,
  date_solved INTEGER,
  help_used TEXT,  -- string of ordered help items: a1z26 for index of letters given, '?' for the definition
  PRIMARY KEY (clue_id, user_id),
  FOREIGN KEY (clue_id)
    REFERENCES cryptic_clue (clue_id)
      ON DELETE CASCADE  -- si esborro la pista, esborro les solucions
      ON UPDATE CASCADE,  -- si canvio l'id de pista, actualitza la referència
  FOREIGN KEY (user_id)
    REFERENCES user (id)
      ON DELETE CASCADE  -- Si esborro l'usuari, esborro les seves solucions
      ON UPDATE CASCADE  -- si actualitzo l'id d'usuari, actualitza la referència
);
