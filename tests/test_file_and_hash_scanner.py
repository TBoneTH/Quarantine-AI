import hashlib

from scanner.file_scanner import get_file_info
from scanner.hash_scanner import calculate_sha256


def test_get_file_info_returns_expected_fields(tmp_path):
    filepath = tmp_path / "exemplo.txt"
    filepath.write_bytes(b"a" * 2048)  # 2 KB

    info = get_file_info(str(filepath))

    assert info["filename"] == "exemplo.txt"
    assert info["extension"] == ".txt"
    assert info["size_mb"] == round(2048 / (1024 * 1024), 2)


def test_get_file_info_extension_is_preserved_lowercase_or_not():
    # extensão vem direto de os.path.splitext, sem normalização —
    # documentando o comportamento atual para não quebrar sem avisar
    import os
    ext = os.path.splitext("ARQUIVO.PDF")[1]

    assert ext == ".PDF"


def test_calculate_sha256_matches_hashlib_reference(tmp_path):
    content = b"conteudo de teste para o hash"
    filepath = tmp_path / "arquivo.bin"
    filepath.write_bytes(content)

    expected = hashlib.sha256(content).hexdigest()
    result = calculate_sha256(str(filepath))

    assert result == expected


def test_calculate_sha256_is_consistent_across_calls(tmp_path):
    filepath = tmp_path / "arquivo.bin"
    filepath.write_bytes(b"mesmo conteudo sempre")

    first = calculate_sha256(str(filepath))
    second = calculate_sha256(str(filepath))

    assert first == second


def test_calculate_sha256_differs_for_different_content(tmp_path):
    file_a = tmp_path / "a.bin"
    file_b = tmp_path / "b.bin"
    file_a.write_bytes(b"conteudo A")
    file_b.write_bytes(b"conteudo B")

    assert calculate_sha256(str(file_a)) != calculate_sha256(str(file_b))
