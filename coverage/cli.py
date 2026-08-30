"""detection-coverage — mapea tus reglas de detección contra MITRE ATT&CK.

  python -m coverage.cli --demo                       # reglas demo
  python -m coverage.cli ./mis-reglas                 # un directorio de reglas
  python -m coverage.cli ./mis-reglas --html cobertura.html
  python -m coverage.cli ./mis-reglas --json informe.json

Acepta reglas en YAML detection-as-code (relevantTechniques) o JSON de reglas de
analítica de Sentinel (techniques). Código de salida 1 si alguna regla referencia una
técnica inexistente o revocada (cobertura fantasma).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from coverage.catalog import Catalogo
from coverage.matrix import calcular
from coverage.report import console, html
from coverage.rules import cargar_directorio

DEMO_DIR = Path(__file__).resolve().parent / "demo" / "rules"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Cobertura de detección vs MITRE ATT&CK")
    p.add_argument("directorio", nargs="?", help="Directorio de reglas (YAML o JSON)")
    p.add_argument("--demo", action="store_true", help="Usar las reglas de ejemplo")
    p.add_argument("--html", type=Path, help="Escribir la matriz HTML")
    p.add_argument("--json", type=Path, help="Escribir el informe JSON")
    p.add_argument("--sin-color", action="store_true")
    args = p.parse_args(argv)

    origen = str(DEMO_DIR) if args.demo or not args.directorio else args.directorio
    reglas = cargar_directorio(origen)
    if not reglas:
        print(f"No encontré reglas en {origen}", file=sys.stderr)
        return 2

    cat = Catalogo()
    m = calcular(reglas, cat)

    if args.html:
        args.html.write_text(html.render(m), encoding="utf-8")
        print(f"Matriz HTML escrita: {args.html}", file=sys.stderr)
    if args.json:
        args.json.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Informe escrito: {args.json}", file=sys.stderr)
    if not args.html and not args.json:
        print(console.render(m, color=not args.sin_color))

    return 1 if m["resumen"]["referencias_invalidas"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
