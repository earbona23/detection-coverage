import json

from coverage.rules import cargar_regla


def test_lee_formato_yaml_detection_as_code(tmp_path):
    f = tmp_path / "r.yaml"
    f.write_text("name: Test\nrelevantTechniques:\n  - T1110\n", encoding="utf-8")
    r = cargar_regla(f)
    assert r["nombre"] == "Test" and r["tecnicas"] == ["T1110"]


def test_lee_formato_json_de_sentinel(tmp_path):
    f = tmp_path / "r.json"
    f.write_text(json.dumps({"properties": {"displayName": "Sentinel rule",
                 "techniques": ["T1078", "T1098"]}}), encoding="utf-8")
    r = cargar_regla(f)
    assert r["nombre"] == "Sentinel rule" and r["tecnicas"] == ["T1078", "T1098"]
