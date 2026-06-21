import json

from database import history_manager


def test_save_analysis_creates_file_if_missing(tmp_path, monkeypatch):
    fake_history = tmp_path / "history.json"
    monkeypatch.setattr(history_manager, "HISTORY_FILE", str(fake_history))

    history_manager.save_analysis({"arquivo": "teste.txt", "score": 0})

    assert fake_history.exists()
    data = json.loads(fake_history.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["arquivo"] == "teste.txt"


def test_save_analysis_appends_to_existing_history(tmp_path, monkeypatch):
    fake_history = tmp_path / "history.json"
    fake_history.write_text(
        json.dumps([{"arquivo": "primeiro.txt", "score": 0}]),
        encoding="utf-8",
    )
    monkeypatch.setattr(history_manager, "HISTORY_FILE", str(fake_history))

    history_manager.save_analysis({"arquivo": "segundo.txt", "score": 40})

    data = json.loads(fake_history.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["arquivo"] == "primeiro.txt"
    assert data[1]["arquivo"] == "segundo.txt"


def test_load_history_returns_empty_list_when_file_missing(tmp_path, monkeypatch):
    fake_history = tmp_path / "nao_existe.json"
    monkeypatch.setattr(history_manager, "HISTORY_FILE", str(fake_history))

    assert history_manager.load_history() == []


def test_load_history_returns_saved_records(tmp_path, monkeypatch):
    fake_history = tmp_path / "history.json"
    monkeypatch.setattr(history_manager, "HISTORY_FILE", str(fake_history))

    history_manager.save_analysis({"arquivo": "a.txt", "score": 0})
    history_manager.save_analysis({"arquivo": "b.txt", "score": 50})

    records = history_manager.load_history()

    assert len(records) == 2
    assert records[1]["arquivo"] == "b.txt"


def test_clear_history_empties_existing_records(tmp_path, monkeypatch):
    fake_history = tmp_path / "history.json"
    monkeypatch.setattr(history_manager, "HISTORY_FILE", str(fake_history))

    history_manager.save_analysis({"arquivo": "a.txt", "score": 0})
    history_manager.save_analysis({"arquivo": "b.txt", "score": 50})
    assert len(history_manager.load_history()) == 2

    history_manager.clear_history()

    assert history_manager.load_history() == []


def test_clear_history_creates_empty_file_when_none_exists(tmp_path, monkeypatch):
    fake_history = tmp_path / "nunca_existiu.json"
    monkeypatch.setattr(history_manager, "HISTORY_FILE", str(fake_history))

    history_manager.clear_history()

    assert fake_history.exists()
    assert history_manager.load_history() == []
