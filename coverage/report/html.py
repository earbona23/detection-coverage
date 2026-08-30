"""Matriz de cobertura estilo ATT&CK Navigator, HTML autocontenido (sin recursos externos)."""
from __future__ import annotations

import html as _h

_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0b0f1a;color:#e7ecf6;font-family:system-ui,Segoe UI,Roboto,sans-serif;padding:24px}
h1{font-size:20px;background:linear-gradient(90deg,#667eea,#c549d0);-webkit-background-clip:text;background-clip:text;color:transparent;margin-bottom:6px}
.sub{color:#8b97b5;font-size:13px;margin-bottom:18px}
.grid{display:flex;gap:8px;overflow-x:auto;padding-bottom:12px}
.col{min-width:150px;flex:0 0 auto}
.col h2{font-size:11px;text-transform:uppercase;letter-spacing:.4px;color:#8b97b5;
  padding:6px 4px;border-bottom:2px solid #26304d;margin-bottom:6px;min-height:44px}
.col .pct{font-size:12px;color:#e7ecf6;font-weight:700}
.cell{font-size:11px;padding:5px 7px;border-radius:5px;margin-bottom:4px;line-height:1.25}
.cov{background:#123a1f;border:1px solid #1c6b38}
.cov .id{color:#2ecc71;font-weight:700}
.gap{background:#1b2338;border:1px solid #26304d;color:#6b7699}
.gap .id{color:#8b97b5}
.n{float:right;color:#8b97b5;font-size:10px}
.invalid{margin-top:20px;padding:12px 14px;border:1px solid #5c1620;background:#2a0d12;border-radius:10px}
.invalid h3{color:#ff5c6c;font-size:14px;margin-bottom:8px}
.invalid li{color:#ff8a94;font-size:13px;list-style:none;margin:3px 0}
.prov{margin-top:18px;color:#8b97b5;font-size:11px}
"""


def render(m: dict) -> str:
    def esc(x):
        return _h.escape(str(x))

    cols = []
    for t in m["tacticas"]:
        celdas = []
        for tc in t["tecnicas_cubiertas"]:
            celdas.append(f'<div class="cell cov"><span class="n">{tc["reglas"]}×</span>'
                          f'<span class="id">{esc(tc["tecnica"])}</span><br>{esc(tc["nombre"])}</div>')
        for g in t["huecos"][:40]:
            celdas.append(f'<div class="cell gap"><span class="id">{esc(g["tecnica"])}</span>'
                          f'<br>{esc(g["nombre"])}</div>')
        cols.append(
            f'<div class="col"><h2>{esc(t["tactica"])}'
            f'<br><span class="pct">{t["cubiertas"]}/{t["total"]} · {t["cobertura_pct"]}%</span></h2>'
            + "".join(celdas) + "</div>")

    invalid = ""
    if m["referencias_invalidas"]:
        items = "".join(f'<li>⚠ {esc(i["tecnica"])} ({esc(i["estado"])}) — «{esc(i["regla"])}»</li>'
                        for i in m["referencias_invalidas"])
        invalid = (f'<div class="invalid"><h3>Cobertura fantasma — {len(m["referencias_invalidas"])} '
                   f'referencia(s) a técnicas inexistentes o revocadas</h3><ul>{items}</ul></div>')

    r = m["resumen"]
    p = m["procedencia"]
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cobertura de detección · MITRE ATT&CK</title><style>{_CSS}</style></head><body>
<h1>Cobertura de detección · MITRE ATT&CK</h1>
<div class="sub">{r['reglas']} reglas · {r['tecnicas_cubiertas']}/{r['tecnicas_del_catalogo']} técnicas
cubiertas ({r['cobertura_pct']}%) · verde = cubierta, gris = hueco</div>
<div class="grid">{''.join(cols)}</div>
{invalid}
<div class="prov">Catálogo ATT&CK: {esc(p['source'])}<br>sha256 {esc(p['sha256'][:32])}… · obtenido {esc(p['retrieved_utc'])}</div>
</body></html>"""
