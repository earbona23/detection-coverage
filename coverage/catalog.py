"""Catálogo de MITRE ATT&CK: carga el snapshot destilado y responde consultas.

El archivo data/mitre-techniques.json es el catálogo oficial de ATT&CK Enterprise
destilado, CON procedencia (URL de origen, sha256, fecha). No se inventa ni un ID acá:
si una técnica no está en este archivo, no existe (o fue revocada), y así se reporta.
"""
from __future__ import annotations

import json
from pathlib import Path

CATALOGO = Path(__file__).resolve().parent.parent / "data" / "mitre-techniques.json"

# Orden de las tácticas en el orden del kill chain. Los shortnames se toman TAL CUAL del
# catálogo, no se inventan: este snapshot de ATT&CK parte la clásica 'defense-evasion' en
# 'stealth' + 'defense-impairment' (15 tácticas). Si el catálogo trae una táctica que no
# está acá, tacticas_ordenadas() la agrega al final en vez de perderla.
ORDEN_TACTICAS = [
    "reconnaissance", "resource-development", "initial-access", "execution",
    "persistence", "privilege-escalation", "stealth", "defense-impairment",
    "credential-access", "discovery", "lateral-movement", "collection",
    "command-and-control", "exfiltration", "impact",
]


class Catalogo:
    def __init__(self, ruta: Path | None = None) -> None:
        datos = json.loads((ruta or CATALOGO).read_text(encoding="utf-8"))
        self.procedencia = {
            "source": datos.get("source"),
            "sha256": datos.get("sha256_of_source"),
            "retrieved_utc": datos.get("retrieved_utc"),
        }
        self.tecnicas: dict = datos["techniques"]

    def existe(self, tid: str) -> bool:
        return tid in self.tecnicas

    def estado(self, tid: str) -> str:
        """'valida' | 'revocada' | 'deprecada' | 'desconocida'."""
        t = self.tecnicas.get(tid)
        if t is None:
            return "desconocida"
        if t.get("revoked"):
            return "revocada"
        if t.get("deprecated"):
            return "deprecada"
        return "valida"

    def nombre(self, tid: str) -> str:
        t = self.tecnicas.get(tid)
        return t["name"] if t else "(desconocida)"

    def padre(self, tid: str) -> str:
        """El ID top-level de una subtécnica (T1548.002 -> T1548). Idempotente en top-level."""
        return tid.split(".")[0]

    def tacticas_de(self, tid: str) -> list[str]:
        t = self.tecnicas.get(tid)
        return list(t.get("tactics", [])) if t else []

    def top_level_por_tactica(self) -> dict[str, list[str]]:
        """Técnicas top-level VÁLIDAS (no sub, no revocadas, no deprecadas) por táctica.
        Es el denominador honesto de la cobertura."""
        mapa: dict[str, list[str]] = {}
        for tid, t in self.tecnicas.items():
            if t.get("is_subtechnique") or t.get("revoked") or t.get("deprecated"):
                continue
            for tac in t.get("tactics", []):
                mapa.setdefault(tac, []).append(tid)
        return {t: sorted(v) for t, v in mapa.items()}

    def tacticas_ordenadas(self) -> list[str]:
        """Las tácticas presentes en el catálogo, en orden de kill chain; las que no estén
        en ORDEN_TACTICAS se agregan al final para no perderlas nunca."""
        presentes = set(self.top_level_por_tactica())
        ordenadas = [t for t in ORDEN_TACTICAS if t in presentes]
        return ordenadas + sorted(presentes - set(ORDEN_TACTICAS))
