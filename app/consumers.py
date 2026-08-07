"""Kafka consumers for eligibility-service.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("eligibility-service.consumers")

TABLE = "eligibility"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("patient.created")
    def _on_patient_created(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    # New patient — establish a placeholder eligibility record.
                    db.execute(f"INSERT INTO {TABLE} (data) VALUES (%s)",
                               (Json({"patient_id": data.get("id"),
                                      "eligible": None,
                                      "status": "pending_check",
                                      "created_from": "patient.created"}),))
        except Exception as e:
            log.exception("eligibility-service/patient.created handler failed: %s", e)
        emit_audit(bus, action="consume.patient.created", actor="system:eligibility-service",
                   target=None, details={"envelope_id": envelope.get("id")})

