import os
from scanner.entropy_scanner import calculate_entropy, classify_entropy


def test_entropy_of_empty_file_is_zero(tmp_path):
    filepath = tmp_path / "vazio.txt"
    filepath.write_bytes(b"")

    assert calculate_entropy(str(filepath)) == 0.0


def test_entropy_of_repetitive_content_is_low(tmp_path):
    filepath = tmp_path / "repetitivo.txt"
    filepath.write_bytes(b"a" * 10000)

    entropy = calculate_entropy(str(filepath))

    assert entropy == 0.0


def test_entropy_of_random_bytes_is_high(tmp_path):
    filepath = tmp_path / "aleatorio.bin"
    filepath.write_bytes(os.urandom(50000))

    entropy = calculate_entropy(str(filepath))

    # Dados verdadeiramente aleatórios ficam bem perto do máximo (8.0)
    assert entropy >= 7.5


def test_entropy_of_nonexistent_file_returns_zero():
    entropy = calculate_entropy("/caminho/que/nao/existe.txt")

    assert entropy == 0.0


def test_classify_entropy_thresholds():
    assert classify_entropy(7.9) == ("Muito Alta", 25)
    assert classify_entropy(7.0) == ("Alta", 10)
    assert classify_entropy(5.0) == ("Normal", 0)
    assert classify_entropy(1.0) == ("Baixa", 0)


def test_classify_entropy_boundary_values():
    # Os limites exatos (7.5 e 6.5 e 4.0) devem cair na categoria
    # superior, não na inferior
    assert classify_entropy(7.5) == ("Muito Alta", 25)
    assert classify_entropy(6.5) == ("Alta", 10)
    assert classify_entropy(4.0) == ("Normal", 0)
