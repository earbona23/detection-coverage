"""Reporte de consola: cobertura por táctica y las referencias inválidas destacadas."""
from __future__ import annotations

_VERDE = "\033[92m"
_AMAR = "\033[93m"
_ROJO = "\033[91m"
_DIM = "\033[90m"
_RESET = "\033[0m"


def _barra(pct: float, ancho: int = 20) -> str:
    llenos = round(pct / 100 * ancho)
    return "█" * llenos + "░" * (ancho - llenos)


def render(m: dict, color: bool = True) -> str:
    def c(txt, col):
        return f"{col}{txt}{_RESET}" if color else txt

    r = m["resumen"]
    out = ["COBERTURA DE DETECCIÓN vs MITRE ATT&CK", "=" * 60]
    out.append(f"Reglas analizadas       : {r['reglas']}")
    out.append(f"Técnicas del catálogo   : {r['tecnicas_del_catalogo']} (top-level, no revocadas)")
    out.append(f"Técnicas cubiertas      : {r['tecnicas_cubiertas']}  ({r['cobertura_pct']}%)")
    if r["referencias_invalidas"]:
        out.append(c(f"Referencias INVÁLIDAS   : {r['referencias_invalidas']} (cobertura fantasma)", _ROJO))
    out.append("")

    for t in m["tacticas"]:
        pct = t["cobertura_pct"]
        col = _VERDE if pct >= 50 else _AMAR if pct > 0 else _DIM
        barra = c(_barra(pct), col)
        out.append(f"  {t['tactica']:<22} {barra} {t['cubiertas']}/{t['total']}  ({pct}%)")

    if m["referencias_invalidas"]:
        out.append("")
        out.append(c("REFERENCIAS INVÁLIDAS — estas reglas NO cubren lo que dicen:", _ROJO))
        for iv in m["referencias_invalidas"]:
            out.append(c(f"  ⚠ {iv['tecnica']} ({iv['estado']}) en «{iv['regla']}»", _ROJO))

    out.append("")
    p = m["procedencia"]
    out.append(c(f"Catálogo ATT&CK: {p['source']}", _DIM))
    out.append(c(f"  sha256 origen {p['sha256'][:24]}…  · obtenido {p['retrieved_utc']}", _DIM))
    return "\n".join(out)
