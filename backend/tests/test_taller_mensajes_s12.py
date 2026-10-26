"""Pruebas del prototipo S12: ejecutar con python -m unittest discover -s backend/tests -p test_taller_mensajes_s12.py."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from taller_mensajes_s12 import BrokerSimulator, Event


def event():
    return Event("msg-42", "corr-42", 42, "Libro usado")


class MessagesTest(unittest.TestCase):
    def test_duplicate_redelivery_is_idempotent(self):
        broker = BrokerSimulator(sleep_fn=lambda _: None)
        broker.publish(event())
        self.assertEqual(broker.consume(event()), "acked")
        self.assertEqual(broker.consume(event()), "duplicate")
        self.assertEqual(broker.stats(), {"processed": 1, "notifications": 1, "dlq": 0})
        self.assertIn("duplicate_skipped", [x["stage"] for x in broker.trace])

    def test_recoverable_failure_retry_and_trace(self):
        delays = []
        broker = BrokerSimulator(sleep_fn=delays.append)
        broker.publish(event())
        self.assertEqual(broker.consume(event(), transient_failures=1), "acked")
        self.assertEqual(broker.stats()["notifications"], 1)
        self.assertEqual(delays, [2])
        self.assertEqual([x["backoff_seconds"] for x in broker.trace if x["stage"] == "retry_scheduled"], [2])
        self.assertEqual([x["attempt"] for x in broker.trace if x["stage"] == "consumer_acked"], [2])
        self.assertEqual({x["correlation_id"] for x in broker.trace}, {"corr-42"})

    def test_permanent_failure_enters_dead_letter_store(self):
        delays = []
        broker = BrokerSimulator(sleep_fn=delays.append)
        self.assertEqual(broker.consume(event(), permanent_failure=True), "dead_lettered")
        self.assertEqual(broker.stats(), {"processed": 0, "notifications": 0, "dlq": 1})
        self.assertEqual([x["backoff_seconds"] for x in broker.trace if x["stage"] == "retry_scheduled"], [2, 4])
        self.assertEqual(delays, [2, 4])

    def test_compatibility_rejects_major_version(self):
        with self.assertRaises(ValueError):
            Event("msg", "corr", 1, "Libro", schema_version=2).validate()


if __name__ == "__main__":
    unittest.main()
