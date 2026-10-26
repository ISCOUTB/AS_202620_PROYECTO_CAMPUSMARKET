"""Prototipo AISLADO: eventos de publicación para notificaciones (sin tocar la API)."""
import json
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone

SCHEMA_VERSION = 1
MAX_ATTEMPTS = 3
BACKOFF_SECONDS = (0, 2, 4)  # esperas reales en demo; reloj inyectado en pruebas


@dataclass(frozen=True)
class Event:
    message_id: str
    correlation_id: str
    publication_id: int
    title: str
    schema_version: int = SCHEMA_VERSION

    def validate(self):
        if self.schema_version != 1:
            raise ValueError("Versión mayor de esquema incompatible")
        if not self.message_id or not self.correlation_id:
            raise ValueError("Identificadores obligatorios")
        if not isinstance(self.publication_id, int) or self.publication_id <= 0:
            raise ValueError("ID de publicación inválido")
        if not isinstance(self.title, str) or not self.title:
            raise ValueError("Título obligatorio")


class BrokerSimulator:
    """Entrega at-least-once mediante redelivery explícito; SQLite solo para el experimento."""
    def __init__(self, connection=None, sleep_fn=None):
        self.db = connection or sqlite3.connect(":memory:")
        self.db.execute("CREATE TABLE IF NOT EXISTS processed (message_id TEXT PRIMARY KEY, publication_id INTEGER NOT NULL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS notifications (publication_id INTEGER NOT NULL, message_id TEXT NOT NULL UNIQUE)")
        self.db.execute("CREATE TABLE IF NOT EXISTS dead_letters (message_id TEXT PRIMARY KEY, payload TEXT NOT NULL, attempts INTEGER NOT NULL, reason TEXT NOT NULL)")
        self.trace = []
        self.sleep_fn = sleep_fn if sleep_fn is not None else time.sleep

    def log(self, event, stage, attempt=0, **fields):
        row = {"time": datetime.now(timezone.utc).isoformat(), "message_id": event.message_id,
               "correlation_id": event.correlation_id, "stage": stage, "attempt": attempt, **fields}
        self.trace.append(row)

    def publish(self, event):
        event.validate()
        self.log(event, "producer_published")

    def consume(self, event, transient_failures=0, permanent_failure=False):
        event.validate()
        for attempt in range(1, MAX_ATTEMPTS + 1):
            self.log(event, "consumer_received", attempt)
            if self.db.execute("SELECT 1 FROM processed WHERE message_id=?", (event.message_id,)).fetchone():
                self.log(event, "duplicate_skipped", attempt)
                return "duplicate"
            try:
                if permanent_failure or attempt <= transient_failures:
                    raise ConnectionError("simulated downstream failure")
                # Ambos efectos comparten transacción SQLite; falla -> rollback.
                with self.db:
                    self.db.execute("INSERT INTO notifications VALUES (?,?)", (event.publication_id, event.message_id))
                    self.db.execute("INSERT INTO processed VALUES (?,?)", (event.message_id, event.publication_id))
                self.log(event, "consumer_acked", attempt)
                return "acked"
            except ConnectionError as exc:
                self.log(event, "attempt_failed", attempt, reason=str(exc))
                if attempt < MAX_ATTEMPTS:
                    delay = BACKOFF_SECONDS[attempt]
                    self.log(event, "retry_scheduled", attempt, backoff_seconds=delay)
                    self.sleep_fn(delay)
                    self.log(event, "retry_elapsed", attempt, backoff_seconds=delay)
                else:
                    with self.db:
                        self.db.execute("INSERT OR REPLACE INTO dead_letters VALUES (?,?,?,?)",
                                        (event.message_id, json.dumps(event.__dict__), attempt, str(exc)))
                    self.log(event, "dead_lettered", attempt)
                    return "dead_lettered"

    def stats(self):
        return {"processed": self.db.execute("SELECT COUNT(*) FROM processed").fetchone()[0],
                "notifications": self.db.execute("SELECT COUNT(*) FROM notifications").fetchone()[0],
                "dlq": self.db.execute("SELECT COUNT(*) FROM dead_letters").fetchone()[0]}


def demo():
    simulator = BrokerSimulator()
    event = Event("msg-publication-42", "corr-demo-001", 42, "Libro usado")
    simulator.publish(event)
    simulator.consume(event, transient_failures=1)
    simulator.consume(event)  # redelivery
    for row in simulator.trace:
        print(json.dumps(row, ensure_ascii=False))
    print(json.dumps(simulator.stats(), ensure_ascii=False))


if __name__ == "__main__":
    demo()
