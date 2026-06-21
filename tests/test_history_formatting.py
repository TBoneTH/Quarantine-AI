from ui.history_formatting import (
    format_entry_summary,
    format_entry_details,
    get_classification_color,
)


def test_format_entry_summary_with_complete_record():
    record = {
        "arquivo": "instalador.exe",
        "classificacao": "Perigoso",
        "score": 65,
        "data_hora": "20/06/2026 14:30:00",
    }

    summary = format_entry_summary(record)

    assert "instalador.exe" in summary
    assert "Perigoso (65 pts)" in summary
    assert "20/06/2026 14:30:00" in summary


def test_format_entry_summary_with_missing_fields_uses_defaults():
    summary = format_entry_summary({})

    assert "Arquivo desconhecido" in summary
    assert "Indefinido (0 pts)" in summary
    assert "data não registrada" in summary


def test_format_entry_details_includes_mismatch_warning():
    record = {
        "data_hora": "20/06/2026 14:30:00",
        "entropia": 7.8,
        "assinatura_divergente": True,
    }

    details = format_entry_details(record)

    assert "Entropia: 7.8" in details
    assert "Assinatura divergente" in details


def test_format_entry_details_omits_warning_when_no_mismatch():
    record = {
        "data_hora": "20/06/2026 14:30:00",
        "entropia": 1.2,
        "assinatura_divergente": False,
    }

    details = format_entry_details(record)

    assert "Assinatura divergente" not in details


def test_get_classification_color_known_values():
    assert get_classification_color("Seguro") == "#2ECC71"
    assert get_classification_color("Suspeito") == "#F39C12"
    assert get_classification_color("Perigoso") == "#E74C3C"


def test_get_classification_color_unknown_falls_back_to_default():
    assert get_classification_color("ValorInexistente") == "#AAAAAA"
