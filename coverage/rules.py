"""Carga reglas de detección y extrae sus técnicas de MITRE, de dos formatos:

  1. detection-as-code YAML (campo `relevantTechniques:` — el formato de
     sentinel-detection-as-code).
  2. Reglas de analítica de Sentinel exportadas a JSON (campo `techniques:` dentro de
     `properties`, o en la raíz).

Autodetecta el formato por extensión y forma. Cada regla se normaliza a
{ nombre, tecnicas }.
"""
from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


def _tecnicas_yaml(datos: dict) -> list[str]:
    return [str(t).strip() for t in (datos.get("relevantTechniques") or datos.get("techniques") or [])]


def _tecnicas_sentinel_json(datos: dict) -> list[str]:
    props = datos.get("properties", datos)
    return [str(t).strip() for t in (props.get("techniques") or props.get("relevantTechniques") or [])]


def cargar_regla(ruta: Path) -> dict | None:
    texto = ruta.read_text(encoding="utf-8")
    if ruta.suffix.lower() in (".yaml", ".yml"):
        if yaml is None:
            raise SystemExit("Se necesita PyYAML: pip install -r requirements.txt")
        datos = yaml.safe_load(texto)
        if not isinstance(datos, dict):
            return None
        nombre = datos.get("name") or datos.get("title") or ruta.stem
        return {"nombre": nombre, "tecnicas": _tecnicas_yaml(datos), "archivo": ruta.name}
    if ruta.suffix.lower() == ".json":
        datos = json.loads(texto)
        if not isinstance(datos, dict):
            return None
        props = datos.get("properties", datos)
        nombre = props.get("displayName") or datos.get("name") or ruta.stem
        return {"nombre": nombre, "tecnicas": _tecnicas_sentinel_json(datos), "archivo": ruta.name}
    return None


def cargar_directorio(directorio: str) -> list[dict]:
    base = Path(directorio)
    reglas = []
    for ruta in sorted(base.rglob("*")):
        if ruta.suffix.lower() in (".yaml", ".yml", ".json") and ruta.is_file():
            r = cargar_regla(ruta)
            if r is not None:
                reglas.append(r)
    return reglas
