"""
Serviço de sessão compartilhada via Supabase Realtime.

Responsável por:
- Criar / entrar em sessões com código de 6 caracteres
- Publicar rolagens e mensagens de chat
- Receber eventos em tempo real via subscription
- Expor sinais Qt para atualizar a UI sem bloquear o event loop
"""

import random
import string
import threading
from datetime import datetime
from typing import Optional, Callable

from PyQt6.QtCore import QObject, pyqtSignal

# ---------------------------------------------------------------------------
# Credenciais – preencha após criar o projeto no Supabase
# ---------------------------------------------------------------------------
SUPABASE_URL = "https://rapxipptdtsimholppog.supabase.co"   # ex: "https://xyzxyzxyz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhcHhpcHB0ZHRzaW1ob2xwcG9nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk0NTc4MzAsImV4cCI6MjA5NTAzMzgzMH0.-KTAYB4z2TZZ6P2I_H2SlyHyL2SLGQAF_b6SJpWDrEM"   # chave anon pública do projeto
# ---------------------------------------------------------------------------


def _get_client():
    """Retorna o cliente Supabase, levantando erro descritivo se não configurado."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "Supabase não configurado.\n"
            "Preencha SUPABASE_URL e SUPABASE_KEY em services/session_service.py"
        )
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def _generate_code(length: int = 6) -> str:
    """Gera um código alfanumérico maiúsculo para a sessão."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


# ---------------------------------------------------------------------------
# Worker de Realtime (roda em thread separada)
# ---------------------------------------------------------------------------

class _RealtimeWorker(threading.Thread):
    """Thread que mantém as subscriptions Supabase ativas."""

    def __init__(self, session_id: str,
                 on_roll: Callable, on_message: Callable, on_player: Callable):
        super().__init__(daemon=True)
        self.session_id = session_id
        self.on_roll = on_roll
        self.on_message = on_message
        self.on_player = on_player
        self._stop_event = threading.Event()

    def run(self):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._subscribe())

    async def _subscribe(self):
        import asyncio
        from supabase import acreate_client
        client = await acreate_client(SUPABASE_URL, SUPABASE_KEY)

        def _extract_record(payload) -> dict:
            """Extrai o registro da rolagem/mensagem/jogador do payload Supabase."""
            if not isinstance(payload, dict):
                return {}
            # supabase-py v2 usa 'new' para INSERT
            record = payload.get("new")
            if record:
                return record
            # Fallback: estrutura aninhada em versões mais antigas
            data = payload.get("data", {})
            return data.get("record", data.get("new", {}))

        _seen_rolls    = set()
        _seen_messages = set()
        _seen_players  = set()

        def _dedup_key(record: dict, fields: list) -> str:
            return "|".join(str(record.get(f, "")) for f in fields)

        def handle_roll(payload):
            if self._stop_event.is_set():
                return
            record = _extract_record(payload)
            if not record:
                return
            key = record.get("id") or _dedup_key(record, ["session_id", "player_name", "expression", "result", "created_at"])
            if key in _seen_rolls:
                return
            _seen_rolls.add(key)
            self.on_roll(record)

        def handle_message(payload):
            if self._stop_event.is_set():
                return
            record = _extract_record(payload)
            if not record:
                return
            key = record.get("id") or _dedup_key(record, ["session_id", "player_name", "message", "created_at"])
            if key in _seen_messages:
                return
            _seen_messages.add(key)
            self.on_message(record)

        def handle_player(payload):
            if self._stop_event.is_set():
                return
            record = _extract_record(payload)
            if not record:
                return
            key = record.get("id") or _dedup_key(record, ["session_id", "player_name"])
            if key in _seen_players:
                return
            _seen_players.add(key)
            self.on_player(record)

        channel = (
            client.channel(f"session:{self.session_id}")
            .on_postgres_changes(
                event="INSERT",
                schema="public",
                table="session_rolls",
                filter=f"session_id=eq.{self.session_id}",
                callback=handle_roll,
            )
            .on_postgres_changes(
                event="INSERT",
                schema="public",
                table="session_messages",
                filter=f"session_id=eq.{self.session_id}",
                callback=handle_message,
            )
            .on_postgres_changes(
                event="INSERT",
                schema="public",
                table="session_players",
                filter=f"session_id=eq.{self.session_id}",
                callback=handle_player,
            )
        )
        await channel.subscribe()

        while not self._stop_event.is_set():
            await asyncio.sleep(0.5)

        await client.remove_channel(channel)

    def stop(self):
        self._stop_event.set()


# ---------------------------------------------------------------------------
# SessionService – API pública, expõe sinais Qt
# ---------------------------------------------------------------------------

