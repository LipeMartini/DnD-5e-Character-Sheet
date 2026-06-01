-- ============================================================
-- DnD Companion – Session Schema
-- Cole este script no SQL Editor do Supabase e execute.
-- ============================================================

-- Sessões ativas
CREATE TABLE IF NOT EXISTS sessions (
    id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    code        TEXT        UNIQUE NOT NULL,
    dm_name     TEXT        NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    is_active   BOOLEAN     DEFAULT TRUE
);

-- Jogadores conectados a uma sessão
CREATE TABLE IF NOT EXISTS session_players (
    id              UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id      UUID        REFERENCES sessions(id) ON DELETE CASCADE,
    player_name     TEXT        NOT NULL,
    character_name  TEXT,
    joined_at       TIMESTAMPTZ DEFAULT NOW(),
    is_active       BOOLEAN     DEFAULT TRUE
);

-- Histórico de rolagens compartilhado
CREATE TABLE IF NOT EXISTS session_rolls (
    id              UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id      UUID        REFERENCES sessions(id) ON DELETE CASCADE,
    player_name     TEXT        NOT NULL,
    character_name  TEXT,
    roll_type       TEXT        NOT NULL DEFAULT 'ROLL',
    expression      TEXT        NOT NULL,
    result          INTEGER     NOT NULL,
    breakdown       TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Chat da sessão
CREATE TABLE IF NOT EXISTS session_messages (
    id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id  UUID        REFERENCES sessions(id) ON DELETE CASCADE,
    player_name TEXT        NOT NULL,
    message     TEXT        NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Habilitar Realtime para as tabelas de eventos
-- ============================================================
ALTER PUBLICATION supabase_realtime ADD TABLE session_rolls;
ALTER PUBLICATION supabase_realtime ADD TABLE session_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE session_players;

-- ============================================================
-- Row Level Security (RLS) – acesso público via anon key
-- ============================================================
ALTER TABLE sessions         ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_players  ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_rolls    ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_messages ENABLE ROW LEVEL SECURITY;

-- Políticas: qualquer um pode ler e inserir (app desktop usa anon key)
CREATE POLICY "public_read_sessions"   ON sessions         FOR SELECT USING (true);
CREATE POLICY "public_insert_sessions" ON sessions         FOR INSERT WITH CHECK (true);
CREATE POLICY "public_update_sessions" ON sessions         FOR UPDATE USING (true);

CREATE POLICY "public_read_players"    ON session_players  FOR SELECT USING (true);
CREATE POLICY "public_insert_players"  ON session_players  FOR INSERT WITH CHECK (true);
CREATE POLICY "public_update_players"  ON session_players  FOR UPDATE USING (true);

CREATE POLICY "public_read_rolls"      ON session_rolls    FOR SELECT USING (true);
CREATE POLICY "public_insert_rolls"    ON session_rolls    FOR INSERT WITH CHECK (true);

CREATE POLICY "public_read_messages"   ON session_messages FOR SELECT USING (true);
CREATE POLICY "public_insert_messages" ON session_messages FOR INSERT WITH CHECK (true);
