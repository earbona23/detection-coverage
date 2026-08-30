from coverage.catalog import Catalogo

CAT = Catalogo()


def test_estados_reales_del_catalogo():
    assert CAT.estado("T1110") == "valida"       # Brute Force
    assert CAT.estado("T1015") == "revocada"     # Accessibility Features (revocada)
    assert CAT.estado("T9999") == "desconocida"  # inventada


def test_padre_de_subtecnica():
    assert CAT.padre("T1114.003") == "T1114"
    assert CAT.padre("T1078") == "T1078"


def test_denominador_excluye_sub_revocadas_y_deprecadas():
    porta = CAT.top_level_por_tactica()
    todas = [t for lst in porta.values() for t in lst]
    for tid in todas:
        assert not CAT.tecnicas[tid]["is_subtechnique"]
        assert not CAT.tecnicas[tid]["revoked"]
        assert not CAT.tecnicas[tid]["deprecated"]