class SessionService(QObject):
    """
    Sinais emitidos quando novos eventos chegam via Realtime:
      roll_received(dict)     – nova rolagem de outro jogador
      message_received(dict)  – nova mensagem de chat
      player_joined(dict)     – novo jogador entrou na sessão
      session_error(str)      – erro na conexão / configuração
    """

    roll_received    = pyqtSignal(object)
    message_received = pyqtSignal(object)
    player_joined    = pyqtSignal(object)
    session_error    = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session_id:    Optional[str] = None
        self.session_code:  Optional[str] = None
        self.player_name:   Optional[str] = None
        self.character_name: Optional[str] = None
        self._worker: Optional[_RealtimeWorker] = None
        self._my_player_id: Optional[str] = None

    # ------------------------------------------------------------------
    # Propriedade de conveniência
    # ------------------------------------------------------------------

    @property
    def is_active(self) -> bool:
        return self.session_id is not None

    # ------------------------------------------------------------------
    # Criar sessão (DM)
    # ------------------------------------------------------------------

    def create_session(self, dm_name: str, character_name: str = "") -> str:
        """
        Cria uma nova sessão e retorna o código de 6 caracteres.
        Levanta RuntimeError em caso de falha.
        """
        client = _get_client()
        code = _generate_code()

        resp = client.table("sessions").insert({
            "code":    code,
            "dm_name": dm_name,
        }).execute()

        session = resp.data[0]
        self.session_id    = session["id"]
        self.session_code  = code
        self.player_name   = dm_name
        self.character_name = character_name

        self._register_player(dm_name, character_name)
        self._start_realtime()
        return code

    # ------------------------------------------------------------------
    # Entrar em sessão (jogador)
    # ------------------------------------------------------------------

    def join_session(self, code: str, player_name: str, character_name: str = "") -> dict:
        """
        Entra em uma sessão existente pelo código.
        Retorna os dados da sessão.
        Levanta ValueError se o código não existir ou a sessão estiver inativa.
        """
        client = _get_client()
        resp = (
            client.table("sessions")
            .select("*")
            .eq("code", code.upper())
            .eq("is_active", True)
            .execute()
        )

        if not resp.data:
            raise ValueError(f"Sessão '{code}' não encontrada ou já encerrada.")

        session = resp.data[0]
        self.session_id    = session["id"]
        self.session_code  = code.upper()
        self.player_name   = player_name
        self.character_name = character_name

        self._register_player(player_name, character_name)
        self._start_realtime()
        return session

    # ------------------------------------------------------------------
    # Publicar rolagem
    # ------------------------------------------------------------------

    def publish_roll(self, roll_type: str, expression: str,
                     result: int, breakdown: str = ""):
        """Publica uma rolagem na sessão ativa."""
        if not self.is_active:
            return
        try:
            client = _get_client()
            client.table("session_rolls").insert({
                "session_id":     self.session_id,
                "player_name":    self.player_name,
                "character_name": self.character_name,
                "roll_type":      roll_type,
                "expression":     expression,
                "result":         result,
                "breakdown":      breakdown,
            }).execute()
        except Exception as e:
            self.session_error.emit(f"Erro ao publicar rolagem: {e}")

    # ------------------------------------------------------------------
    # Publicar mensagem de chat
    # ------------------------------------------------------------------

    def publish_message(self, message: str):
        """Publica uma mensagem de chat na sessão ativa."""
        if not self.is_active:
            return
        try:
            client = _get_client()
            client.table("session_messages").insert({
                "session_id":  self.session_id,
                "player_name": self.player_name,
                "message":     message,
            }).execute()
        except Exception as e:
            self.session_error.emit(f"Erro ao enviar mensagem: {e}")

    # ------------------------------------------------------------------
    # Buscar histórico inicial
    # ------------------------------------------------------------------

    def fetch_recent_rolls(self, limit: int = 50) -> list:
        """Retorna as últimas `limit` rolagens da sessão."""
        if not self.is_active:
            return []
        client = _get_client()
        resp = (
            client.table("session_rolls")
            .select("*")
            .eq("session_id", self.session_id)
            .order("created_at", desc=False)
            .limit(limit)
            .execute()
        )
        return resp.data or []

    def fetch_recent_messages(self, limit: int = 50) -> list:
        """Retorna as últimas `limit` mensagens de chat da sessão."""
        if not self.is_active:
            return []
        client = _get_client()
        resp = (
            client.table("session_messages")
            .select("*")
            .eq("session_id", self.session_id)
            .order("created_at", desc=False)
            .limit(limit)
            .execute()
        )
        return resp.data or []

    def fetch_players(self) -> list:
        """Retorna os jogadores ativos na sessão."""
        if not self.is_active:
            return []
        client = _get_client()
        resp = (
            client.table("session_players")
            .select("*")
            .eq("session_id", self.session_id)
            .eq("is_active", True)
            .execute()
        )
        return resp.data or []

    # ------------------------------------------------------------------
    # Encerrar sessão
    # ------------------------------------------------------------------

    def leave_session(self):
        """Desconecta o jogador atual da sessão."""
        if not self.is_active:
            return
        try:
            if self._my_player_id:
                client = _get_client()
                client.table("session_players").update({"is_active": False}).eq(
                    "id", self._my_player_id
                ).execute()
        except Exception:
            pass
        finally:
            self._stop_realtime()
            self.session_id    = None
            self.session_code  = None
            self.player_name   = None
            self.character_name = None
            self._my_player_id = None

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------

    def _register_player(self, player_name: str, character_name: str):
        client = _get_client()
        resp = client.table("session_players").insert({
            "session_id":     self.session_id,
            "player_name":    player_name,
            "character_name": character_name,
        }).execute()
        if resp.data:
            self._my_player_id = resp.data[0]["id"]

    def _start_realtime(self):
        self._worker = _RealtimeWorker(
            session_id  = self.session_id,
            on_roll     = lambda d: self.roll_received.emit(d),
            on_message  = lambda d: self.message_received.emit(d),
            on_player   = lambda d: self.player_joined.emit(d),
        )
        self._worker.start()

    def _stop_realtime(self):
        if self._worker:
            self._worker.stop()
            self._worker = None
