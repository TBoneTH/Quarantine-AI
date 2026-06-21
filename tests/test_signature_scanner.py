from scanner.signature_scanner import detect_signature, check_extension_mismatch


def test_detect_signature_pdf(tmp_path):
    filepath = tmp_path / "documento.pdf"
    filepath.write_bytes(b"%PDF-1.4\n%resto do conteudo aqui")

    assert detect_signature(str(filepath)) == "Documento PDF"


def test_detect_signature_windows_executable(tmp_path):
    filepath = tmp_path / "qualquer.bin"
    filepath.write_bytes(b"MZ" + b"\x00" * 100)

    assert detect_signature(str(filepath)) == "Executável Windows (PE/EXE/DLL)"


def test_detect_signature_png(tmp_path):
    filepath = tmp_path / "imagem.bin"
    filepath.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

    assert detect_signature(str(filepath)) == "Imagem PNG"


def test_detect_signature_unknown_returns_none(tmp_path):
    filepath = tmp_path / "desconhecido.bin"
    filepath.write_bytes(b"XYZ123 conteudo qualquer sem assinatura conhecida")

    assert detect_signature(str(filepath)) is None


def test_mismatch_when_exe_disguised_as_txt(tmp_path):
    # Caso clássico: executável renomeado para .txt pra enganar o usuário
    filepath = tmp_path / "fotos_ferias.txt"
    filepath.write_bytes(b"MZ" + b"\x00" * 200)

    mismatch, real_type = check_extension_mismatch(str(filepath), ".txt")

    assert mismatch is True
    assert real_type == "Executável Windows (PE/EXE/DLL)"


def test_no_mismatch_when_extension_matches_content(tmp_path):
    filepath = tmp_path / "documento.pdf"
    filepath.write_bytes(b"%PDF-1.4\nconteudo normal de pdf")

    mismatch, real_type = check_extension_mismatch(str(filepath), ".pdf")

    assert mismatch is False
    assert real_type == "Documento PDF"


def test_no_mismatch_when_signature_unrecognized(tmp_path):
    # Se não reconhecemos a assinatura, não acusamos mismatch
    # (evita falso positivo por limitação da nossa tabela)
    filepath = tmp_path / "arquivo.dat"
    filepath.write_bytes(b"conteudo sem assinatura conhecida na tabela")

    mismatch, real_type = check_extension_mismatch(str(filepath), ".dat")

    assert mismatch is False
    assert real_type is None
