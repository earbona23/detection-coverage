"""Calcula la matriz de cobertura: qué técnicas de ATT&CK cubren tus reglas, cuáles
son huecos, y qué reglas referencian técnicas que NO existen o están revocadas.

La honestidad central de la herramienta: una regla que dice cubrir T9999 (inexistente)
o una técnica revocada NO cubre nada. Esa "cobertura fantasma" se reporta aparte, porque
inflar la matriz con IDs falsos es exactamente el autoengaño que un mapa de cobertura
debería evitar.

Cobertura: una técnica top-level cuenta como cubierta si alguna regla la referencia
directamente O referencia una de sus subtécnicas.
"""
from __future__ import annotations

from coverage.catalog import Catalogo


def calcular(reglas: list[dict], cat: Catalogo) -> dict:
    # Técnicas top-level cubiertas (resolviendo subtécnicas a su padre) y refs inválidas.
    cubiertas_top: dict[str, int] = {}
    invalidas: list[dict] = []

    for regla in reglas:
        for tid in regla.get("tecnicas", []):
            estado = cat.estado(tid)
            if estado != "valida":
                invalidas.append({"regla": regla["nombre"], "tecnica": tid, "estado": estado})
                continue
            padre = cat.padre(tid)
            cubiertas_top[padre] = cubiertas_top.get(padre, 0) + 1

    por_tactica_all = cat.top_level_por_tactica()
    tacticas = []
    for tac in cat.tacticas_ordenadas():
        universo = por_tactica_all.get(tac, [])
        cubiertas = [t for t in universo if t in cubiertas_top]
        huecos = [t for t in universo if t not in cubiertas_top]
        total = len(universo)
        tacticas.append({
            "tactica": tac,
            "total": total,
            "cubiertas": len(cubiertas),
            "cobertura_pct": round(100 * len(cubiertas) / total, 1) if total else 0.0,
            "huecos": [{"tecnica": t, "nombre": cat.nombre(t)} for t in huecos],
            "tecnicas_cubiertas": [{"tecnica": t, "nombre": cat.nombre(t), "reglas": cubiertas_top[t]}
                                   for t in cubiertas],
        })

    total_uni = sum(t["total"] for t in tacticas)
    total_cub = sum(t["cubiertas"] for t in tacticas)
    return {
        "procedencia": cat.procedencia,
        "resumen": {
            "reglas": len(reglas),
            "tecnicas_del_catalogo": total_uni,
            "tecnicas_cubiertas": total_cub,
            "cobertura_pct": round(100 * total_cub / total_uni, 1) if total_uni else 0.0,
            "referencias_invalidas": len(invalidas),
        },
        "tacticas": tacticas,
        "referencias_invalidas": invalidas,
    }
