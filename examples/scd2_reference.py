"""Referencia secuencial SCD2; no es una implementación Delta distribuida."""

from copy import deepcopy
from datetime import date


def apply_snapshot(history, snapshot, effective_date):
    if not isinstance(effective_date, date):
        raise ValueError("effective_date debe ser una fecha")
    keys = [row["customer_id"] for row in snapshot]
    if any(key is None for key in keys) or len(keys) != len(set(keys)):
        raise ValueError("claves de snapshot nulas o duplicadas")
    result = deepcopy(history)
    active = {}
    for row in result:
        if row["valid_to"] is None:
            if row["customer_id"] in active:
                raise ValueError("más de una versión vigente")
            active[row["customer_id"]] = row
    for row in snapshot:
        key, region = row["customer_id"], row["region"]
        current = active.get(key)
        if current and effective_date < current["valid_from"]:
            raise ValueError("fecha anterior a la versión vigente")
        if current and current["region"] == region:
            continue
        if current:
            if effective_date == current["valid_from"]:
                raise ValueError("cambio conflictivo en la misma fecha")
            current["valid_to"] = effective_date
        result.append({"customer_id": key, "region": region,
                       "valid_from": effective_date, "valid_to": None})
    return result
