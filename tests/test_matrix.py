from pathlib import Path

from coverage.catalog import Catalogo
from coverage.matrix import calcular
from coverage.rules import cargar_directorio

CAT = Catalogo()
DEMO = str(Path(__file__).resolve().parent.parent / "coverage" / "demo" / "rules")


def test_subtecnica_cubre_a_su_padre_top_level():
    reglas = [{"nombre": "r", "tecnicas": ["T1114.003"]}]  # subtécnica de T1114
    m = calcular(reglas, CAT)
    cubiertas = [tc["tecnica"] for t in m["tacticas"] for tc in t["tecnicas_cubiertas"]]
    assert "T1114" in cubiertas


def test_referencia_revocada_o_inexistente_es_fantasma_no_cobertura():
    reglas = [{"nombre": "r", "tecnicas": ["T1015", "T9999", "T1110"]}]
    m = calcular(reglas, CAT)
    assert m["resumen"]["referencias_invalidas"] == 2   # T1015 revocada + T9999 inexistente
    estados = {i["tecnica"]: i["estado"] for i in m["referencias_invalidas"]}
    assert estados["T1015"] == "revocada"
    assert estados["T9999"] == "desconocida"


def test_demo_produce_cobertura_y_dos_fantasmas():
    reglas = cargar_directorio(DEMO)
    m = calcular(reglas, CAT)
    assert m["resumen"]["reglas"] == 5
    assert m["resumen"]["referencias_invalidas"] == 2
    assert m["resumen"]["tecnicas_cubiertas"] >= 5


def test_cobertura_pct_coherente():
    m = calcular([{"nombre": "r", "tecnicas": ["T1110"]}], CAT)
    r = m["resumen"]
    assert 0 < r["cobertura_pct"] < 100
    assert r["tecnicas_cubiertas"] >= 1
