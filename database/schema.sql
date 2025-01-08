-- SCHEMA version 1.0

CREATE TABLE IF NOT EXISTS user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL,
  date_joined INTEGER DEFAULT (unixepoch()),
  username TEXT UNIQUE
);

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
  date_created INTEGER DEFAULT (unixepoch()),
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

